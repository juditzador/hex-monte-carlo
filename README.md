# hex-monte-carlo

A Monte Carlo simulator, using Gale's Algorithm to determine the winner of a
Hex game, based on the difference of the stone played on a single cell.

This is a random turn Hex game.

There are two implementations in this repository. The first was written in
Python, by [pgadey](https://github.com/pgadey). The second is written in Go,
by [nesv](https://github.com/nesv). I forked the repo from the 
repository of nesv, which contains both. I am working with the Python version only.

The core functions are not changed, but extended to keep track of more 
variables in order to implement a new, more efficient algorithm to find 
the critical score for each cell. The cell with the highest score is the 
pivotal one.

The simplest strategy to get the critical score map is to create $N$ random boards. 
For each random board there is a winner $w$, which is only dependent on the board's state $B$,
and is found by the path $G$ that is 
taken according to the Gale algorithm, i.e., $w(B)=G(B)$. Then, each of the cells are flipped
individually, creating a new board, $B'$, which only differs in once cell from $B$.
The new Gale winner is determined, $w(B')=G(B')$. If the winner flips from the base
case, $w(B) \not = w(B')$, the cell gets a point. The cell with the most points after $N$ simulations is the
pivotal (most critical) one. This strategy requires a total of $N\times(dim \times dim+1)$ Gale algorithm
evaluation, where $dim$ is the dimension of the board.

In the new strategy, for each random board there are only two Gale algorithm evaluations. 
One from the top left corner, $G1$, as originally, and one from the bottom
right corner, $G2$. The latter is practically achieved by rotating the board by 180 degrees in the code. The
winner is of course invariant to the starting point, $w(B)=G1(B)=G2(B)$, but the paths are different, $p(G1(B))\not =p(G2(B))$. 
We record the paths traveled by the Gale algorithms. More precisely, if player 1 wins, 
we record the cells along the Gale path with value 1, $p(G1(B)\mid 1)$ and $p(G2(B) \mid 1)$, and if player 2 wins, 
we record the cells with 2, $p(G1(B) \mid 2)$ and $p(G2(B) \mid 2)$. Cells that appear in both cases, $p(G1(B) \mid x)\cap p(G2(B)\mid x)$, 
$x={1, 2}$,
are given a point. This way, we only need $N \times 2 \times dim$ Gale algorithm evaluations.

Finally, our goal is to play a compound game. The the first game, consisting of $N$ random boards, 
we determine the pivotal point, $P1$, and 
fix it to 1 or 2 by a coin flip. In all subsequent games this cell is fixed to this value, 1 or 2. In the 
next game, we determine the pivotal point from the rest of the points on this new board, $B(P1=fix)$, 
and fix the pivot to a coin flip value for all subsequent games. The next game is played on 
$B(P1=fix, P2=fix)$, and we continue this process
until there the fixed points themselves
form a finished game scenario. 

This is a project with my husband, [Alan](https://math.berkeley.edu/~alanmh/).
