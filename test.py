import NikolajUnderstrupMaze as n
import pprint as pp

def test1():
	assert n.toMatrix([],1) == []
	assert n.toMatrix([1],1) == [[1]]
	assert n.toMatrix([1,1],1) == [[1],[1]]
	assert n.toMatrix([1,3,2],2) == [[1,3],[2]]
	assert n.toMatrix([1,3,2],3) == [[1,3,2]]

def test2():
	assert n.instantiateMaze(15,15,10)["game-state"] == {'state': 'Active', 'state-result': 'Successfully created'}
	assert n.instantiateMaze(25,15,10)["game-state"] == {'state': 'Active', 'state-result': 'Successfully created'}
	assert n.instantiateMaze(15,25,10)["game-state"] == {'state': 'Active', 'state-result': 'Successfully created'}
	assert n.instantiateMaze(25,25,10)["game-state"] == {'state': 'Active', 'state-result': 'Successfully created'}

def test3():
	tinyGameState = {
	"data": [
		["west", "north"], ["west","north"],["north"],
		["west"], [], ["west"]
	],
	"size": [3,-9000]
	}
	assert n.generateLocalMaze(tinyGameState) == [[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1, 0], [0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
	assert len(n.generateLocalMaze(n.instantiateMaze(15,25,10))) == 51
	assert len(n.generateLocalMaze(n.instantiateMaze(25,15,10))) == 31

def test4():
	tinyGameState = {
	"data": [
		["west", "north"], ["west","north"],["north"],["west"],
		["west"], [], ["west"],["west"],
		["north"], ["north"], ["north"],[]
	],
	"size": [3,2],
	"pony": [0],
	"end-point": [3],
	"domokun": [1]
	}
	tinyMazeGrid = [[0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1, 0], [0, 1, 1, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]]
	assert n.findPaths(tinyMazeGrid, tinyGameState) == ([(1, 1), (1, 2), (1, 3)], [(3, 1), (3, 2), (3, 3), (2, 3), (1, 3)])

def test5():
	assert n.pathToInstructions([(1, 1), (1, 2), (1, 3)]) == ["south"]
	assert n.pathToInstructions([(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]) == ['south', 'east', 'north']

def test6():
	assert n.findLocation(0,[3,2]) == (1,1)
	assert n.findLocation(1,[3,2]) == (3,1)
	assert n.findLocation(2,[3,2]) == (5,1)
	assert n.findLocation(3,[3,2]) == (1,3)
	assert n.findLocation(4,[3,2]) == (3,3)

def test7():
	try:
		n.main()
	except Exception as e:
		print(e)

def testSuite():
	test1()
	test2()
	test3()
	test4()
	test5()
	test6()
	test7()

testSuite()