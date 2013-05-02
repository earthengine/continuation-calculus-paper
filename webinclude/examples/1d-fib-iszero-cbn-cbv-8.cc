# Title: Test whether fib(8) = 0: CBN faster than CBV

# Definitions

Zero.z.s -> z
S.m.z.s -> s.m
Nil.ifempty.iflist -> ifempty
Cons.n.l.ifempty.iflist -> iflist.n.l

# Definitions for call-by-value

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

FibCBV.x.r -> x.(r.Zero).(FibCBV_1.r)
FibCBV_1.r.y -> y.(r.(S.Zero)).(FibCBV_2.r.y)
FibCBV_2.r.y.y' -> FibCBV.y.(FibCBV_3.r.y')
FibCBV_3.r.y'.fib_{y} -> FibCBV.y'.(FibCBV_4.r.fib_{y})
FibCBV_4.r.fib_{y}.fib_{y'} -> AddCBV.fib_{y}.fib_{y'}.r

# Definitions for call-by-name

AddCBN.x.y.z.s -> x.(y.z.s).(AddCBN'.y.s)
AddCBN'.y.s.x' -> s.(AddCBN.x'.y)

FibCBN.x.z.s -> x.z.(FibCBN_1.z.s)
FibCBN_1.z.s.y -> y.(s.Zero).(FibCBN_2.z.s.y)
FibCBN_2.z.s.y.y' -> AddCBN.(FibCBN.y).(FibCBN.y').z.s

IsZero.n -> n.yes.IsZero'
IsZero'.n' -> no

# Is FibCBN.8 zero?
IsZero.(FibCBN.(S.(S.(S.(S.(S.(S.(S.(S.Zero)))))))))

# Compute FibCBV.8. As the result is 21, continue evaluation in IsZero.21.
FibCBV.(S.(S.(S.(S.(S.(S.(S.(S.Zero)))))))).IsZero