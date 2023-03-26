import requests
import json
import random
import string
import time
import sys
import argparse

def get_random_name(name_lenght = 10):
    # Generate random name
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=name_lenght))

def get_id(url):
    responce = requests.get(url)
    random_item = random.choice(responce.json())
    id = random_item['id']
    return id

def get_payload(service):

    payload = {}

    if service == "products":
        # Request body
        payload = {
            "productName": get_random_name(),
            "userId": random.randint(1, 1000),
            "price": random.randint(1, 100),
            "description": "This is a test description. There's nothing special. Just to make the product have a description"
        }
    elif service == "accounts":
        payload = {
            "username": get_random_name(),
            "password": get_random_name()
        }
    elif service == "orders":
        payload = {
            "productName": get_random_name(),
            "postUserId": random.randint(1, 1000),
            "purchaseUserId": random.randint(1, 1000)
        }


    return payload


def get_ip_address(service):
    # API endpoint URL
    if service == "products":
        return "34.148.11.51"
    elif service == "orders":
        return "34.148.161.115"
    elif service == "accounts":
        return "34.23.38.111"
    else:
        print("Not a service...")
        exit()


def main(args):

    service, method, num_users = get_arg(args)

    url = "http://{}/{}".format(get_ip_address(service), service)

    # Loop to simulate users
    for i in range(num_users):


        if method == 'post':
            headers = {'Content-Type': 'application/json'}

            payload = get_payload(service)
            # Send POST request to API
            response = requests.post(url, headers=headers, data=json.dumps(payload))
        elif method == 'get':
            id = get_id(url)
            response = requests.get('{}/{}'.format(url, id))
        elif method == 'delete':
            id = get_id(url)
            response = requests.delete('{}/{}'.format(url, id))

        # Print response status code and content
        print(f"User {i+1} - Status code: {response.status_code}, Response content: {response.content}")

        # Wait for a random time between 0.1 and 1 second before sending the next request
        time.sleep(random.uniform(0.1, 1))

def get_arg(args):
    default_service = 'products'
    default_method = 'post'
    default_n_user = 100

    parser = argparse.ArgumentParser(description='Enter arguments in lowercase')
    parser.add_argument('--service', type=str,  help='E.G products, accounts or orders,     Default: {}'.format(default_service),  required=False, default=default_service)
    parser.add_argument('--method', type=str,   help='E.G GET, POST, DELETE                 Default: {}'.format(default_method),  required=False, default=default_method)
    parser.add_argument('--user', type=int,     help='Enter the number of user to simulate  Default: {}'.format(default_n_user),  required=False, default=default_n_user)

    args = parser.parse_args()

    service = args.service.lower()
    method = args.method.lower()
    user = args.user.lower()

    return service, method, user

if __name__ == '__main__':
    main(sys.argv)
