+++
title = "Code and enumeration for Polyominoes"
date = 2026-09-22
draft = false

[taxonomies]
categories = ["Math", "Algebra"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

<style>
.poly {
  --cell: 1.2em;
  --poly-line: #3c4043;
  --poly-fill: #ffffff;
  --poly-new: #f2ce3c;
  --poly-gray: #d5d7da;
  --poly-red: #f0908a;
  --poly-green: #8ecf96;
  --poly-cyan: #86ccd6;
  display: inline-grid;
  grid-auto-columns: var(--cell);
  grid-auto-rows: var(--cell);
  vertical-align: middle;
  line-height: 0;
}
.poly i {
  display: block;
  border: 1px solid var(--poly-line);
  background: var(--poly-fill);
  margin: 0 -1px -1px 0;
}
.poly i.new { background: var(--poly-new); }
.poly i.g   { background: var(--poly-gray); }
.poly i.r   { background: var(--poly-red); }
.poly i.gr  { background: var(--poly-green); }
.poly i.cy  { background: var(--poly-cyan); }
.poly.sm    { --cell: 0.85em; vertical-align: -0.4em; }

.dark .poly {
  --poly-line: #8b9099;
  --poly-fill: #26282c;
  --poly-new: #b8952a;
  --poly-gray: #4b4f55;
  --poly-red: #9c5450;
  --poly-green: #4f7f57;
  --poly-cyan: #47818b;
}

.polyeq {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  margin: 1.7em 0;
}
.polyeq .op  { font-size: 1.1em; opacity: 0.7; padding: 0 0.1em; }
.polyeq .gap { width: 1.8em; }
.polyeq .lbl { font-size: 1em; white-space: nowrap; }

.latch { display: inline-flex; align-items: center; gap: 0.15em; }
.latch .pr {
  display: inline-block;
  font-size: 1.5em;
  font-weight: 300;
  line-height: 1;
  opacity: 0.55;
  transform: scaleY(1.45);
}
.latch .lt { font-family: KaTeX_Math, Georgia, serif; font-style: italic; font-size: 0.85em; opacity: 0.85; align-self: flex-end; margin-bottom: 0.35em; }

.slot {
  border: 1px dashed currentColor;
  background: rgba(128, 128, 128, 0.06);
  border-radius: 3px;
  padding: 1.1em 1.2em;
  margin: 1.6em 0;
  text-align: center;
  font-style: italic;
  font-size: 0.94em;
  opacity: 0.65;
}

.tetro-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
  gap: 0.5em 2.4em;
  margin: 1.8em 0;
}
.tetro { display: flex; align-items: center; gap: 1em; min-height: 5.2em; }
.tetro-pic { flex: 0 0 5.2em; line-height: 0; }
.tetro-eq { flex: 1 1 auto; min-width: 0; overflow-x: auto; overflow-y: hidden; }

@media (max-width: 400px) {
  .tetro-grid { grid-template-columns: 1fr; }
  .tetro-eq { font-size: 0.9em; }
}

.polyeq .stk { display: inline-flex; flex-direction: column; align-items: center; gap: 0.4em; }
.polyeq .stk .cap { font-size: 0.82em; opacity: 0.7; line-height: 1.2; white-space: nowrap; }
</style>

