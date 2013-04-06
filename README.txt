To use the evaluator, type this:

python3 cc.py < input.cc

The program will load the continuation calculus definitions in input.cc, and execute the terms.

Terms and definitions must be on single lines, with no surrounding whitespace. A hash symbol starts a comment line.

Options:

  [no option]   Produce human-readable output.

  -printnum:    Produce human-readable output, but replace (S.(S.(S.Zero))) by
                3 in the output. Warning: you must still enter S.(S.(S.Zero))
                in the input!

  -printlatex   Produce output suitable for inclusion in a LaTeX file

  -printlyx     Produce output suitable for inclusion in a LyX file


You can choose only one of the options.