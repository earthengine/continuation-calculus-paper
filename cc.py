#!/usr/bin/env python3

import sys, buffer, io, os

_defs = dict() # stores rules

# defaults to be overridden in main()
_PRINTNUM = False # convert (S.(S.Zero)) to 2?
_PRINTLATEX = False # whether to output pure latex
_PRINTLYX = False # whether to output for LyX math array mode
_PRINTLATEXY = False # = printlatex or printlyx
_PRINTVERBOSE = True # = not printlatexy

# Some methods to make everything Python 2 compatible.

if isinstance(range(0), list):
    # Python 2
    range = xrange
    def tounicode(b):
        return b.decode("utf-8")
    if 'EOFError' in dir(io):
        # PyJS
        from io import EOFError
        def tounicode(s):
            return s
        unichr = chr
    else:
        str = unicode
else:
    # Python 3
    def tounicode(s):
        return s
    unichr = chr

def printstdout(s="", end="\n"):
    "Print to standard output."
    return sys.stdout.write(s + end)

def printstderr(s="", end="\n"):
    "Print to standard error."
    return sys.stderr.write(s + end)

def usage():
    printstderr("Usage:")
    printstderr("    python cc.py [-printnum|-printlatex|-printlyx] [input.cc]")
    printstderr("Options:")
    printstderr("")
    printstderr("  [no option]   Produce human-readable output.")
    printstderr("")
    printstderr("  -printnum:    Produce human-readable output, but replace (S.(S.(S.Zero))) by")
    printstderr("                3 in the output. Warning: you must still enter S.(S.(S.Zero))")
    printstderr("                in the input!")
    printstderr("")
    printstderr("  -printlatex   Produce output suitable for inclusion in a LaTeX file")
    printstderr("")
    printstderr("  -printlyx     Produce output suitable for inclusion in a LyX file")

def usagefail():
    usage()
    exit(1)

class ReductionFail(Exception):
    __slots__ = ['message']

    def __init__(self, message):
        # assert isinstance(message,str)
        self.message = message

    def __str__(self):
        return self.message

def main():
    global _PRINTLATEX, _PRINTLYX, _PRINTNUM, _PRINTLATEXY, _PRINTVERBOSE

    override_stdin = False

    for arg in sys.argv[1:]:
        if arg == '-printlatex' and not _PRINTLATEX:
            assert not _PRINTLYX
            _PRINTLATEX = True
            _PRINTNUM = True
        elif arg == '-printlyx' and not _PRINTLYX:
            assert not _PRINTLATEX
            _PRINTLYX = True
            _PRINTNUM = True
        elif arg == '-printnum' and not _PRINTNUM:
            _PRINTNUM = True
        elif os.access(arg, os.F_OK):
            # Input file
            if override_stdin:
                printstderr("You seem to want to load two files, which I can not.")
                printstderr()
                usagefail()

            sys.stdin = open(arg)
        elif '.cc' in arg:
            printstderr("You seem to want to load file {}, but it does not exist.".format(arg))
            printstderr()
            usagefail()
        else:
            printstderr("I do not understand this argument: " + repr(arg))
            printstderr()
            usagefail()

    _PRINTLATEXY = _PRINTLATEX or _PRINTLYX
    _PRINTVERBOSE = not _PRINTLATEXY

    verbose = sys.stdin.isatty()

    if verbose:
        printstderr("cc.py started. Please input definitions and terms, and end them with enter.")
        printstderr()

    runfile(inputfile=sys.stdin, verbose=verbose,
            printout=printstdout, printerr=printstderr)

def runfile(inputfile, verbose, printout, printerr):
    try:
        line = ''
        while True:
            if not line:
                # Read a new line
                line = inputfile.readline()
                if not line:
                    raise EOFError()
                line = line.strip()
            if line.startswith("#") or line == "":
                line = None
                continue
            file = buffer.BufferReader(io.StringIO(tounicode(line)))
            try:
                tag, thing = readtermorrule(file)
            except EOFError:
                printerr("Premature end of line?")
                line = None
                continue
            leftover = file.unreadbuf + file.source.read()
            if leftover.startswith(r'\\'):
                # Do the rest also.
                line = leftover[2:]
            elif leftover and not leftover.isspace():
                printerr("Error: trailing garbage: " + repr(leftover))
                line = ''
                continue
            else:
                line = ''
            dostuffwith(tag, thing, verbose, printout, printerr)
    except EOFError:
        # import traceback
        # traceback.print_exc()
        if verbose:
            printerr("Quitting.")

class Term(object):
    __slots__ = ['name', 'arguments']

    def __init__(self, name, arguments=None):
        if arguments == None:
            arguments = []
        # assert isinstance(name, str)
        # assert isinstance(arguments, list)
        self.name = name
        self.arguments = arguments

    def __str__(self):
        """Format a term for human inspection."""
        # Try to find a natural in here.
        try:
            if (self.name == 'Zero' or self.name == 'S') and _PRINTNUM:
                return "%s" % (try_findnatterm(self),)
        except StopIteration:
            pass
        return self.name + ''.join("." +
                                   ("%s" if arg.arguments == [] else "(%s)") % (arg.__str__(),)
                                   for arg in self.arguments)

    def __repr__(self):
        return "<Term %s>" % self

