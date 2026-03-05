''' TCPClient.py
usage: python TCPClient.py HOSTNAMEorIP PORT
Reads text from user, sends to server, and prints answer
Modified by Dale R. Thompson
10/12/17 modified for Python 3
'''

import sys
import json

# Import socket library
from socket import *

# Set hostname or IP address from command line or default to localhost
# Set port number by converting argument string to integer or use default
# Use defaults
if sys.argv.__len__() != 3:
    serverName = 'localhost'
    serverPort = 5555
# Get from command line
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

# Choose SOCK_STREAM, which is TCP
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to server using hostname/IP and port
clientSocket.connect((serverName, serverPort))

# newline-delimited
sockfile = clientSocket.makefile("rwb")

print("Welcome to HANGMAN!")

wordLength = 8
wordLines = ["_"] * wordLength

while True:
    print(" ".join(wordLines))
    letter = input("Please enter a letter: ").strip().lower()

    if len(letter) != 1 or not letter.isalpha():
        print("Please enter a single letter (a-z).")
        continue

    # Send guess + newline so the server can readline()
    sockfile.write((letter + "\n").encode("utf-8"))
    sockfile.flush()
    
    # Receive JSON message 
    line = sockfile.readline()
    if not line:
        print("Server disconnected.")
        break
    
    msg = json.loads(line.decode("utf-8"))

    # if result returns invalid, print the associated message
    if msg.get("result") == "Invalid":
        print("From Server:", msg.get("message"))
        continue

    # get the game information from the server
    result = msg["result"]
    positions = msg["positions"]
    guessesUsed = msg["guessesUsed"]
    gameOver = msg["gameOver"]
    win = msg["win"]
    word = msg["word"]

    # print the result and guess count
    print(f"From Server: {result}")
    print(f"Incorrect guesses: {guessesUsed} / 7")

    # fill in the blanks with correct letters
    if result.lower() == "correct":
        for index in positions:
            if 0 <= index < wordLength:
                wordLines[index] = letter

    # win condition from server
    if win:
        print("\n" + " ".join(wordLines))
        print("You won!")
        break

    if gameOver:
        print("\nGame over — out of guesses.")
        print("The word was:", word)
        break
