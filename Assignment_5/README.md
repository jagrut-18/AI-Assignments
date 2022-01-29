# Assignment 5

## K-Nearest Neighbors Classification

### Fit method
As KNN Classification simply remembers the entire training data therefore in the fit method I just set the given X and y.

### Predict method
 - In this method, I first calculate the distance between all the test items and the train items.
 - After sorting the list based on distance, we take the first k items from the list.
 - Now based on the type of weights we make the decision.<br>
 If weights is uniform, all the neighbors are considered same. Otherwise the nearer neighbors are considered more important than the farther. For that we are using inverse of the distance.
 - At last, we make the decision based on the most votes from the neighbors.


## Multilayer Perceptron Classification

### _initialize method
Here weights and biases are initialized randomely with the appropriate shapes.

### Fit method
This method loops over the number of iterations provided and does the following:
- Does the forward pass by doing `weights * inputs + biases`
- Calculate the error which is the difference between expected and the predicted
- Then it performs gradient descent to adjust the weights and biases to reduce the error.

### Predict method
This method performs one forward pass with the updated weights and biases to predict value for the given input. Using the argmax function, we output the most probable class.

### Other functions
1. Normal and derivative versions of the activation functions are implemented.
2. Cross entropy loss is calculated using its formula and a small epsilon value is used to avoid zero division error.
3. One hot encoding: Using the unique method, a list of classes is collected. After that classes are mapped to indexes and appropriate items are marked as 1 in the table.

