''' TCPServer.py
usage: python3 TCPServer.py PORT
Note that you type python3 on CSCE server.
Reads in text, changes all letters to uppercase, and returns
the text to the client
Modified by Dale R. Thompson
10/12/17 converted to Python 3
'''

import sys
import json

# Import socket library
from socket import *

def letterPositions(word):
    positions = {}

    for i, letter in enumerate(word):
        if letter not in positions:
            positions[letter] = []
        positions[letter].append(i)

    return positions

# Set port number by converting argument string to integer
# If no arguments set a default port number
# Defaults
if sys.argv.__len__() != 2:
    serverPort = 5555
# Get port number from command line
else:
    serverPort = int(sys.argv[1])

# Choose SOCK_STREAM, which is TCP
# This is a welcome socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# The SO_REUSEADDR flag tells the kernel to reuse a local socket
# in TIME_WAIT state, without waiting for its natural timeout to expire.
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Start listening on specified port
serverSocket.bind(('', serverPort))

# Listener begins listening
serverSocket.listen(1)

print("The server is ready to receive")

# Wait for connection and create a new socket
# It blocks here waiting for connection
connectionSocket, addr = serverSocket.accept()

word = 'arkansas'

# Forever, read in sentence, convert to uppercase, and send
while True:

    # Read bytes from socket
    letter = connectionSocket.recv(1024)
    
    if not letter:
        break
    
    letterString = letter.decode('utf-8')
    
    if letterString in word:
        reply = 'Correct'
        correctPositions = letterPositions(word)[letterString]
    else:
        reply = 'Incorrect'
        correctPositions = []
  
    replyBytes = reply.encode('utf-8')
    # Send it into established connection
    connectionSocket.send(replyBytes)
    
    correctPositionsBytes = json.dumps(correctPositions).encode('utf-8')
    connectionSocket.send(correctPositionsBytes)