def try_findnatterm(term):
    if term.name == 'Zero' and len(term.arguments) == 0:
        return 0
    elif term.name == 'S' and len(term.arguments) == 1:
        return 1 + try_findnatterm(term.arguments[0])
    else:
        raise StopIteration

_keywords = r"\spadesuit \place \star".split(' ')

def readterm(f, onlyname=False):
    # Read head term
    head = None
    # Special cases
    for keyword in _keywords:
        l = len(keyword)
        if f.peekornone(l) == keyword:
            head = f.read(len(keyword))
            break

    # Else, parse a normal variable or name. (This program doesn't distinguish.)
    if head == None:
        if not f.peek(1).isalnum() and f.peek(1) != '*':
            raise ValueError("term does not start with alnum: " % (repr(f.peek(1)),))
        head = f.read(1)
        char = f.peekornone(1) or ''
        while char.isalnum() or char in set("'_*{}"):
            head += char
            f.read(1)
            char = f.peekornone(1) or ''

    arguments = []
    if not onlyname:
        # Read dots followed by more terms
        while f.peekornone(1) == '.':
            f.read(1)
            if f.peek(1) == '(':
                f.read(1)
                arguments.append(readterm(f, False))
                if f.read(1) != ')':
                    raise ValueError("no closing paren?")
            else:
                arguments.append(readterm(f, True))

    return Term(head, arguments)

def readtermorrule(f):
    f.skiplinespace()

    # We have three syntaxes for rules:
    #
    # 1. \d{LHS}{RHS}
    # 2. LHS \u2192 RHS (Unicode arrow)
    # 3. LHS -> RHS
    #
    # If the line is a sole term, then we return the representation of that
    # term.

    if f.peekornone(3) == r"\d{":
        f.read(3)
        # Read a rule
        lhs = readterm(f)
        assert f.read(1) == "}"
        if f.peek(1) == "{":
            f.read(1)
            rhs = readterm(f)
            assert f.read(1) == "}"
        else:
            name = f.read(1)
            assert name.isalnum()
            rhs = Term(name)
        return ('RULE', Rule(lhs, rhs))
    else:
        term = readterm(f)
        f.skiplinespace()
        if f.peekornone(1) == unichr(0x2192):
            # Shorthand for ->
            f.read(1)
            f.unread("->")
        if f.peekornone(2) == '->':
            f.read(2)
            lhs = term
            f.skiplinespace()
            rhs = readterm(f)
            return ('RULE', Rule(lhs, rhs))
        else:
            return ('TERM', term)

class Rule(object):
    __slots__ = ['lhs', 'rhs']
    def __init__(self, lhs, rhs):
        # assert isinstance(lhs, Term)
        # LHS must be flat
        assert all(var.arguments == [] for var in lhs.arguments)
        assert allunique([var.name for var in lhs.arguments])
        # assert isinstance(rhs, Term)
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return "%s -> %s" % (self.lhs, self.rhs)
    def __repr__(self):
        return "<Rule %s>" % (self,)

def allunique(l):
    return len(l) == len(set(l))

def dostuffwith(tag, thing, verbose, printout, printerr):
    """Given a rule, install or overwrite it. Given a term, reduce it as far as possible.

    tag = 'RULE' or 'TERM'. Variable thing is then the rule or the term.
    """

    if tag == 'RULE':
        if thing.lhs.name not in _defs:
            if _PRINTVERBOSE: 
                printerr("  Installing %s." % (thing,))
        else:
            if _PRINTVERBOSE: 
                printerr("  Overwriting %s." % (thing,))
        _defs[thing.lhs.name] = thing
    else:
        term = thing
        printout(("%s" if not _PRINTLATEXY else r" & \mathit{%s}\\") % (term,),
                 end=('\n' if not _PRINTLYX else ''))
        while term.name in _defs:
            # Rewrite this term
            try:
                term = rewrite(term, _defs[term.name])
                printout(("-> %s" if not _PRINTLATEXY else r"\rightarrow & \mathit{%s}\\") % (term,),
                         end=('\n' if not _PRINTLYX else ''))
            except ReductionFail as e:
                printerr("Reduction failed to continue: %s" % (e,))
                return
        if _PRINTLYX: printout("(end)")
        printerr("Reduction complete." if not _PRINTLATEX else "\\\\")

def rewrite(term, rule):
    """Rewrite a term using a rule."""
    lhs = rule.lhs
    rhs = rule.rhs

    assert term.name == lhs.name

    # Look up the variables.
    arity = len(lhs.arguments)
    length = len(term.arguments)
    if length < arity:
        raise ReductionFail("incomplete term (%s<%s)" % (length, arity))
    if length > arity:
        raise ReductionFail("invalid term (%s>%s)" % (length, arity))
    assert len(term.arguments) == len(lhs.arguments)
    vars = dict((lhsarg.name, subterm) for (lhsarg, subterm) in zip(lhs.arguments, term.arguments))

    # Substitute in the RHS
    def subst(subterm):
        if subterm.name in vars:
            base = vars[subterm.name]
        else:
            base = Term(subterm.name, [])

        return Term(base.name, base.arguments + [subst(subpart) for subpart in subterm.arguments])
    return subst(rhs)

if __name__ == '__main__':
    main()
