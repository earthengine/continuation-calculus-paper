# Title: Call-by-value 13 + 0

# Definitions

Zero.z.s -> z
S.x.z.s -> s.x
Nil.e.c -> e
Cons.x.xs.e.c -> c.x.xs

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

# Computing 13 + 0 = 13 takes 41 steps.
AddCBV.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))))).Zero.fr
# Computing 0 + 13 = 13 takes 2 steps.
AddCBV.Zero.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))))).fr