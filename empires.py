import requests
import json
from pymongo import MongoClient
from log import logger

# video recording


empires_endpoint = r"https://age-of-empires-2-api.herokuapp.com/api/v1/unit/"


def get_empire_name():
    """
    Getting name of id for empire from user input
    :return: name_or_id for empire  (str)
    """
    logger.info('Getting empire name from user')
    name_or_id = input("ID or name of the unit to fetch")
    counter = 0
    max_attempts = 3
    while not name_or_id:
        counter += 1
        name_or_id = input(f"Required ID or name ({max_attempts - counter + 1}) remains")
        if counter == max_attempts:
            print('Max Attempts, Try Again Later')
            break
    if name_or_id:
        logger.info('Empire Name or ID is "{}"'.format(name_or_id))
    else:
        logger.info('Empty Empire Name or ID')
    return name_or_id


def get_empire_info(name_or_id):
    """
    :param
        name or id for empire
        name(str)
        id (int, str)
    :return all empire data (dic) or False
    """
    if not name_or_id:
        logger.info("Missing name or id for empire")
        return {'message': '400 Bad Request'}
    logger.info(f'Starting getting data for empire "{name_or_id}"')
    unit_endpoint = f"{empires_endpoint}{name_or_id}"  # accept id as int in case of using function independently
    response = requests.get(unit_endpoint)
    # assert response.status_code == 200
    if response.status_code == 200:
        data = response.json()
        json_file = open('empire_info.json', 'w')
        json.dump(data, json_file, indent=4, sort_keys=False)
        json_file.close()
        logger.info(f'Finishing retrieving data for empire "{name_or_id}"')
        return data

    else:
        logger.info(f'"{name_or_id}" {response.reason}')
        return False


def to_mongodb():
    """
    Connect with mongodb and insert all data of empire
    :return: None
    """
    logger.info("Starting Connection to mongodb")
    client = MongoClient('localhost', 27017)
    db = client['CloudInn']
    collection_empires = db['empires']

    with open('empire_info.json') as f:
        file_data = json.load(f)   # you can also use (empire_info) dictionary to insert

    logger.info("Inserting Data to mongodb")
    collection_empires.insert_one(file_data)
    logger.info("Closing Connection with mongodb")
    client.close()


def main():
    name_or_id = get_empire_name()
    if name_or_id:
        empire_info = get_empire_info(name_or_id)
        if empire_info is not False:
            print(empire_info)
            to_mongodb()


if __name__ == '__main__':
    main()