Find the code at [GitHub](https://github.com/pUrGe12/shape-algebra/blob/master/enumeration/without_sub.py).

# Cool information

The number of fixed polyominoes with $N$ cells is given in the [A001168](https://oeis.org/A001168) OEIS sequence, and you can see that it grows extremely fast. So, as N increases, since we're going to guess and check every possible string of size ~1.2N from before, with 4 different operations for each string that's a naive worst-case of $4^{1.2N}$.

## Representation

The premise of the code is to represent **each state** into a single arbitrary-precision integer with bitwise packing. The assignment looks like this:

| Bits | Field | Size | Description / Encoding |
| :--- | :--- | :--- | :--- |
| **0** | `latch` | 1 bit | `0` = `'R'` (Row mode), `1` = `'C'` (Column mode) |
| **1** | `pinned` | 1 bit | `0` = Unpinned, `1` = Pinned |
| **2..6** | `W` (Width) | 5 bits | Grid width (1 to 31) |
| **7..11** | `H` (Height) | 5 bits | Grid height (1 to 31) |
| **12..31** | `prS` (Row Pin Summary) | 20 bits | $4 \times 5$-bit fields storing row profile bounds |
| **32..51** | `pcS` (Col Pin Summary) | 20 bits | $4 \times 5$-bit fields storing column profile bounds |
| **52+** | `mask` (Occupancy) | Dynamic | 1 bit per cell: bit $((r - 1) \times W + (c - 1))$ |

Then the computation keeps updating this state in a precise manner.

Let me explain each bit clearly:

1. The `latch` bit

The latch bit is whether the current latch is on `Row` (0) or `Column` (1). It's evaluated with a bitwise `AND` (&) during runtime.

2. The `pin` flag

Determines if the selection of the line (row or column depending on what is being added) happens on a pinned shape (1) or the current whole shape (0). Again evaluated as an `AND` (&).

3. The width and height bits

For each state we track its width and height. This is defined as the width and height of the smallest enclosing rectangle for the polyomino whose each square is a single unit.

4. Pin summaries

We store the pinned shape's (or the current shape depending on the set bit) projection along each axis into a 4-tuple of 5-bit integers:

$$
\text{Summary} = (\text{first\_max}, \text{last\_max}, \text{first\_non\_zero}, \text{last\_non\_zero})
$$

- Row Summary `prS`: Four 5-bit integers shifted at offsets $12 + 5*i$ ($i \in [0, 3]$).
- Column Summary `pcS`: Four 5-bit integers shifted at offsets $32 + 5*i$ ($i \in [0, 3]$).

If pinned is `False`, then `prS` and `pcS` are forcibly overwritten with $(0, 0, 0, 0)$. This guarantees that two unpinned states with identical shape bitmasks but different "stale" historical pin summaries collapse into the same integers.

5. The bitmask

This is the most important part because this encodes the geometry of the shape. This is made by flattening the 2D shape into a 1D bitmask where each cell $(c, r)$ with $1 \le c \le W$ and $1 \le r \le H$, corresponds to bit position:

$$\text{Bit Position} = 52 + (r - 1) \times W + (c - 1)$$

> The reason we do this, is to limit the memory we use. Because we're going to have to hold so many states at the same time for computing larger and larger N values.

### Concrete example

Let's try this representation out for the following tetromino, and we'll keep updating this as we try to build it up to see how the logic holds up in the future too.

<div class="polyeq"><span class="poly"><i class="g" style="grid-area:1/2"></i><i class="g" style="grid-area:1/3"></i><i class="g" style="grid-area:2/1"></i><i class="g" style="grid-area:2/2"></i></span></div>

So, for this shape the construction is as follows:

<div class="polyeq"><span class="stk"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i></span><span class="cap">$A_R^{(2)}$ &middot; $v_0$</span></span><span class="op">$\xrightarrow{+\,1_C}$</span><span class="stk"><span class="poly"><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_1$</span></span><span class="op">$\xrightarrow{(\cdot)_C+\,1_R}$</span><span class="stk"><span class="poly"><i style="grid-area:1/2"></i><i class="new" style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_2$</span></span></div>

In full, that construction is $\left(\left(A_R^{(2)} + 1_C\right)_C + 1_R\right)$, and the yellow cell at each step is the one that was just added.

<div class="polyeq"><span class="stk"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i></span><span class="cap">$A_R^{(2)}$ &middot; $W=2$, $H=1$</span></span></div>

The initial seed ($A_R^{(2)}$) has the following properties:

- Grid: $W = 2$, $H = 1$
- Cells: $(1,1)$ and $(2,1)$
- Latch: 'R' | Pinned: False
- From the bitmask formulation we get:

$$\text{bit}(c, r) = (r - 1) \times W + (c - 1)$$

	Cell $(1,1) \to \text{bit } 0$
	Cell $(2,1) \to \text{bit } 1$
	Mask $= 2^0 + 2^1 = 3$ (0b00011)

Now we can compute the integer encoding for the first shape as $v_0$ given by:

$$
\begin{aligned}
\text{bit } 0 \ (\text{Latch}) &= 0 \quad (\text{'R'}) \\
\text{bit } 1 \ (\text{Pinned}) &= 0 \\
\text{bits } 2..6 \ (W) &= 2 \ll 2 = 8 \\
\text{bits } 7..11 \ (H) &= 1 \ll 7 = 128 \\
\text{bits } 52+ \ (\text{Mask}) &= 3 \ll 52 = 13,510,798,882,111,488 \\
\mathbf{v_0} &= \mathbf{13,510,798,882,111,624}
\end{aligned}
$$

Awesome!

### Code

The code for this is implemented as follows:

```py
def pack(W, H, mask, prS, pcS, lt, pinned):
    if not pinned: prS = pcS = ZERO
    v = (1 if lt == 'C' else 0) | (2 if pinned else 0) | (W << 2) | (H << 7)
    for i, x in enumerate(prS): v |= x << (12 + 5 * i)
    for i, x in enumerate(pcS): v |= x << (32 + 5 * i)
    return v | (mask << 52)
```

This function returns the same huge integer for the first state.

Its inverse just shifts everything back out, and `scope` is the small helper that decides *which* pair of summaries a selection is allowed to read: the stored pin summaries when the state is pinned, and a freshly computed profile of the whole shape when it isn't.

```py
def unpack(v):
    return ((v >> 2) & 31, (v >> 7) & 31, v >> 52,
            tuple((v >> (12 + 5 * i)) & 31 for i in range(4)),
            tuple((v >> (32 + 5 * i)) & 31 for i in range(4)),
            'C' if v & 1 else 'R', bool(v & 2))

def scope(W, H, mask, prS, pcS, pinned):
    """The summaries selection should actually read."""
    return (prS, pcS) if pinned else profile(W, H, mask)
```

That one-line `scope` is what implements "before any pin, the scope is the whole shape" from the first post, without needing a separate unpinned code path anywhere else.

## Manipulations

So, we're doing 4 things here:

1. Latching
2. Mirroring
3. Addition
4. Pinning

The one we're leaving out is subtraction because we don't need subtraction for $N \le 10$. Also, the GitHub repo linked above actually has a lot more code for a lot of different cases as well. I'll try to cover as many as possible, but this one was long overdue!

Let's talk about how each of them affect the bit string.

### Mirror effects

We know that mirror just means reflections along the row or column. Thus, the new $(c, r)$ cell after a mirror becomes

$$c' = W + 1 - c \quad \text{or} \quad r' = H + 1 - r$$

This changes the summaries (the 4-tuples) too:

$$
(f_{\text{max}}, l_{\text{max}}, f_{\text{nz}}, l_{\text{nz}}) \longrightarrow (L + 1 - l_{\text{max}}, L + 1 - f_{\text{max}}, L + 1 - l_{\text{nz}}, L + 1 - f_{\text{nz}})
$$

Looking at the code,

```py
def do_mirror(W, H, mask, prS, pcS, lt, pinned, axis):
    cs = cells_of(W, H, mask)
    if axis == 'C':
        return pack(W, H, mask_of([(W + 1 - c, r) for c, r in cs], W),
                    prS, rev(pcS, W), lt, pinned)
    return pack(W, H, mask_of([(c, H + 1 - r) for c, r in cs], W),
                rev(prS, H), pcS, lt, pinned)
```

you can see this in effect. The `rev` function is the one which runs the logic for the summaries:

```py
def rev(t, L): return (L + 1 - t[1], L + 1 - t[0], L + 1 - t[3], L + 1 - t[2])
```

Note that a `'C'` mirror reverses only `pcS` and leaves `prS` alone (and vice versa), which is exactly the "the pin travels with mirrors" rule, and that `lt` is passed straight through, which is the "the mirror tag does not latch" rule.

### Pinning

Here we need to summarise the current state and set `pinned` to high. This is done in 3 steps:

1. It computes `profile(W, H, mask)` for the active shape bitmask. The `profile` function calculates the cells per row/column and summarizes counts.

2. It sets `pinned` = True (bit 1 set to 1).

3. It writes the generated row/col 4-tuples into bits $12...51$.

This is the code for it:

```py
def profile(W, H, mask):
    pr = [0] * H; pc = [0] * W
    for c, r in cells_of(W, H, mask): pr[r - 1] += 1; pc[c - 1] += 1
    return summ(pr), summ(pc)

def do_pin(W, H, mask, lt):
    a, b = profile(W, H, mask)
    return pack(W, H, mask, a, b, lt, True)
```

We just need to keep track of WHICH cells were pinned and once we do that via summaries, we're sorted, then we just let the future states know that there is a separate pinned shape.

The compression happens in `summ`, which is what turns a whole list of per-line counts into the 4-tuple:

```py
def summ(counts):
    m = max(counts); first = last = fnz = lnz = 0
    for i, v in enumerate(counts, 1):
        if v == m:
            if not first: first = i
            last = i
        if v:
            if not fnz: fnz = i
            lnz = i
    return (first, last, fnz, lnz)
```

Four numbers are enough because the rules only ever ask two questions of a line: "which one has the most cells" (`first`/`last`, with the tie broken topmost for rows and rightmost for columns) and "which one is the default" (`fnz`/`lnz`, the topmost or rightmost occupied line). We never need the counts themselves, so they don't get stored.

### Adding $1_R$/$1_C$ and latching

Explicit latching is handled inside addition only because normally you latch and then quickly add a block.

When a new cell lands at $(c, r)$:

- If $r = 0$ (growing upward), the grid expands ($H^' = H + 1$) and all existing rows shift down by 1 in the bitmask (`dr = 1`). The **row** pin summary values are incremented by `dr`; the column summary is left untouched, since shifting rows renumbers row indices only.

- If $c > W$, $W^' = c$ and the bitmask is re-indexed to the new width $W^'$.

- The new cell bit is flipped to 1, and the single-use latch mode falls back to default.

This is the code that does it.

```py
def additions(v):
    W, H, mask, prS, pcS, lt, pinned = unpack(v)
    out = []
    for X in 'RC':
        for u in 'RC':
            s = do_add(W, H, mask, prS, pcS, X, 'most', u, pinned)
            if s is not None: out.append(s)
    for u in 'RC':
        s = do_add(W, H, mask, prS, pcS, lt, 'default', u, pinned)
        if s is not None: out.append(s)
    return out

def do_add(W, H, mask, prS, pcS, latch, mode, unit, pinned):
    """Return the new packed state, or None if the cell is already occupied."""
    sprS, spcS = scope(W, H, mask, prS, pcS, pinned)
    prS, pcS = sprS, spcS
    if latch == 'R':
        rho = prS[0] if mode == 'most' else prS[2]
        if unit == 'R': c, r = maxcol(mask, W, rho) + 1, rho
        else:
            c = maxcol(mask, W, rho); r = minrow(mask, W, H, c) - 1
    else:
        gam = pcS[1] if mode == 'most' else pcS[3]
        if unit == 'C': c, r = gam, minrow(mask, W, H, gam) - 1
        else:
            rs = minrow(mask, W, H, gam); c, r = maxcol(mask, W, rs) + 1, rs
    if 1 <= c <= W and 1 <= r <= H and mask >> ((r - 1) * W + (c - 1)) & 1:
        return None
    dr = 1 if r == 0 else 0           # growing upward shifts every row down
    nW = max(W, c); nH = H + dr
    old = cells_of(W, H, mask)
    nm = mask_of([(cc, rr + dr) for cc, rr in old] + [(c, r + dr)], nW)
    return pack(nW, nH, nm,
                tuple(x + dr for x in sprS), spcS, latch, pinned)
```

You can see the latching mechanism in `do_add` very clearly, along with a `mode` separator. The `mode` is there to implement the logic of selecting the row/column with MOST cells or the default one (defined as rightmost or topmost).

One more detail worth pointing out in that last `pack` call: the four index picks line up one-for-one with the rules from the first post: `prS[0]` is the topmost max row, `pcS[1]` is the rightmost max column, `prS[2]` is the topmost occupied row and `pcS[3]` is the rightmost occupied column. Those are exactly the tie-breaks the algebra asks for.

The `additions` function is where the "four different operations" figure from the top comes from: four latch/unit combinations under `'most'`, plus two more under `'default'` that reuse whatever latch the state already carries.

## Finishing up the example

So, now that we have the base for the example ready, let's compute the first addition:

The step can be represented as:

> Add Unit $1_C$ with Latch 'R' (mode = 'most')

<div class="polyeq"><span class="stk"><span class="poly"><i style="grid-area:1/1"></i><i style="grid-area:1/2"></i></span><span class="cap">$v_0$</span></span><span class="op">$\xrightarrow{+\,1_C}$</span><span class="stk"><span class="poly"><i class="new" style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_1$</span></span></div>

First the row selection:

1. Latch is 'R' $\implies$ inspect the row counts and find the most populated row.
2. There is only one row which means, row 1 has 2 cells (max) $\implies$ target row $\rho = 1$.

Then the landing point:

3. The target column $c = \text{maxcol}(\text{row } 1) = 2$ which is the default one too in this case.
4. Target row $r = \text{minrow}(\text{col } 2) - 1 = 1 - 1 = 0$. (Note that row 1 and row 0 are just notation to say one above the other!).
5. Target coordinate is $(2, 0)$ (above row 1).

Then the grid shift:

6. $r = 0 \implies dr = 1$ (grid grows upward by 1 row).
7. We compute the new height and width: New height $H' = 2$, width $W' = 2$.
8. The existing cells shift down: $(1,1) \to (1,2)$ and $(2,1) \to (2,2)$.
9. New cell lands at $(2, 1)$ (that's (column,row) sorry about the twisted thing here)

Now we calculate the updated mask:

- Cell $(2,1) \to \text{bit } 1 \ (2^1 = 2)$
- Cell $(1,2) \to \text{bit } 2 \ (2^2 = 4)$
- Cell $(2,2) \to \text{bit } 3 \ (2^3 = 8)$
- Mask $= 2 + 4 + 8 = 14$ (`0b01110`)

And finally we get the new integer encoding ($v_1$)

$$
\begin{aligned}
\text{bits } 2..6 \ (W=2) &= 8 \\
\text{bits } 7..11 \ (H=2) &= 256 \\
\text{bits } 52+ \ (\text{Mask}=14) &= 14 \ll 52 = 63,050,394,783,186,944 \\
\mathbf{v_1} &= \mathbf{63,050,394,783,187,208}
\end{aligned}
$$

Now the final step is to add another unit $1_R$ with Latch `C`, mode = `most` (again since we explicitly set the latch).

<div class="polyeq"><span class="stk"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_1$</span></span><span class="op">$\xrightarrow{(\cdot)_C+\,1_R}$</span><span class="stk"><span class="poly"><i style="grid-area:1/2"></i><i class="new" style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_2$</span></span></div>

We perform the same steps, and this time we get the following mask ($W=3, H=2$)

- Cell $(2,1) \to \text{bit } 1 \ (2^1 = 2)$
- Cell $(3,1) \to \text{bit } 2 \ (2^2 = 4)$
- Cell $(1,2) \to \text{bit } 3 \ (2^3 = 8)$
- Cell $(2,2) \to \text{bit } 4 \ (2^4 = 16)$
- Mask $= 2 + 4 + 8 + 16 = 30$ (`0b011110`)

And hence, final integer encoding ($v_2$)

$$
\begin{aligned}
\text{bit } 0 \ (\text{Latch 'C'}) &= 1 \\
\text{bits } 2..6 \ (W=3) &= 12 \\
\text{bits } 7..11 \ (H=2) &= 256 \\
\text{bits } 52+ \ (\text{Mask}=30) &= 30 \ll 52 = 135,107,988,821,114,880 \\
\mathbf{v_2} &= \mathbf{135,107,988,821,115,149}
\end{aligned}
$$

And that's the final shape!

<div class="polyeq"><span class="stk"><span class="poly"><i style="grid-area:1/2"></i><i style="grid-area:1/3"></i><i style="grid-area:2/1"></i><i style="grid-area:2/2"></i></span><span class="cap">$v_2 = 135{,}107{,}988{,}821{,}115{,}149$</span></span></div>

## Enumeration

Now that we understand this, the script is a level-by-level BFS using the integers as state. At every $N$:

1. Inject some seed (that's the $A_j^{k}$)
2. Explores all algebraic configurations of the same cell count $n$ without adding any shapes.

It initializes a double-ended queue q = deque(cur). For every integer v in q, it calls successors(v) to generate:

- Horizontal mirror ($M_C$) $\to$ yields a new integer.
- Vertical mirror ($M_R$) $\to$ yields a new integer.
- Pin ($P$) $\to$ yields a new integer with bit 1 set and pin summaries computed.

If a newly generated integer nx is not in cur, it is added to cur and pushed to q. And so, the set cur now holds every valid state integer reachable at size $n$.

The seeds are just the two strips of length $n$, packed directly, with the latch already set to match the orientation:

```py
def seeds(n):
    out = []
    for horiz in (True, False):
        W, H = (n, 1) if horiz else (1, n)
        mask = (1 << n) - 1 if horiz else sum(1 << (r * W) for r in range(n))
        out.append(pack(W, H, mask, ZERO, ZERO, 'R' if horiz else 'C', False))
    return out
```

And `successors` is the cell-count-preserving half of the step set, which is why it can be iterated to a fixed point without ever leaving level $n$:

```py
def successors(v, use_p):
    W, H, mask, prS, pcS, lt, pinned = unpack(v)
    out = [do_mirror(W, H, mask, prS, pcS, lt, pinned, 'C'),
           do_mirror(W, H, mask, prS, pcS, lt, pinned, 'R')]
    if use_p: out.append(do_pin(W, H, mask, lt))
    return out
```

Putting the two together, here is the whole sweep. The inner `while q` loop is the closure at level $n$, and the last three lines are the single step that carries every state up to level $n+1$ via `additions`:

```py
def sweep(N, use_p=True, max_states=None):
    cur = set(seeds(1)); reached = {}
    t0 = time.time()
    for n in range(1, N + 1):
        cur |= set(seeds(n))
        q = deque(cur)
        while q:
            for nx in successors(q.popleft(), use_p):
                if nx not in cur: cur.add(nx); q.append(nx)
        reached[n] = {shape_key(v) for v in cur}
        print(f"  n={n:>2}: {len(reached[n]):>9} shapes, {len(cur):>10} states, "
              f"{time.time()-t0:>6.0f}s", flush=True)
        if max_states and len(cur) > max_states:
            print(f"  stopping: state count passed --max-states"); break
        if n == N: break
        nxt = set()
        for v in cur: nxt.update(additions(v))
        cur = nxt
    return reached
```

That should be enough for now!