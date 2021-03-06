# Title: 0 plus call-by-name fib(8)

# Encoding of data

Zero.z.s -> z
S.x.z.s -> s.x

# Definitions for call-by-value

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x' -> AddCBV.x'.(S.y).r

FibCBV.x.r -> x.(r.Zero).(FibCBV_1.r)
FibCBV_1.r.y -> y.(r.(S.Zero)).(FibCBV_2.r.y)
FibCBV_2.r.y.y' -> FibCBV.y.(FibCBV_3.r.y')
FibCBV_3.r.y'.fib_y -> FibCBV.y'.(FibCBV_4.r.fib_y)
FibCBV_4.r.fib_y.fib_y' -> AddCBV.fib_y.fib_y'.r

# Definitions for call-by-name

AddCBN.x.y.z.s -> x.(y.z.s).(AddCBN'.y.s)
AddCBN'.y.s.x' -> s.(AddCBN.x'.y)

FibCBN.x.z.s -> x.z.(FibCBN_1.z.s)
FibCBN_1.z.s.y -> y.(s.Zero).(FibCBN_2.z.s.y)
FibCBN_2.z.s.y.y' -> AddCBN.(FibCBN.y).(FibCBN.y').z.s

# Terms to evaluate
AddCBV.Zero.(FibCBN.(S.(S.(S.(S.(S.(S.(S.(S.Zero))))))))).fr
