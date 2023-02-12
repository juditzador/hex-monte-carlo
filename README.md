# hex-monte-carlo

A Monte Carlo simulator, using Gale's Algorithm to determine the winner of a
Hex game, based on the difference of the stone played on a single cell.

This is a random turn Hex game.

There are two implementations in this repository. The first was written in
Python, by [pgadey](https://github.com/pgadey). The second is written in Go,
by [nesv](https://github.com/nesv). I forked the repo from the latter's 
repository, but working with the Python version only.

The core functions are not changed, but extended to keep track of more 
variables in order to implement a new, more efficient algorithm to find 
the critical score for each cell. 

The old strategy to get the critical score map was to create $N$ random boards. 
For each random board there is a Gale winner. Then, each of the cells are flipped
individually and a new Gale winner is determined. If the winner flips from the base
case, the cell gets a point. The cell with the most points after $N$ simulations is the
pivotal (most critical) one. This requires a total of $N\times(dim \times dim+1)$ Gale algorithm
evaluation.

In the new strategy, for each random board there are only two Gale algorithm evaluations
are done. One from the top left corner ( $G1$ ), as originally, and one from the bottom
right ( $G2$ ) corner (practically achieved by rotating the board by 180 degrees). Note that the
winner is of course invariant to the start point, $w(G1)=w(G2)$, but the paths are different, $p(G1)\not =p(G2)$. 
We record the paths traveled by the Gale algorithms. More precisely, if 1 wins, 
we record the cells along the Gale path with value 1, $p(G1\mid 1)$ and $p(G2 \mid 1)$, and if 2 wins, 
we record the cells with 2, $p(G1 \mid 2)$ and $p(G2 \mid 2)$. Cells that appear in both cases, $p(G1)\cap p(G2)$,
are given a point. This way, we only need $N \times 2 \times dim$ Gale algorithm evaluations.
