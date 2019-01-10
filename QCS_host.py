from __future__ import print_function
from pymongo import MongoClient
import vinDecoder

# mongodb account info and connection
mongodbUser = "qcs"
mongodbPass = "Flash&spiderman1"
mongodbClient = MongoClient("ds139934.mlab.com", 39934)
mongodbRoot = mongodbClient['qcs']
mongodbRoot.authenticate(mongodbUser, mongodbPass)


def lambda_handler(event, context):
    #user_collection = mongodbRoot.user_profiles
    msg = event['Body']
    print("Received event: " + str(event))
    #user_collection.insert_one({'phoneNumber': event['From'], 'fullName': 'Wahab Ehsan', 'company': 'Sammys Auto'})
    #user_info = user_collection.find_one({'phoneNumber': event['From']})
    #if user_info == None:
    #    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>' + "\n\n" + "Welcome to Quick Car Sort. Enter name?" + '</Message></Response>'
    response = command_check(msg)

    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>' + "\n\n" + str(response) + '</Message></Response>'


def command_check(msg):
    msg_array = msg.split("+")
    command = msg_array[0]
    if command.lower() == "add":
        info = add_process(msg_array[1])
    elif command.lower() == "get":
        info = get_process(msg_array[1])
    elif command.lower() == "search":
        info = search_vehicle(msg_array[1])
    else:
        info = "No such command"
    return info


def search_vehicle(vin_num):
    vin_d = vinDecoder.VinDecoder()
    info, vin, year, model, make, cyl, trim = vin_d.decode(vin_num)
    return str(make_response(vin, year, model, make, cyl, trim))


def get_process(stock_id):
    vehicle_info = get_vehicle(stock_id)
    if vehicle_info == None:
        return "Car not found."
    response = "Car found: \n" + str(vehicle_info['year']) + " " + str(vehicle_info['make']) + " " + str(vehicle_info['model']) + "\nColor: " + str(vehicle_info['color']) + "\nVin: " + str(vehicle_info['vin']) + "\nTrim: " + str(vehicle_info['trim']) + "\nTitle: " + str(vehicle_info['title']) + "\nDescription: " + str(vehicle_info['description'])
    return response


def get_vehicle(stock_id):
    vehicle_collection = mongodbRoot.vehicles
    return vehicle_collection.find_one({'id': stock_id})


def add_process(vin):
    vind = vinDecoder.VinDecoder()
    info, vin, year, model, make, cyl, trim = vind.decode(vin)
    return add_vehicle(info)


def add_vehicle(vehicle_info):
    if vehicle_info['make'] == None:
        return "Invalid Vin"
    vehicle_collection = mongodbRoot.vehicles
    vehicle_collection.insert_one({'id': vehicle_info['vin'][-4:], 'year': vehicle_info['year'], 'make': vehicle_info['make'], 'model': vehicle_info['model'], 'trim': vehicle_info['trim'], 'vin': vehicle_info['vin'], 'color': "", 'cylinder': vehicle_info['cyl'], 'priceBought': 0, 'priceSold': 0, 'public': False, "description": "", 'title': "salvage", "partTotalCost": 0, 'partDetail': {'right fender': {'cost': 0, 'detial': ""}}})
    return 'Added ' + vehicle_info['year'] + " " + vehicle_info['make'] + " " + vehicle_info['model']


def make_response(vin, year, model, make, cyl, trim):
    response = str(year) + " " + str(make) + " " + str(model) + "\nCylinder: " + str(cyl) + "\nTrim: " + str(trim) + "\nVIN: " + str(vin)
    return response


if __name__ == '__main__':
    event = {
        "From": "+13364176628",
        #'Body': "add 1N4AL3AP6FC149535"
        "Body": "get 0855"
        #"Body": "Search 1N4AL3AP6FC149535"
    }
    print (lambda_handler(event, ""))
    #add_process('2HGFB2F59CH586931')
