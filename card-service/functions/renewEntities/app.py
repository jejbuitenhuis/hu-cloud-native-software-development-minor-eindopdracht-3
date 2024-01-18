import os
import time
import traceback
from os import environ
from aws_xray_sdk.core import patch_all
import boto3
import logging
import requests
import ijson
import json

if 'DISABLE_XRAY' not in environ:
    patch_all()

dynamodb = boto3.resource('dynamodb', 'us-east-1')
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
update_frequency_days = os.getenv("CARDS_UPDATE_FREQUENCY")

table = dynamodb.Table(DYNAMODB_TABLE_NAME)

event_bus = boto3.client('events')
logger = logging.getLogger()
logger.setLevel("INFO")

ttlOffSetSecs = (3 * 60 * 60)
local_filename = os.getenv("CARD_JSON_LOCATION", "/tmp/default-cards.json")


def createCardFace(card, oracle_id, scryfall_id, face_count=1):
    image_uris = card.get('image_uris', {})  # Check if 'image_uris' exists, provide an empty dictionary as default
    return {
        "PK": f'OracleId#{oracle_id}',
        "SK": f'PrintId#{scryfall_id}#Face#{face_count}',
        "OracleText": card.get('oracle_text', ''),  # we set default values in case a field isn't specified
        "ManaCost": card.get('mana_cost', ''),
        "TypeLine": card.get('type_line', ''),
        "FaceName": card.get('name', ''),
        "FlavorText": card.get('flavor_text', ''),
        "ImageUrl": image_uris.get('png', ''),
        "Colors": str(card.get('colors', [])),
        "DataType": "Face"
    }


def getOracleFromCard(card):
    if card.get('layout', '') == 'reversible_card':
        return card['card_faces'][0]['oracle_id']
    else:
        return card['oracle_id']


def createCardInfo(card, oracle_id):
    try:
        return {
            "PK": f'OracleId#{oracle_id}',
            "SK": f'PrintId#{card["id"]}#Card',
            "OracleName": card['name'],
            "SetName": card['set_name'],
            "ReleasedAt": card['released_at'],
            "Rarity": card['rarity'],
            "Price": card['prices']['eur'],
            "DataType": "Card"
        }
    except Exception as error:
        logger.error(f"An error has occurred while processing card: \n{card}\n "
                     f"Error: \n {error}")


# Can only handle 25 items at a time!
def writeBatchToDb(items, table, ttl):
    with table.batch_writer() as batch:
        for item in items:
            item['RemoveAt'] = ttl
            response = batch.put_item(
                Item=item
            )


def calculateTTL(offsetInSeconds, update_frequency_days):
    currentEpochInSeconds = int(time.time())
    return currentEpochInSeconds + offsetInSeconds + int(update_frequency_days) * 24 * 60 * 60


def cutTheListAndPersist(item_list, ttl):
    if len(item_list) < 25:
        return item_list

    to_be_persisted = item_list[:25]
    to_be_continued = item_list[25:]

    writeBatchToDb(to_be_persisted, table, ttl)
    return to_be_continued


def countPersistedItems(amount):
    global persistedCounter
    persistedCounter += amount


def lambda_handler(event, context):
    ttl = calculateTTL(ttlOffSetSecs, update_frequency_days)

    with requests.get("https://api.scryfall.com/bulk-data") as response:
        if response.status_code == 200:
            bulk_data_items = response.json()
        else:
            logger.info(f'Failed to fetch bulk data information. Status code: {response.status_code}')

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

    with open(f'{local_filename}', "rb") as file:
        cards = ijson.items(file, 'item')

        item_list = []
        for card in cards:
            oracle_id = getOracleFromCard(card)
            card_info = createCardInfo(card, oracle_id)
            card_faces = []
            item_list.append(card_info)

            if card.get("card_faces") != None:
                face_count = 0
                for face in card['card_faces']:
                    face_count += 1
                    card_faces.append(createCardFace(card, oracle_id, card['id'], face_count))
            else:
                card_faces.append(createCardFace(card, oracle_id, card['id']))

            item_list.extend(card_faces)
            item_list = cutTheListAndPersist(item_list, ttl)

        item_list = cutTheListAndPersist(item_list, ttl)

        writeBatchToDb(item_list, table, ttl)
        logger.info("Finished!")
    return True
