from socket import *
import json

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM) # create socket
clientSocket.connect((serverName, serverPort)) # connect to socket

while True:
    input_string = input("Write JSON input (or write 'close' to exit):")

    if input_string.strip() == "close":
        clientSocket.send(input_string.encode())
        break

    try:
        request = json.loads(input_string)
    except json.JSONDecodeError:
        print("Invalid JSON format. Check code comments for how-to.")
        continue

    if "operation" in request and "operands" in request and isinstance(request["operands"], list):
        request_json = json.dumps(request)
        clientSocket.send(request_json.encode())
    else:
        print("Invalid JSON format. Check code comments for how-to.")

    response = clientSocket.recv(1024).decode()

    try:
        response_data = json.loads(response)
        if "error" in response_data:
            print("Server response error:", response_data["error"])
        elif "result" in response_data:
            print("Server response result:", response_data["result"])
        else:
            print("Invalid response format")
    except json.JSONDecodeError:
        print("Invalid JSON response from the server")

clientSocket.close()
