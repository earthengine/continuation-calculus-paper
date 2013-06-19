# Title: List multiplication of [3, 0, 2] vs. [3, 1, 2]

# Definitions

ListMult.xs.r -> A.xs.r.(r.Zero)
A.xs.r.abort -> xs.(r.(S.Zero)).(B.r.abort)
B.r.abort.x.xs -> x.abort.(C.r.abort.x.xs)
C.r.abort.x.xs.x' -> A.xs.(PostMult.x.r).abort
PostMult.x.r.y -> Mult.x.y.r
Mult.x.y.r -> y.(r.Zero).(PostMult.x.(PostAdd.x.r))
PostAdd.x.r.y -> AddCBV.x.y.r

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x' -> AddCBV.x'.(S.y).r

Zero.z.s -> z
S.x.z.s -> s.x
Nil.e.c -> e
Cons.x.xs.e.c -> c.x.xs

# Calculating the product of [3, 0, 2] takes 10 steps
ListMult.(Cons.(S.(S.(S.Zero))).(Cons.Zero.(Cons.(S.(S.Zero)).Nil))).fr
# Calculating the product of [3, 1, 2] takes 87 steps
ListMult.(Cons.(S.(S.(S.Zero))).(Cons.(S.Zero).(Cons.(S.(S.Zero)).Nil))).fr