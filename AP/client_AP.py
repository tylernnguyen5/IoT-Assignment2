#!/usr/bin/env python3

import socket
import requests

HOST = input("Enter IP address of server: ")

# HOST = "0.0.0.0"    # The server's hostname or IP address
PORT = 5000         # The port used by the server
ADDRESS = (HOST, PORT)

def credentialsCheck():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to {}...".format(ADDRESS))
        s.connect(ADDRESS)
        print("Connected.")

        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if(not username or not password): # if blank input, will break the loop
                break
            
            # Send credentials 
            credentials = "{} {}".format(username, password)
            s.sendall(credentials.encode())


            # Receive data, which is a user ID if validated
            data = s.recv(4096) # 4096 is the buffersize
            print("Received {} bytes of data decoded to: '{}'".format(  len(data), 
                                                                        data.decode()))
            return data.decode()
        
        print("Disconnecting from server.")
    print("Done.")


def unlockCar(user_id, car_id, begin_time):
    data = {
        'user_id'   : user_id,
        'car_id'    : car_id,
        'begin_time': begin_time   
    }

    # Send a request to Flask API
    response = requests.put("http://{}:{}/car/unlock".format(HOST, PORT), data)


    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False


def lockCar(user_id, car_id):
    data = {
        'user_id'   : user_id,
        'car_id'    : car_id
    }

    # Send a request to Flask API
    response = requests.put("http://{}:{}/car/lock".format(HOST, PORT), data)


    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False