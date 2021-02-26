from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import math
import requests
import numpy
import random

def to_matrix(l, n): # this function turns a 1D list into a 2D list, so it is easier to work with.
	return [l[i:i+n] for i in range(0, len(l), n)]

def generateLocalMaze(gameState): # this function takes the maze data from the api and turns it into a grid of 0s and 1s. 1 represents a free square and 0 represents an obstacle. The grid is gamesize * 2 + 1 in size.
	mazeGrid = [] # this list will contain the maze. 
	XYmaze = to_matrix(gameState["data"], gameState["size"][0]) # this turns the api data into a 2D list
	for y in XYmaze: # this iterates on the maze vertically
		xGrid = [[0],[]] # this list contains the layer above and the current layer.
		for x in y: # this iterates on the maze horizontally
			if "north" in x:
				xGrid[0].append(0)
			else:
				xGrid[0].append(1)
			if "west" in x:
				xGrid[1].append(0)
			else:
				xGrid[1].append(1)
			
			xGrid[0].append(0)
			xGrid[1].append(1)

		xGrid[1].append(0)
		mazeGrid.append(xGrid[0])
		mazeGrid.append(xGrid[1])

	mazeGrid.append([0] * len(xGrid[0]))
	return mazeGrid

def findLocation(point, mazeSize): # this function converts the location integer from the api, to coordinates for the mazegrid.
	x = point % mazeSize[0] * 2  + 1 # the size of the mazeGrid is x2 + 1
	y = math.floor(point/mazeSize[0]) * 2 + 1
	return x,y

def instantiateMaze(x, y, difficulty): # this function creates a new game and returns the game information
	urlNewGame = "https://ponychallenge.trustpilot.com/pony-challenge/maze"
	postData = {
		"maze-width": x,
		"maze-height": y,
		"maze-player-name": "spike",
		"difficulty": difficulty
	}
	r = requests.post(urlNewGame, json=postData).json()

	print("maze initiated with size {}x, {}y and maze_id {}".format(x, y, r["maze_id"]))

	urlState = "https://ponychallenge.trustpilot.com/pony-challenge/maze/{}".format(r["maze_id"])
	return requests.get(urlState).json()


def pathToInstructions(path): # this functino turns the path from a list of tuples into a list of directions for the api. 
	directionDict = {"0,2":"north", "0,-2":"south", "2,0":"west", "-2,0":"east"} # This converts tuple math to directions.
	directions = []
	for i in range(0,len(path)-2,2): # the maze in the script, is twice as big as what the api expects, so i use i+=2.
		difference = numpy.subtract(path[i], path[i+2])
		directions.append(directionDict["{},{}".format(difference[0], difference[1])])
	return directions

def walkTowardsExit(gameState, directions): # this function tells the api to move the pony. 
	print("Game is winnable. Executing api calls.")
	urlWalk = 'https://ponychallenge.trustpilot.com/pony-challenge/maze/{}'.format(gameState["maze_id"])

	for i in directions:
		r = requests.post(urlWalk, json={"direction":i}).json()

	print(r)

def findPaths(mazeGrid, gameState): # this function uses the pathfinding library to create paths from the mazeGrid and the gamestate. 
	finder = AStarFinder() # A* is chosen because it is the default pathfinding algorithm. 
	grid = Grid(matrix=mazeGrid)

	ponyX,ponyY = findLocation(gameState["pony"][0], gameState["size"])
	domoX,domoY = findLocation(gameState["domokun"][0], gameState["size"])
	endX,endY = findLocation(gameState["end-point"][0], gameState["size"])

	pony = grid.node(ponyX,ponyY)
	domo = grid.node(domoX,domoY)
	end = grid.node(endX,endY)

	path, runs = finder.find_path(pony, end, grid)
	grid.cleanup()
	pathDomoToEnd, runs2 = finder.find_path(pony, domo, grid)

	print(grid.grid_str(path=path, start=pony, end=end))
	legend = {"#":"obstacle","x":"path","s":"start","e":"end"}
	print("legend: ", legend)

	return path, pathDomoToEnd

def main(): # this function creates a maze game and completes it.
	gameSize = [random.randint(15,25), random.randint(15,25)]
	difficulty = 10

	gameState = instantiateMaze(gameSize[0], gameSize[1], difficulty)
	mazeGrid = generateLocalMaze(gameState)
	path, pathDomoToEnd = findPaths(mazeGrid, gameState)
	directions = pathToInstructions(path)
	directionsDomoToEnd = pathToInstructions(pathDomoToEnd)

	print("Distance to end = {} | Distance from domo to end = {}".format(len(directions), len(directionsDomoToEnd)))

	if (len(directions) > len(directionsDomoToEnd)):
		print("Game is unwinnable, exitting script.")
		exit()

	walkTowardsExit(gameState, directions)

if __name__ == "__main__":
	main()