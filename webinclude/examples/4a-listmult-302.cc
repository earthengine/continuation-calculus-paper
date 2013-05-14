# Title: List multiplication of [3, 0, 2]

# Definitions

ListMult.l.r -> A.l.r.(r.Zero)
A.l.r.abort -> l.(r.(S.Zero)).(B.r.abort)
B.r.abort.x.xs -> x.abort.(C.r.abort.x.xs)
C.r.abort.x.xs.x' -> A.xs.(PostMult.x.r).abort
PostMult.x.r.y -> Mult.x.y.r
Mult.x.y.r -> y.(r.Zero).(PostMult.x.(PostAdd.x.r))
PostAdd.x.r.y -> AddCBV.x.y.r

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

Zero.z.s -> z
S.x.z.s -> s.x
Nil.e.c -> e
Cons.x.xs.e.c -> c.x.xs

# Reduce these terms
ListMult.(Cons.(S.(S.(S.Zero))).(Cons.Zero.(Cons.(S.(S.Zero)).Nil))).fr
