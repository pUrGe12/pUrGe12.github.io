+++
title = "The false - Card variant for Liar's Dice"
date = 2026-08-03
draft = false

[taxonomies]
categories = ["Games", "Math"]
tags = ["blog"]

[extra]
lang = "en"
+++

## Introduction

I was watching some clips on YouTube of Pirates of the Carribean and the scene where Davy Jones plays against Will Turner the dice game got me thinking. So, naturally I wanted to understand how the fuck the game even works because the movie's cut for this scene does an absoulute jackshit job of explaining it. I found some YouTube videos to explain the game and I won't explain that here but I'll [link the video](https://youtu.be/T44LuxdH0iw?si=2B5FIfzB6kQPapCQ) so that you can see for yourself.

Now I only have a deck of cards, and 0 dies, which means I had to come up with a variant for Liar's Dice that I can play with my friends using cards. 

> The major difference between dies and cards is that cards have dependent events

In a typical liar's dice game, you can roll any number you want, but it doesn't necessarily pin down or give you any information about what the other player might have. In cards however, such is not the case. Because if you see 3 6's in your hand, then you're damn sure only 1 more exists in the entire deck, so your betting strategy will change. Anyways, I am getting ahead of myself here, let me explain the rules a little more precisely.

## Rules

This is a 3 player game only with 1 standard card deck.

Each player gets 5 cards out of a standard 52 card deck.

The cards are ordered in the following Increasing face value:

```
F={H<N<2<3<4<5<6}
```
Where,

```
H = {10, J, Q, K, A}
N = {7, 8, 9}
```

> Note: This ordering is taken from the hi-lo card counting method in blackjack

The game starts from the dealer who bids on the possibility of there being X number of cards belonging to a particular face in F in the entire table. Game goes in counter-clockwise direction (direction flips after each round) and each subsequent player can do either of the following things:

1. Up the bid (rules for that are described below)
2. Fold (Lose the bid to the previous bidder)
3. Call the bluff

Calling bluff can only be done on the previous bidder and NOT anyone in the table. (A variation of this game can be calling bluff by anyone)

The game goes on until someone calls bluff.

### Calling Bluff

In the event of a bluff call, each player must show their hands and either of the following events can occur:

