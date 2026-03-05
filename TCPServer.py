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

# creates an object with the set of letters and their positions in the word
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

while True:
    
    # Wait for connection and create a new socket
    # It blocks here waiting for connection
    connectionSocket, addr = serverSocket.accept()

    # game variables
    word = 'arkansas'
    numGuesses = 0
    maxGuesses = 7
    gameOver = False
    positionMap = letterPositions(word)
    correctLetters = set()
    incorrectLetters = set()

    # use newline-delimited JSON to make it easier to send bundled information
    # like positions and game status
    sockfile = connectionSocket.makefile("rwb")

    # Forever, read in sentence
    while True:

        # read bytes from socket
        line = sockfile.readline()
        if not line:
            break
        
        letter = line.decode('utf-8').strip().lower()
        
        # validate letter
        if len(letter) != 1 or not letter.isalpha():
            payload = {
                "result": "Invalid",
                "positions": [],
                "guessesUsed": numGuesses,
                "gameOver": False,
                "win": False,
                "message": "Please guess a single letter (a-z)."
            }
            sockfile.write((json.dumps(payload) + "\n").encode("utf-8"))
            sockfile.flush()
            continue

        # if the letter is in the word - send the positions so the client can fill it in
        if letter in word:
            result = "Correct"
            positions = positionMap[letter]
            # add the letter to the set of correctly guessed letters
            correctLetters.add(letter)
        elif letter in incorrectLetters:
            # update the client but don't increment numGuesses
            result = "Already guessed"
            positions = []
        else:
            result = "Incorrect"
            positions = []
            # count the guess if incorrect
            numGuesses += 1
            incorrectLetters.add(letter)

        # win condition is met when we can spell the word using the correctly guessed letters
        win = set(word).issubset(correctLetters)
        gameOver = win or (numGuesses >= maxGuesses)

        # create the payload with all the information that the client needs
        payload = {
            "result": result,
            "positions": positions,
            "guessesUsed": numGuesses,
            "gameOver": gameOver,
            "win": win,
            "word": word
        }

        sockfile.write((json.dumps(payload) + "\n").encode("utf-8"))
        sockfile.flush()
        
        if gameOver:
            break
    try:
        sockfile.close()
    except:
        pass
    connectionSocket.close()
    print("Client disconnected")