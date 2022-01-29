#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Jagrut Dhirajkumar Chaudhari - jagchau@iu.edu
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys
from queue import PriorityQueue

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# This function returns 'U' -> Up, 'D' -> Down, 'L' -> Left, 'R' -> Right
def getPathString(pt1, pt2):
        if pt1[0] == pt2[0]:
                if pt1[1] > pt2[1]:
                        return 'L'
                else:
                        return 'R'
        if pt1[1] == pt2[1]:
                if pt1[0] > pt2[0]:
                        return 'U'
                else:
                        return 'D'

def calculate_manhatten(pt1, pt2):
  return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])
 
# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        # Find goal position
        goal_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        
        fringe_queue = PriorityQueue()
        fringe_queue.put((0, pichu_loc, ''))
        visited_moves = [pichu_loc]

        while not fringe_queue.empty():
                (total_cost, curr_move, path) = fringe_queue.get()
                for move in moves(house_map, *curr_move):
                        if move not in visited_moves:
                                visited_moves.append(move)
                                if house_map[move[0]][move[1]]=="@":
                                        return (len(path) + 1, path + getPathString(curr_move, move))
                                else:
                                        path_string = path + getPathString(curr_move, move)
                                        current_cost = len(path_string)
                                        heuristic = calculate_manhatten(goal_loc, move)
                                        fringe_queue.put(((current_cost + heuristic), move, path_string))
                return (-1, '')

                                

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

