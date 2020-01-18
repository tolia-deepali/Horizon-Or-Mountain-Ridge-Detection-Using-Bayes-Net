## Introduction

The given problem was to find the mountain ridge. For that we were given a matrix of the image based on the color intensity of the image.

### 1.1 Task 1 - Simple:

For this we simply took the max of edge strength as P(S) will be a constant as the prior data for every row has equal chances of having ridges in it.

### 1.2 Task 2 - Map using Viterbi Algorithm

In this task we implemented viterbi algorithm. To implement this we considered the formula for Viterbi i.e.

P(Q0 = q0)􏰀 P(Qt+1 = qt+1|Qt = qt)􏰀 P(Ot|Qt = qt)

#### 1.2.1 Transition State:

Total number of transition from state j to i Number of transitions from state j

    Pij = P(Qt+1 =j|Qt =i)

        = P(Qt|Qt+1)P(Qt+1)

        P(Qt) as P(Qt+1) and P(Qt) are equal we are left with P(Qt|Qt+1)

Probability of Qt = i given Qt+1 = j
is equal to intersection of them divided by probability of number of transitions from
Qt = j


##### 1.2.2 Initial State:

    wi =P(Q0 =i)
    We assumed the initial state as edge strength matrix

##### 1.2.3 Emission State:
    Count ( observed value that are in current) + m
    -----------------------------------------------
    Count (values in observed) + mV

I.e

    ei(a) = P(Ot =a|Qt =i)

          = P(Qt=i|Ot=a)P(Ot=a)
            ------------------
            P(Qt=i)

as P(Ot) and P(Qt) are equal we are left with P(Qt|Ot)

Probability of Qt given Ot is equal to intersection of them divided by probability of number of observed values from
Ot

References: ”https://stats.stackexchange.com/questions/212961/calculating-emission-probability-values-for-hidden-markov-model-hmm”

### 1.3 Task 3 - Human Input:
For this task we accepted the human input which is x,y coordinate on the image. We assumed that the input coordinates are on the ridge of the mountain.
We split the edge strength matrix column-wise in two arrays
1. The first array we had columns range from 0 to input column - 1
2. The second array had columns from input column to the last column.
As the given coordinates are on the ridge the intensity over that pixel should be max but due to gradient in the colors of image we sometimes get max where there is no mountain ridge to avoid this we nullify all the other values in that row by assigning zero to it except for the pixel that is given as the input.
For both the arrays now we run viterbi algorithm and generate coordinates which we merge together and send as the coordinate for the ridges.

#### Code Run :
```
   ./horizon.py input_file.jpg row_coord col_coord

```
where row coord and col coord are the image row and column coordinates of the human-labeled pixel.

#### Results :
Please Find Results Doc for the Output
