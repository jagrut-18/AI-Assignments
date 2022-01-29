# Assignment 3

# Raichu Board Game - Minimax implementation with Alpha-beta pruning

The problem is similar to chess and can be used as a basis further enhancement. To solve this problem, we used minimax algorithm with alpha-beta pruning. We fixed the maximum depth to 3 since anything greater than that resulted in code taking a long time to give meaningful results (or any result at all).

An enhancement we made to the running time was using `yield` and `itertools` to generate successors since this would create successor states lazily and reduce computation in case states don't need to be explored due to pruning.

For the heuristic, we assigned importance values to each of the pieces which we then used to calculate a score for ourselves and the opponent. We then subtract these scores and return the value as heuristic.

### References

1. https://www.youtube.com/watch?v=-ivz8yJ4l4E&t=105s
2. https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

No code was copied from the references.


## AI Review Classifier - Detecting deceptive reviews using Naive Bayes Classifier

To create the Naive Bayes Classifier for these user-generated reviews, we have done the following steps:<br>
1. Separated truthful and deceptives in different lists.
2. For every word of a truthful or deceptive review, we calcuate the probability using the below equation.<br>
> `p = frequency of word in a class / total words in a class` <br>
We also used <b>smoothing</b> to overcome new words problem. Therefore the probability equation after smoothing is below. <br>
> `p = (frequency of word in a class + alpha) / total words in a class` <br>
Here we have used alpha = 1
3. Then we calculated prior probabilities using the below equation.
> `prior = total words in one class / total words in all classes`
4. To improve the accuracy, instead of directly multiplying the probabilites we summation of `log` values.
5. We have also ignored stop words to increase the accuracy as they do not provide any relavant information.

Using all the learned probabilities, we calculate the probability of a given review being truthful or deceptive, and decision is made based on the probability value.
> If P(review/truthful) >= P(review/deceptive) then truthful else deceptive
