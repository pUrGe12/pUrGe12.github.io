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

# Introduction

I was watching some clips on YouTube of Pirates of the Carribean and the scene where Davy Jones plays against Will Turner the dice game got me thinking. So, naturally I wanted to understand how the fuck the game even works because the movie's cut for this scene does an absolute jackshit job of explaining it. I found some YouTube videos to explain the game and I won't explain that here but I'll [link the video](https://youtu.be/T44LuxdH0iw?si=2B5FIfzB6kQPapCQ) so that you can see for yourself.

Now I only have a deck of cards, and 0 dies, which means I had to come up with a variant for Liar's Dice that I can play with my friends using cards. 

> The major difference between dies and cards is that cards have dependent events

In a typical liar's dice game, you can roll any number you want, but it doesn't necessarily pin down or give you any information about what the other player might have. In cards however, such is not the case. Because if you see 3 6's in your hand, then you're damn sure only 1 more exists in the entire deck, so your betting strategy will change. Anyways, I am getting ahead of myself here, let me explain the rules a little more precisely.

## Rules

This is a 3 player game only with 1 standard card deck. Each player gets 5 cards out of a standard 52 card deck.

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

{{ figure(src="assets/axis_sweeps_BASE_neutral_control.png", alt="Neutral control sweep", caption="This sweeps all the axes for the neutral player against neutral bots. This is our control") }}

> These are against neutral players

Across all the plots, clearly `calling` more is an advantage. The **win percentage and chips** gained scale equally with calling. Both bluffing more and being more truthful leads to a decline in revenue. Something interesting happens with **raising**.

**Raising** is supposed to signify a confident bet. If you raise more, the win percentage increases by a point but the net chips decrease to 0! This probably happens because even if you are winning slightly more, your losses hurt a **LOT** more, and in the net, they pull you down.

**Predictability** is an interesting case. It's saying that being not predictable at all or being highly predictable are both good. Anywhere in between is where you lose more. However the money you make doesn't really change (shows a slight increase). 

{{ figure(src="assets/axis_sweeps_BASE_vs_TRUTHFUL_BLUFFER.png", alt="Neutral sweep against truthful bluffer", caption="This sweeps all the axes for the neutral player against a bluffer and a truthful guy.") }}

> These are against a bluffer and a truthful guy

This is more interesting because raising and predictability have changed courses drastically. Against a truthful guy and a bluffer, `raising` **DOES NOT** bring down your profits at all! This could be explained by the bluffer always bluffing harder and losing the pot to either you or the truthful guy. There can ofcourse be more nuanced explanations.

`Predictability` again doesn't change the net money you make, but it does change how many rounds you win. The earlier drop becomes almost the new peak! Its better to be only slightly predictable against a truthful and a bluffer!

{{ figure(src="assets/heatmap_TRUTHFUL_truthfulness_x_predictability_vs_field.png", alt="Heatmap for truthfulness and predictability", caption="Amount of chips won depending on the truthfulness and predictability of the neutral guy") }}

Its kind of counter-intuitive if you think about. Its saying that the more predictable AND truthful you are, the more chips you win (against a neutral and a bluffer). Basically, letting others know that you are always truthful no matter what, works out.

This might be because everyone you're called out, you're rarely off the threshold cause you had been telling the truth. So you are either rarely called out, or you win the pot. Hence the money.

{{ figure(src="assets/joint_grid_BASE_vs_TRUTHFUL_BLUFFER.png", alt="Net chips over axes", caption="Joint grid for net chips against different values of bluffing") }}

Increasing the bluff lever, kills almost all variation in the green side and inverts the red side. This is pretty funny but also quite boring and normie.

### Variations

You will notice that the plots reveal something serious. The game is quite boring so to speak. Due to the dependent events on the cards. So, let's give a little more to chance by adding more players and decks.

We want to find the "optimal" game, so to do that, we first need to define what an optimal game means in this context. This is what I came up with:

> An optimal game is where bluffing and calling both lie in the "contested" zone, and more than 40% of the entire deck remains hidden in an honest table (everyone is honest)

Let's first unpack what a contested zone is. Look at this image here for a normal game:

{{ figure(src="assets/bid_winprob_contested_zone.png", alt="Bid win probability distribution against bet size", caption="Bid win probability distribution against bid size for H and N cards.") }}

The `contested zone` is defined as the region where there is a near coin flip probability of winning or losing the bid. This adds an element of fun in the game. In the plain game as shown above the contested zone is really only for 1 number in each of H and N. Can we do better?

> Note the probability remains same in going from 10 to 11, because of the 0.1 tolerance rule

{{ figure(src="assets/decks_winprob_widen_contested_zone.png", alt="Bid win probability on H against multiple decks", caption="Bid win probability distribution for H against multiple decks") }}

This image shows the effect of different deck sizes in a 3 player game on the probability of a victory. What you should note, is that when there are more decks, the point 8 slowly slides inside the contested zone. This means, we wanna up our number of decks.

