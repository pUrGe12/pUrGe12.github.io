from stitch_core import compress

# The same programs as above, written in de Bruijn style
programs = [
    "(lam (+ 3 (* (+ 2 4) 2)))",
    "(lam (map (lam (+ 3 (* 4 (+ 3 $0)))) $0))",
    "(lam (* 2 (+ 3 (* $0 (+ 2 1)))))"
]

# Iterations control the number of abstractions
res = compress(programs, iterations=1, max_arity=2)

res.abstractions[0]
# fn_0(#0,#1) := (+ 3 (* #1 #0))

# We can rewrite with the abstractions

from stitch_core import rewrite
a = rewrite(["(lam (+ 3 (* (+ 1 1) 1)))", "(lam (- 5 (+ 3 (* $0 (+ 2 1)))))"], res.abstractions)
# [
#     '(lam (fn_0 1 (+ 1 1)))',
#     '(lam (- 5 (fn_0 (+ 2 1) $0)))'
# ]

# We can also do silent=False

res2 = compress(programs, iterations=1, max_arity=2, silent=False)
# This will produce a lot of interesting outputs
