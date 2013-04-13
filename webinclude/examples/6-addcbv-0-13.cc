# Title: Call-by-value 0 + 13

# Definitions

Zero.z.s -> z
S.m.z.s -> s.m
Nil.ifempty.iflist -> ifempty
Cons.n.l.ifempty.iflist -> iflist.n.l

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

# To see 0 + 13 = 13, run this. This takes 41 steps.
AddCBV.Zero.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))))).fr