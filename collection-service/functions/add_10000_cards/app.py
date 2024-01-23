import os
from os import environ
from aws_xray_sdk.core import patch_all
import boto3
import logging
import ijson
import uuid
import random

if 'DISABLE_XRAY' not in environ:
    patch_all()

dynamodb = boto3.resource('dynamodb', 'us-east-1')
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
user_id = os.getenv("USERID")
local_filename = os.getenv("CARD_JSON_LOCATION")

table = dynamodb.Table(DYNAMODB_TABLE_NAME)

LOGGER = logging.getLogger()
LOGGER.setLevel("INFO")

def parse_card_item_from_own_lambda(item, user_id, condition):
    card_instance_id = str(uuid.uuid4())
    face_items = []

    for face in item['CardFaces']:
        face_items.append({
            "OracleText": face['OracleText'],
            "ManaCost": face['ManaCost'],
            "TypeLine": face['TypeLine'],
            "FaceName": face['FaceName'],
            "FlavorText": face['FlavorText'],
            "ImageUrl": face['ImageUrl'],
            "Colors": face['Colors'],
            "LowercaseFaceName": face['LowercaseFaceName'],
            "LowercaseOracleText": face['LowercaseOracleText']
        })

    return {
        "PK": f'UserId#{user_id}',
        "SK": f'CardInstanceId#{card_instance_id}',
        "PrintId": item["PrintId"],
        "OracleId": item['OracleId'],
        "CardInstanceId": card_instance_id,
        "Condition": condition,
        "DeckId": "",
        "OracleName": item['OracleName'],
        "SetName": item['SetName'],
        "ReleasedAt": item['ReleasedAt'],
        "Rarity": item['Rarity'],
        "Price": item['Price'],
        "LowerCaseOracleName": item['LowerCaseOracleName'],
        "CardFaces": face_items,
        "GSI1SK": ""
    }

def create_card_info(card, oracle_id):
    try:
        return {
            "PK": f'OracleId#{oracle_id}',
            "SK": f'PrintId#{card["id"]}',
            "OracleName": card['name'],
            "SetName": card['set_name'],
            "ReleasedAt": card['released_at'],
            "Rarity": card['rarity'],
            "Price": card['prices']['eur'],
            "OracleId": oracle_id,
            "PrintId": card['id'],
            "LowerCaseOracleName" : str.lower(card.get('name', ''))
        }
    except Exception as error:
        LOGGER.error(f"An error has occurred while processing card: \n{card}\n "
                     f"Error: \n {error}")

def turn_card_into_face_item(card):
    image_uris = card.get('image_uris', {})
    return {
        "OracleText": card.get('oracle_text', ''),
        "ManaCost": card.get('mana_cost', ''),
        "TypeLine": card.get('type_line', ''),
        "FaceName": card.get('name', ''),
        "FlavorText": card.get('flavor_text', ''),
        "ImageUrl": image_uris,
        "Colors": card.get('colors', []),
        "LowercaseFaceName": str.lower(card.get('name', '')),
        "LowercaseOracleText": str.lower(card.get('oracle_text', ''))
    }


def turn_face_into_face_item(face, card_image_uri):
    return {
        "OracleText": face.get('oracle_text', ''),
        "ManaCost": face.get('mana_cost', ''),
        "TypeLine": face.get('type_line', ''),
        "FaceName": face.get('name', ''),
        "FlavorText": face.get('flavor_text', ''),
        "ImageUrl": card_image_uri,
        "Colors": face.get('colors', []),
        "LowercaseFaceName": str.lower(face.get('name', '')),
        "LowercaseOracleText": str.lower(face.get('oracle_text', ''))
    }

def getOracleFromCard(card):
    if card.get('layout', '') == 'reversible_card':
        return card['card_faces'][0]['oracle_id']
    else:
        return card['oracle_id']

def getCombinedLowerCaseOracleText(faces):
    loweredText = "";
    for face in faces:
        loweredText += str.lower(face.get('OracleText', ''))
        loweredText += " "
    return loweredText

def writeBatchToDb(items, table):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

def cutTheListAndPersist(item_list):
    if len(item_list) < 25:
        return item_list

    to_be_persisted = item_list[:25]
    to_be_continued = item_list[25:]

    LOGGER.info(f"Persisting {len(to_be_persisted)} items")

    writeBatchToDb(to_be_persisted, table)
    return to_be_continued

def getRandomCondition():
    conditions = ["Mint", "Near Mint", "Lightly Played", "Moderately Played", "Heavily Played", "Damaged"]
    return random.choice(conditions)

def get_image_uri_from_face(card):

    if hasattr(card, 'card_faces'):
        if hasattr(card['card_faces'][0], 'image_uris'):
            return True
        else:
            return False

def lambda_handler(event, context):
    with open(f'{local_filename}', "rb") as file:
        LOGGER.info("Started the function")
        cards = ijson.items(file, 'item')

        card_counter = 0

        item_list = []
        for card in cards:
            if card_counter < 13000:
                card_counter += 1
                oracle_id = getOracleFromCard(card)
                card_info = create_card_info(card, oracle_id)
                card_faces = []

                if card.get("card_faces") != None:
                    face_count = 0
                    for face in card['card_faces']:

                        if get_image_uri_from_face(card):
                            card_image_uri = face['image_uris'].get('png', '')
                        else:
                            card_image_uri = card['image_uris'].get('png', '')

                        face_count += 1
                        card_faces.append(turn_face_into_face_item(face, card_image_uri))
                else:
                    card_faces.append(turn_card_into_face_item(card))

                card_info['CardFaces'] = card_faces
                card_info['CombinedLowercaseOracleText'] = getCombinedLowerCaseOracleText(card_faces)

                collection_card_info = parse_card_item_from_own_lambda(card_info, user_id, getRandomCondition())

                item_list.append(collection_card_info)
                item_list = cutTheListAndPersist(item_list)
            else:
                LOGGER.info(f"Finished adding: {card_counter} cards, breaking")
                break

        item_list = cutTheListAndPersist(item_list)
        if len(item_list) != 0:
            LOGGER.info(f"Persisting {len(item_list)} items")
            writeBatchToDb(item_list, table)

        LOGGER.info(f"Finished!")
    return True