But if we use more decks without increasing the number of players, that's gonna be bad too. Because look at this graph.

{{ figure(src="assets/sweep_lines_players_vs_game_health.png", alt="Effect of number of players on the game health", caption="Left: effect of number of players and number of decks on game health. Having 1 deck and 10 players kills bluffing. Right: Same plot with different axes") }}

This is using a metric called "contested-zone health" which is the weighted total number of **bid values**, across all faces, that sit in the **bluffable win-probability band** which is defined as the band where the win probability is within 30% to 70%.

We can see that 9 players seem to maximize the health of the contested zone, which in-turn means there is a higher chance of someone bluffing and it being a genuinely contested bet. 10 players might rise up with more decks, but we're already pushing our limits with 6 decks. This is not blackjack!

So, clearly an optimal seems to be around 9 players and 3 decks, we can verify that with a heatmap too:

{{ figure(src="assets/sweep_heatmap_players_vs_game_health.png", alt="Heatmaps for the previous data", caption="Heatmaps for gamehealth vs number of decks measured against different fields.") }}

If we analyze this properly, then our above assessment becomes clearer. About 71% of the deck is still hidden which leaves enough room for players to bluff (with 80%+ still hidden, all calls will be bluffs!) while still having something substantial on the table. The **game health** (contested zone health) also supports this argument. At 10 decks, the room for blluffing is way too high for a game to function normally, and too little decks, kills bluffing very fast.

We need to work in the diagonal band and on the upper side of it, which is 3 players and 9 decks.

### Plots for 3P9D

For 3P9D, we can run the simulations again and see how they affect the game.

{{ figure(src="assets/joint_grid_BASE_9p_3deck.png", alt="Heatmaps for calling and bluffing 9p3d", caption="Calling vs Raising over 9 players and 3 decks w.r.t. the number of chips gained.") }}

If you compare these heatmaps to the ones made for the 3p1d configuration, it will become very apparent as to why the 9p3d is a much better game

{{ figure(src="assets/joint_grid_BASE_vs_TRUTHFUL_BLUFFER.png", alt="Heatmaps for calling and bluffing", caption="Calling vs Raising for 3 players and 1 deck w.r.t. the number of chips gained against a truthful player and a bluffer player.") }}

- The 9p3d set tells us that calling too much, even if the player is a huge bluffer will reward you negatively. While the 3p1d set always tells you to call. 

- There are certain gray areas in the 9p3d config, especially when you raise moderately (0.6) and call base (base is where all params are 0.5) aggressively, you are more likely to lose all your money there.

- The best part about 9p3d is that the middle region is a mix of green and orange, which means the region where most players will live in, is where there is a lot of variability, which is what makes a game worth playing. In contrast to the 3p1d where there are solid boundaries!

---

Before I run the next part of the sims, I noticed that to make sure **calling is not the best thing** in the world for any bluff level, I decided to **penalize calls**. That is, by having the caller throw in some money in the pot. But that doesn't make sense if you think about it, they'll just throw in the table minimum always. So, we change the rules:

> Let anyone in the table call out, the final caller will be decided by the size of their bets during calls

The confidence of their calls is prescribed by their bet size they're willing to throw into the pot. All potential callers would throw in their money, one person will win, rest automatically lose money. The `conviction` is a metric for how much they want to call, which is reflected in their bid size.

{{ figure(src="assets/axis_sweeps_BASE_9p_3deck.png", alt="Axis sweeps for 9p3d", caption="Sweeping the axis for the BASE player in a 9p3d setting.") }}

This is another very important graph because if you look at the **bluffing** axis, its now at an optimal value of 0.2ish! Which means you should bluff atleast 20% of the times and if you look at the slope of the curve leading up to it, the number of victories rise steeply as you start bluffing from 0 to 0.2.

And this time, calling all the time is not the best strategy, while the number of games you win will increase, you will lose money when you do so (because you are throwing money in the pot).

Another important revelation now is that, if you are in general `truthful`, then being sligtly predictable is fine, but as soon as someone is sure that you are always saying the truth, you get screwed very very quickly. This is because its not just the next call who can call you out, **its anyone in the table**. So you got to be extra careful.

The `conviction` axis is also pretty interesting, the more money you throw in your calls, (that is, the more you `show` that you are sure of what your calls are) the more you win. Pretty neat.

Let's look at the truthfulness and predictability map in more details:

{{ figure(src="assets/heatmap_TRUTHFUL_truthfulness_x_predictability_9p_3deck.png", alt="Truthfulness vs predictability over chips scored", caption="Truthfulness vs predictability over chips scored") }}

1. Being 100% truthful and 0% predictable (hard to replicate in real life) earns you a lot of money
2. Being 0% truthful and 100% predictable (that is, everyone knows you just lie), you get called out a lot and lose money

> There really is only one optimal strategy here, its best to be 0% predictable, no matter whether you're truthful or not

---

Alright that concludes this. I will (hopefully) code out a website where I can play this game with bots and maybe even host it in the future. Haffun.