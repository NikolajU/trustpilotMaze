Installation:

This program is written in python 3. It is not backwards compatible with python 2, because backwards compatibility in python is complicated.

To install dependencies for the script:

`pip3 install pathfinding`

`pip3 install requests`

`pip3 install numpy`

To run the script on windows:

`py NikolajUnderstrupMaze.py`

To run the script on windows with verbose output (printing maze every time a step is taken):

`py NikolajUnderstrupMaze.py -v`

To run the script on linux:

`py NikolajUnderstrupMaze.py`

To run the script on linux with verbose output (printing maze every time a step is taken):

`py NikolajUnderstrupMaze.py -v`


How the script works:

The script calls the API at https://ponychallenge.trustpilot.com/api-docs/index.html#/pony-challenge to instantiate a maze with random size, and get the state of the maze. 
The game is either won or lost at the instantiation. If the monster is closer to the exit than the pony, the game is lost. If the monster is further from the exit than the pony, the game is won. This is because on difficulty 10, the monster will always make the optimal move, which is to move towards the player. 

After the maze is instantiated, the script turns the data from the api, into a grid of 1s and 0s. This is because the script uses the A* pathfinding algorithm, which needs a grid of 1s and 0s. 1 describes an empty space, 0 describes an obstacle. A* then finds the path from pony to exit, and the path from monster to exit. If the game is unwinnable, the script exits, with an explanation. If the game is winnable, the script then turns the path into instructions for the api. The instructions are then sent to the api. The response is not validated because it isn't needed. The program will only fail to communicate with the api in case of internet connectivity issues. When the last instruction is sent, the game will be won, and the api response is printed. 

Architecture decision:
My goal was to make a short, lightweight script. It consists of 8 functions that are short and comprehensive. I have not created a GUI because i wanted to solve the maze problem as a backend problem. 

The test suite is run in test.py. It contains tests for all functions, except walkTowardsEnd(), which is tested by running the main() function. This is because the function requires a new maze every time to execute directions on. 
