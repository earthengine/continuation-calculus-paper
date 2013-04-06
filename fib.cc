# Run this program as follows:
#
#   python3 cc.py -printnum < fib.cc
#
#
# This will print embedded numbers as integers: (S.(S.(S.Zero))) will be
# printed 3. However, be sure to use (S.(S.(S.Zero))) in the input. A 3 in the
# input will be treated as any other name: behaviorless by default.
#
# To see the raw evaluating terms:
#
#   python3 cc.py < fib.cc

Zero.z.s → z
S.m.z.s → s.m
Nil.ifempty.iflist → ifempty
Cons.n.l.ifempty.iflist → iflist.n.l

# fib 0 = 0
# fib 1 = 1
# fib n+2 = fib n + fib (n+1)
# 
# let rec fib =
#   | 0 -> 0
#   | y + 1 -> match y with
#     | 0 -> 1
#     | y' + 1 -> fib y + fib y'

# Call-by-value

AddCBV.x.y.r → x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x → AddCBV.x.(S.y).r

FibCBV.x.r → x.(r.Zero).(FibCBV_1.r)
FibCBV_1.r.y → y.(r.(S.Zero)).(FibCBV_2.r.y)
FibCBV_2.r.y.y' → FibCBV.y.(FibCBV_3.r.y')
FibCBV_3.r.y'.fib_{y} → FibCBV.y'.(FibCBV_4.r.fib_{y})
FibCBV_4.r.fib_{y}.fib_{y'} → AddCBV.fib_{y}.fib_{y'}.r

# Call-by-name

AddCBN.x.y.z.s → x.(y.z.s).(AddCBN'.y.s)
AddCBN'.y.s.x' → s.(AddCBN.x'.y)

FibCBN.x.z.s → x.z.(FibCBN_1.z.s)
FibCBN_1.z.s.y → y.(s.Zero).(FibCBN_2.z.s.y)
FibCBN_2.z.s.y.y' → AddCBN.(FibCBN.y).(FibCBN.y').z.s

# To see fib(7) = 13:
# FibCBV.(S.(S.(S.(S.(S.(S.(S.Zero))))))).fr
AddCBV.(FibCBN.(S.(S.(S.(S.(S.(S.(S.Zero)))))))).Zero.fr
# AddCBV.Zero.(FibCBN.(S.(S.(S.(S.(S.(S.(S.Zero)))))))).fr
# 
# AddCBV.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))))).Zero.fr
# AddCBV.Zero.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))))).fr

# To see fib(10) = 55:
# FibCBV.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero)))))))))).fr
# AddCBV.(FibCBN.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))).Zero.fr
# AddCBV.Zero.(FibCBN.(S.(S.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))))).fr

