# Title: List multiplication of [3, 1, 2]

# Definitions

ListMult.l.r -> A.l.r.(r.Zero)
A.l.r.abort -> l.(r.(S.Zero)).(B.r.abort)
B.r.abort.x.xs -> x.abort.(C.r.abort.x.xs)
C.r.abort.x.xs.x' -> A.xs.(PostMult.x.r).abort
PostMult.x.r.y -> Mult.x.y.r
Mult.x.y.r -> y.(r.Zero).(PostMult.x.(PostAdd.x.r))
PostAdd.x.r.y -> AddCBV.x.y.r

# Implementation from fib.cc

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

Zero.z.s -> z
S.m.z.s -> s.m
Nil.ifempty.iflist -> ifempty
Cons.n.l.ifempty.iflist -> iflist.n.l

# Reduce these terms
ListMult.(Cons.(S.(S.(S.Zero))).(Cons.(S.Zero).(Cons.(S.(S.Zero)).Nil))).fr
