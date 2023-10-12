from socket import *
import threading
import random
import json

# To use this TCP server and client with JSON: Start the server and then the client
# Then from the client, type in the JSON format {"operation": "operation", "operands": [nr1, nr2]}
# Can use 3 operations: add, subtract, random
# EXAMPLE: {"operation": "add", "operands": [10, 7]}

def handle_client(connectionSocket, address):
    print(f"Connected from IP: {address[0]}")
    keep_communicating = True

    while keep_communicating:
        request = {}

        try:
            sentence = connectionSocket.recv(1024).decode()
            request = json.loads(sentence)

            if "operation" not in request or "operands" not in request:
                response = {"error": "Invalid request. Must include 'operation' and 'operands'."}
            else:
                operation = request["operation"].lower()
                operands = request["operands"]

                if operation == "random" and len(operands) == 2:
                    first_number, second_number = operands
                    if first_number <= second_number:
                        response = {"result": random.randint(first_number, second_number)}
                    else:
                        response = {"error": "Invalid request: First number must be less than or equal to the second number"}
                elif operation == "add" and len(operands) == 2:
                    response = {"result": operands[0] + operands [1]}
                elif operation == "subtract" and len(operands) == 2:
                    response = {"result": operands[0] - operands[1]}
                else:
                    response = {"error": "Invalid request"}
        except json.JSONDecodeError:
            response = {"error": "Invalid request"}
        
        connectionSocket.send(json.dumps(response).encode())

        if request.get("operation") == "close":
            keep_communicating = False

    connectionSocket.close()

    
serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print ("Server is ready to listen")

while True:
    connectionSocket, address = serverSocket.accept()
    threading.Thread(target = handle_client, args = (connectionSocket, address)).start()