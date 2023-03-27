import requests
import json
import random
import string
import time
import sys
import argparse
import threading

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

def simulate_user(method, service, url, user):
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
    print(f"User {user + 1} - Status code: {response.status_code}, Response content: {response.content}")

    # Wait for a random time between 0.1 and 1 second before sending the next request
    #time.sleep(random.uniform(0.1, 1))

def get_all(url):
    response = requests.get('{}'.format(url))
    print(f"Status code: {response.status_code}, Response content: {response.content}")
    return response

def delete_all(url):
    response = requests.delete('{}'.format(url))
    print(f"Status code: {response.status_code}, Response content: {response.content}")

def main(args):

    service, method, num_users, num_threads = get_arg(args)
    method_dic = {"post": "create new ", "get": "get all ", "delete": "delete all "}

    print("Service type:", service)
    print("Request:", method_dic[method] + service)
    print("Number of Users:", num_users)
    print("Concurrent thread:", num_threads)
    print("--------------------------------------------------------------------------------\n\n")

    url = "http://{}/{}".format(get_ip_address(service), service)

    if method == 'get all':
        get_all(url)
        exit()
    elif method == 'delete all':
        delete_all(url)
        exit()

    # Loop to simulate users
    user_id = 0
    for event in range(int(num_users / num_threads)):
        print("--------------------------------------------------------------------------------\n\n")
        threads = []
        # Loop to create threads
        for thread in range(num_threads):
            # Create thread for each user
            t = threading.Thread(target=simulate_user, args=(method, service, url, user_id,))
            threads.append(t)
            user_id = user_id + 1

        # Start all threads
        for t in threads:
            t.start()

        # Wait for all threads to finish
        for t in threads:
            t.join()

def get_arg(args):
    default_service = 'products'
    default_method = ['post']
    default_n_user = 1000
    default_num_threads = 15

    parser = argparse.ArgumentParser(description='Enter arguments in lowercase')
    parser.add_argument('--service', type=str,  help='E.G products, accounts or orders,     Default: {}'.format(default_service),  required=False, default=default_service)
    parser.add_argument('--method', type=str, nargs='+',   help='E.G get, post, delete, get all or delete all Default: {}'.format(default_method),  required=False, default=default_method)
    parser.add_argument('--user', type=int,     help='Enter the number of user to simulate  Default: {}'.format(default_n_user),  required=False, default=default_n_user)
    parser.add_argument('--threads', type=int,     help='Enter the number of threads           Default: {}'.format(default_num_threads),  required=False, default=default_num_threads)


    args = parser.parse_args()

    service = args.service.lower()
    method = ' '.join(args.method).lower()
    user = args.user
    threads = args.threads

    return service, method, user, threads

if __name__ == '__main__':
    main(sys.argv)