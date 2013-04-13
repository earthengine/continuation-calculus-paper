# Continuation calculus #

There are two ways you can try continuation calculus for yourself: a web interface and a Python script.

## Web interface ##

Go to [http://bgeron.nl/cc-paper/](http://bgeron.nl/cc-paper/) to try it yourself. The webinterface works fine, but is slower and has slightly less features.

## Python script ##

Download the source using the link on your right, or clone this Mercurial repository. 

Type this:

	python3 cc.py input.cc

The program will load the continuation calculus definitions in input.cc, and execute the terms.

You can also enter interactive mode:

    python3 cc.py

Now you can enter definitions and terms. Definitions will be remembered, terms will be evaluated to a final term.

For the syntax of terms and rules, look in fib.cc en listmult.cc. Terms and definitions must be on single lines, with no surrounding whitespace. A hash symbol starts a comment line.

Options:

> [no option]   Produce human-readable output.
>
> -printnum:    Produce human-readable output, but replace (S.(S.(S.Zero))) by
>               3 in the output. Warning: you must still enter S.(S.(S.Zero))
>               in the input!
>
> -printlatex:  Produce output suitable for inclusion in a LaTeX file
>
> -printlyx:    Produce output suitable for inclusion in a LyX file


You can choose only one of the options.