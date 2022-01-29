#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Jagrut Dhirajkumar Chaudhari - jagchau@iu.edu
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys


# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line]
                for line in f.read().rstrip("\n").split("\n")][3:]


# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([row.count('p') for row in house_map])


# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])


# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [
        house_map[row][0:col] + [
            'p',
        ] + house_map[row][col + 1:]
    ] + house_map[row + 1:]


# Get list of successors of given house_map state
def successors(house_map):
    return [
        add_pichu(house_map, r, c) for r in range(0, len(house_map))
        for c in range(0, len(house_map[0])) if house_map[r][c] == '.'
    ]


#Check whether location is in the bound
def is_in_bound(house_map, loc):
    limit = (len(house_map) - 1, len(house_map[0]) - 1)
    return all(x >= 0 for x in loc) and all(x <= y for x, y in zip(loc, limit))


# Check whether agent is visible to other agents
def validate_loc(house_map, row, col):
    inc = 1

    # Indexes with True value will be checked and indexes with False will not be checked
    # This list has 8 values, representing 8 directions
    indexes_to_check = [True for i in range(8)] 

    while True:
        # These are the 8 directions
        locations = [(row - inc, col), (row, col - inc), (row + inc, col),
                     (row, col + inc), (row + inc, col + inc),
                     (row - inc, col - inc), (row - inc, col + inc),
                     (row + inc, col - inc)]

        for i, is_true in enumerate(indexes_to_check):
            if is_true:
                loc = locations[i]
                if is_in_bound(house_map, loc):
                    item = house_map[loc[0]][loc[1]]
                    if item == 'p':
                        return False
                    if item in 'X@':
                        indexes_to_check[i] = False #Setting False because no need to check in this direction
                else:
                    indexes_to_check[i] = False
        if not any(indexes_to_check):
          return True
        inc += 1


# check if house_map is a goal state
def is_goal(house_map, k):
    if count_pichus(house_map) != k:
        return False
    pichu_locations = [(row_i, col_i) for col_i in range(len(house_map[0]))
                       for row_i in range(len(house_map))
                       if house_map[row_i][col_i] == "p"]
    for pichu_loc in pichu_locations:
        if not validate_loc(house_map, pichu_loc[0], pichu_loc[1]):
            return False # Return False if any pichu_location is not valid
    return True


# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map, k):
    fringe = [initial_house_map]
    count = 0
    visited = []
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):
            count += 1
            if new_house_map not in visited:
                visited.append(new_house_map)
                if is_goal(new_house_map, k):
                    return (new_house_map, True)
                if count_pichus(new_house_map) < k:
                    fringe.append(new_house_map)
    return ([], False)


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print("Starting from initial house map:\n" +
          printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map, k)
    print("Here's what we found:")
    print(printable_house_map(solution[0]) if solution[1] else "False")