1. The callee (bidder) claims X of a face. Actual on table = A. Tolerance T = ⌈0.10 × X⌉.
2. A + T < X -> callee loses (reality plus tolerance still can't reach the bid — overbid).
3. A ≥ X + T but A ≠ X -> callee wins (bid falls within tolerance).
4. A = X -> callee wins double*.

The double victory is on the BET size made during the last bid by the callee (if that was the table minimum, then the caller must pay the callee the table minimum * 2, if it was x, then the caller pays 2x to the callee).

This effectively means that within a count of 10, one can get 1 card wrong and still win it, within a count of 20 (10-20), they can get 2 cards wrong and so on.

### Betting

Betting takes place through chips, and there are 4 rules for upping the bid. There are no minimum or maximum bets, but there is a minimum raise for each new bid, which can be pre-decided. The rules for upping the bid are:

1. Go higher in the face value but lower in the count (e.g. if the previous bid was “There exists 7 H (high cards) in the table” then your next bid can be “There exists 3 N (neutrals) in the table”)
2. Go higher in the count but keep the same face value (e.g. if the previous bid was “There exists 7 H (high cards) in the table” then your next bid can be “There exists 10 H (high cards) in the table”)
3. Go higher in the count but lower in the face value (e.g. if the previous bid was “There exists 7 4s in the table” then your next bid can be “There exists 10 N (neutrals) in the table”)
4. Go higher in both face value and count (e.g. if the previous bid was “There exists 7 H (high cards) in the table” then your next bid can be “There exists 10 N (neutrals) in the table”)

A player CANNOT bid:

1. Lower in the face value AND lower in the count
2. Lower in the count AND keep the same face value
3. Same count AND lower face
4. Same count AND same face

> Which means they can only lower the count if they climb up in the face value.

Each bid must be followed by either throwing the table minimum or more in the pot. This is the second bluff in the game. The money you throw dictates how sure you are. At the call of the bluff, the callee or the caller wins the pot.

## Analysis

Now, a game by itself is not very useful. We need to run some calculations to establish some baselines and understand the risks and rewards in the game. If we see the basic numbers first, then a few things immediately stand out:

1. There are **20 H cards**, **15 total cards** are dealt, which means on average in the table, there are (20/52) * 15 ~ **6 H cards**. Thus, any bid more **than 6 H is a risk** (in the default sense) and **less than 6 H is a safe** bet.

2. There are 12 N cards, 15 cards are dealt, which means on average in the table, there are (12/52) * 15 ~ 3.5 N cards. So, a bid more than 4 N is a risky bid and less than 3 is a safe bid.

3. For each of the numbered cards till 6, we have 4 of each which means (4/52) * 12 ~ 0.9. That means even bidding on 1 numbered card till 6 is a risky bid.

These numbers don't paint the most beautiful picture of the game, because it looks like the majority of the game is going to be within H and N cards only. So why not group the remaining cards into a different set L? I'll explore that later. Let's first look at some simulations.

### Sims

I ran some monte-carlo sims to understand the game nuances. I'll attach the more important graphs and plots here. To begin with we'll be assuming a 3 player 5 card 1 deck game and we'll assign a certain persona to each person. These persona's toggle 4 different axises:

1. `Truthfulness` - how closely opening/raising bids track the player's own expected count (1.0 = bids exactly its estimate, 0.0 = bids are unrelated to belief).
2. `Bluffing` - propensity to inflate a bid beyond what belief supports (0.0 = never pad the count, 1.0 = pad aggressively).
3. `Calling` - trigger-happiness on calling the previous bidder's bluff (0.0 = almost never call, 1.0 = call on the slightest doubt).
4. `Raising` - drive to keep pushing the bid up toward a target level rather than fold (0.0 = folds readily, 1.0 = raises whenever a legal raise exists and the target isn't yet reached).
5. `Predictability` - A value that indicates OTHER's knowledge of this player's calls. If a bluffer is highly predictable, it means everyone knows he's bluffing.

Based on these we can have these personas:

1. Player 1 -> `Neutral` (all values at 0.5)
2. Player 2 -> `Bluffer` (high bluffness and raising, others moderate)
3. Player 3 -> `TruthGuy` (high truthfulness, others moderate)

And we can also have a **neutral player and sweep its axes against two other neutral players** to get a better sense of how things stand. Each player also has a `target` count they are trying to drive the bid toward.

### Plots

{{ figure(src="assets/axis_sweeps_BASE_neutral_control.png", alt="Neutral control sweep", caption="This sweeps all the axes for the netural player against neutral bots. This is our control") }}

> These are against neutral players

Across all the plots, clearly `calling` more is an advantage. The **win percentage and chips** gained scale equally with calling. Both bluffing more and being more truthful leads to a decline in revenue. Something interesting happens with **raising**.

**Raising** is supposed to signify a confident bet. If you raise more, the win percentage increases by a point but the net chips decrease to 0! This probably happens because even if you are winning slightly more, your losses hurt a **LOT** more, and in the net, they pull you down.

**Predictability** is an interesting case. It's saying that being not predictable at all or being highly predictable are both good. Anywhere in between is where you lose more. However the money you make doesn't really change (shows a slight increase). 

{{ figure(src="assets/axis_sweeps_BASE_vs_TRUTHFUL_BLUFFER.png", alt="Neutral sweep against truthful bluffer", caption="This sweeps all the axes for the neutral player against a bluffer and a truthful guy.") }}

> These are against a bluffer and a truthful guy

This is more interesting because raising and predictability have changed coureses drastically. Against a truthful guy and a bluffer, `raising` **DOES NOT** bring down your profits at all! This could be explained by the bluffer always bluffing harder and losing the pot to either you or the truthful guy. There can ofcourse be more nuanced explanations.

`Predictability` again doens't change the net money you make, but it does change how many rounds you win. The earlier drop becomes almost the new peak! Its better to be only slightly predictable against a truthful and a bluffer!

{{ figure(src="assets/heatmap_TRUTHFUL_truthfulness_x_predictability_vs_field.png", alt="Heatmap for truthfulness and predictability", caption="Amount of chips won depending on the truthfulness and predictability of the netural guy") }}

Its kind of counter-intuitive if you think about. Its saying that the more predictable AND truthful you are, the more chips you win (against a netural and a bluffer). Basically, letting others know that you are always truthful no matter what, works out.

This might be because everyone you're called out, you're rarely off the threshold cause you had been telling the truth. So you are either rarely called out, or you win the pot. Hence the money.

{{ figure(src="assets/joint_grid_BASE_vs_TRUTHFUL_BLUFFER.png", alt="Net chips over axes", caption="Joint grid for net chips against different values of bluffing") }}

Increasing the bluff lever, kills almost all variation in the green side and inverts the red side. This is pretty funny but also quite boring and normie.

### Variations

You will notice that the plots reveal something serious. The game is quite boring so to speak. Due to the dependent events set forth by the cards. So, let's give a little more to chance by adding more players and decks.

