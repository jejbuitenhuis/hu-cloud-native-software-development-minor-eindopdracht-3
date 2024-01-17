import json
import os
import shutil
from os import environ
from aws_xray_sdk.core import patch_all
import boto3
import logging
import requests
import ijson

if 'DISABLE_XRAY' not in environ:
    patch_all()

dynamodb = boto3.resource('dynamodb', 'us-east-1')
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

event_bus = boto3.client('events')
logger = logging.getLogger()
logger.setLevel("INFO")

local_filename = "/tmp/default-cards.json"

def createCardFaces(cardFaces, oracleId, scryfallId):
    faces = []
    for cardFace in cardFaces:
        index = cardFaces.index(cardFace) + 1
        faces.append({
            "PK": f'OracleId#{oracleId}',
            "SK": f'PrintId#{scryfallId}#Face#{index}',
            "OracleText": cardFace.get('oracle_text', ''),
            "ManaCost": cardFace.get('mana_cost', ''),
            "TypeLine": cardFace.get('type_line', ''),
            "FaceName": cardFace.get('name', ''),
            "FlavorText": cardFace.get('flavor_text', ''),
            "ImageUrl": cardFace['image_uris'].get('png', ''),
            "Colors": str(cardFace.get('colors', [])), #Colors will return a list so we convert it to a string before handing it over to the database
            "DataType": "Face"
            # TODO: add ttl
        })
    return faces

def createCardFace(card):
    return {
        "PK": f'OracleId#{card["oracle_id"]}', #PK and sk don't have default values because if they aren't there throwing and error would be correct
        "SK": f'PrintId#{card["id"]}#Face#1',
        "OracleText": card.get('oracle_text', ''), #we set default values in case a field isn't specified
        "ManaCost": card.get('mana_cost', ''),
        "TypeLine": card.get('type_line', ''),
        "FaceName": card.get('name', ''),
        "FlavorText": card.get('flavor_text', ''),
        "ImageUrl": card['image_uris'].get('png', ''),
        "Colors": str(card.get('colors', [])), #Colors will return a list so we convert it to a string before handing it over to the database
        "DataType": "Face"
    }

def createCardInfo(card):
    return {
        "PK": f'OracleId#{card["oracle_id"]}',
        "SK": f'PrintId#{card["id"]}#Card',
        "OracleName": card['name'],
        "SetName": card['set_name'],
        "ReleasedAt": card['released_at'],
        "Rarity": card['rarity'],
        "Price": card['prices']['eur'],
        "DataType": "Card"
    }


# Can only handle 25 items at a time!
def writeBatchToDb(items, table):
    with table.batch_writer() as batch:
        for item in items:
            response = batch.put_item(
                Item=item
            )


# will submit several times if needed
def appendListAndSubmitIfNeeded(entryList=[], toAddList=[], toAddItem=None, table=None):
    returnList = entryList.copy()

    if toAddItem != None:
        toAddList.append(toAddItem)
    returnList.extend(toAddList)

    if len(returnList) >= 25:
        # cuts the list into pieces of 25 leaving the rest that is below 25
        for i in range(len(returnList) // 25):
            writeBatchToDb(returnList[:25], table)
            del returnList[:25]

    return returnList


def lambda_handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    bulk_data_items = requests.get("https://api.scryfall.com/bulk-data").json()

    # Because we fetch a json file with multiple items with different types we first need to find the one with the type default_card
    for item in bulk_data_items["data"]:
        if item["type"] == "default_cards":
            default_cards_uri = item["download_uri"]


    with requests.get(default_cards_uri, stream=True) as response:
        if response.status_code == 200:
            # wb for write bytes
            with open(local_filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            logger.info(f"Downloaded '{local_filename}' successfully.")
        else:
            logger.info(f"Failed to download. Status code: {response.status_code}")

    # Check faces object exists, extract them from the single card JSON notation using for loop
    # AWS BatchWriteItem per batch item

    with open(local_filename, "rb") as file:
        cards = ijson.items(file, 'item')

        processedCards = []
        for card in cards:
            try:
                cardInfo = createCardInfo(card)
                processedCards = appendListAndSubmitIfNeeded(processedCards, toAddItem=cardInfo, table=table)

                # If a card only has multiple faces the face data is put in card_faces.
                if card.get("card_faces") == None:
                    cardFace = createCardFace(card)
                    processedCards = appendListAndSubmitIfNeeded(processedCards, toAddItem=cardFace, table=table)
                else:
                    cardFaces = createCardFaces(card["card_faces"], card["oracle_id"], card['id'])
                    processedCards = appendListAndSubmitIfNeeded(processedCards, toAddList=cardFaces, table=table)
            except Exception as error:
                logger.error(f"An error has occurred while processing card: \n{card} \n Error: \n {error}")

        writeBatchToDb(processedCards) #because appendListAndSubmitIfNeeded only submits when the item count is >= 25 we need to write away the last few cards
    return True
