+++
title = "GRiddle's Puzzle: Greyscale Gambit"
date = 2026-09-10
draft = false

[taxonomies]
categories = ["Puzzles", "Games"]
tags = ["blog"]

[extra]
lang = "en"
+++

[GResearch](http://gresearch.com/) is a cool company, they put up puzzles! I was trying to solve another one of their puzzles but I digressed and ended up in a whole statistical number theory area which I had no clue of. I think I lost track of the fact that it was meant to be a puzzle... but anyway. This is a different one, its called [greyscale gambit](https://www.gresearch.com/griddles/series-b-puzzle-2/).

## Question

We have been given a picture and we have a few statements that can either be true or false. Yes we need to decide which is it.

1. It is Black to move.
2. One colour has exactly one more piece than the other.
3. The two rooks are of different colours.
4. No piece is on a square that matches its own colour.
5. There is a knight that is not threatened by any pawn.
6. There is a pawn that is threatened by a king.
7. Promotions have occurred in this game.
8. All knights are the same colour.
9. No bishop is protected by a knight.
10. Every piece has been moved in this game.
11. There is a bishop that threatens a king.

> Either all statements are true or all statements are false

Another thing we need to sort before coming to the question is the orientation of the board. We don't know that as well. So once we figure that out, we need to see who wins White or Black.

## Solving

The path is pretty straight forward, we'll pick up the four possible orientations and try to satisfy (or not) the rules above and see if anything blows up. Right now I am assuming that the statements are true.

First let's look at the base case and try to reason about the statements.

> Note: We'll be assuming White is below and Black is above

{{ figure(src="assets/BaseBase_case_non_rotated.png", alt="The base case provided", caption="The base case provided with no knowledge of orientation or colors") }}

Since the statements are true, we have `P3` telling us that the two Rooks (**R**) are of different colors and `P4` telling us that no piece is on a square that matches its own color. In the board, no matter what orientation we pick, the two rooks will always be on the same colored square. So, according to `P4` they should be of the same colors (if they're both in the **Black square**, they they both should be **White** and vice-versa). But that contradicts with `P3`!

In fact, there is no resolution to this. This means that either one of P3 or P4 is false. But since we know that either all the statements are true or false, this leads to the conclusion that:

> All the statements are false

We'll be using the negation of these statements henceforth:

1. It is White to move.
2. One colour does not have exactly one more piece than the other.
3. The two rooks are of the same colours.
4. pieces can be on a square that matches its own colour.
5. There is no knight that is not threatened by any pawn.
6. There is no pawn that is threatened by a king.
7. Promotions have not occurred in this game.
8. All knights are different colours.
9. At least one bishop is protected by a knight.
10. Not every piece has been moved in this game.
11. There is no bishop that threatens a king.

If we try to apply these to the base case, we eventually get to this point:

{{ figure(src="assets/non_rotated_base_case.png", alt="The base case with annotations", caption="The base case with colored annotations following the rules") }}

The thinking behind this setup is as follows:

1. We have two Knight, one must be White and one must be Black
2. Only one bishop can be protected by a Knight, so both of those must be the same color (White here).
3. No bishop should threaten the kind, hence the king next to White Bishop must be White and next to the Black one must be Black.
4. The only peices that could possible not have moved are the White Pawns in the 2nd row from the bottom. So, atleast one of them should be White (I've used both White but as we'll see it won't make a difference)
5. Since the King doesn't threaten any Pawns, the 2 Pawns next to the White King should be White and the one Pawn next to the Black King should be Black.

Now here's the problem. Once we arrive at 5, the Pawn in the White's last row must have been promoted since Pawns can't live there without it. That contradicts `~P7`.

If we switch colors, make every White piece Black and so on, we'll see that it breaks `~P5` since the White Knight now won't be threatened by any Pawn.

Hence, this orientation will not work.

### Rotate CW by 90 degrees

{{ figure(src="assets/90_degress_CW.png", alt="90 degrees CW rotated case", caption="The 90 degrees CW rotated case with colored annotations following the rules") }}

We follow the same procedure as before, and everything checks out almost exactly right. Almost. Note that we applied `~P2` here as well, which forced the two Rooks to be the same color and White. This tipped the number of White pieces to 8 and Black pieces to 5. Since two Bishops are still un-colored, and we have 4 in the game with no promotions, one of them must be White and one must be Black. So the total number of `White pieces > Black pieces + 1`. Hence `~P2` was satisfied.

Anyway, the issue here is again `~P5`. In this case, the diagram shows the White Knight in the rightmost column not being threatned by any Pawn.

This time we CANNOT flip the colors, because of `~P10`, since the only piece which could have possibly stated in its own place the entire game is the White pawn in row 2 from the bottom. So, it must be White. And hence we have a **contradiction**.

### Rotate CW by 180 degrees

{{ figure(src="assets/180_degress_CW.png", alt="180 degrees CW rotated case", caption="The 180 degrees CW rotated case with colored annotations following the rules") }}

Again following the same procedure as before, we again see a contradiction between `~P5` and `~P7`, that both cannot be true at the same time. Try it out!

### Rotate CW by 270 degrees

{{ figure(src="assets/270_degress_CW.png", alt="270 degrees CW rotated case", caption="The 270 degrees CW rotated case with colored annotations following the rules") }}

Following the same procedure here we easily get away without any contradictions. We're forced to choose the two Rooks to be Black due to `~P2`, and we still don't have a confirmation on which bishop is what color of the two pink ones.

So this is the image we'll be talking about going forward. This is the current state of the game, with White below and Black above the board.

## Who wins?

Since we have two bishops which can be assigned any color (albeit one black and one white), let's try out both permutations and see what we get.

### Permutation 1

{{ figure(src="assets/P1.png", alt="First permutation for the Bishops", caption="First permutation for the Bishops") }}

So, since the White King is under a check, we'll have to kill the Black Knight with the White Pawn (its White's move remember). This opens up the White Bishop to check the Black King and that is taken by the Black Rook.

Now the game can proceed in many directions so I am not 100% sure if this is the right permutation for a puzzle. Hence, even though its a very valid state for the game, I'll discard this.

### Permutation 2

{{ figure(src="assets/P2.png", alt="Second permutation for the Bishops", caption="Second permutation for the Bishops") }}

This leads to a clear victor, since after taking the Black Knight, the Black Rook checks the White King and its game over.

> Therefore I'll be choosing the Permutation 2

And hence the final state of the board looks like:

{{ figure(src="assets/final_board_state.png", alt="Final board state after Black checkmate", caption="Final board state after Black checkmate") }}

---