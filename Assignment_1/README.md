# Assignment 1

# Route Pichu: Path finding using AI

<b>Description:</b><br/>
Firstly, I executed the program that was already provided, to understand why it was going in infinite loop. Looking at the output I quickly figured out that the problem was revisiting the nodes.

Therefore I had to do two tasks.
1. Implement visited nodes array
2. Calculate path based on direction ('U', 'D', 'L', 'R')

To do the first task:
> Created a visited_moves array with pichu_loc as first item in it.
> For every move, I checked whether it is already visited or not. If visited, ignore it. Otherwise check for goal state or append to fringe.

For the second task:
> I changed the fringe tuple from `(move, distance)` to `(move, path_string)`. I calculated the distance using the length of that path string.
> Also, built a function to classify a move into one of these `'U', 'D', 'L', 'R'`. Using this function I append the path string with one of the character for each move.

After reaching to the goal state, the program returns the `distance` and `path string` from start to the end.

## Optimisation
### 1. Adding Heuristic
> In the above method I described, I did not use any heuristic value and performed an uninformed search. It was giving an optimal solution but may be taking more time as compared to informed search.<br/><br/>
>So I added heuristic in the algorithm. For that I used manhatten distance and created a function `calculate_manhatten` that calculates the manhatten distance between two points.<br/><br/>
### 2. Calculating heuristic
> Here priority of a state is calculated by adding the currently travelled distance and heuristic to reach the goal. The state with least value will be considered first using the priority queue.
### 3. Using priority queue
> For poping the most promising state I used a priority queue. Each element of priority queue is tuple of `(heuristic, move, path_string)`. Therefore, the state with the least heuristic is explored first.



# Arrange Pichus: Hiding agents from each other

1. <b>State space</b><br/>
All the possible combination of places where pichu can be placed.
2. <b>Initial state</b><br/>
The state given as input here
3. <b>Goal state</b><br/>
Goal state has k number of pichus from which none are in same row, column or diagonal.
4. <b>Successor function</b><br/>
To generate new house_maps by adding a pichu at all possible places from a given state.
5. <b>Cost function</b><br/>
There is no cost involved between states here.


<b>Description:</b><br/>
The `successors` function returns all the possible states by adding pichus in the empty places. But it does not check for the validity of the location. So I created a function called `validate_loc` which checks whether the pichu at that location is visible to others or not.

`validate_loc` explanation:
> Check in the all the eight directions:<br/>
>1. if we find a pichu directly then return `False`<br/>
>2. if we find wall or @, stop finding in that direction<br/>
>3. otherwise keep looking in the remaining directions<br/>
>4. Atlast, return `True` if we no pichu found in the way

Also created a `is_in_bound` function to check whether a point `(x, y)` is in the map or not.

I used these functions in `is_goal` function, which was just checking the count of pichus earlier, to validate the map entirely.
