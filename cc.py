#!/usr/bin/env python3

import sys, buffer, io, os

_defs = dict() # stores rules

if False: print("Sorry, you must run cc.py using Python 3.", file=None)

def printerr(*args, **kw):
    "Print to standard error."
    return print(*args, file=sys.stderr, **kw)

def usage():
    printerr("Usage:")
    printerr("    python3 cc.py [-printnum|-printlatex|-printlyx]")

# defaults to be overridden in main()
_PRINTNUM = False # convert (S.(S.Zero)) to 2?
_PRINTLATEX = False # whether to output pure latex
_PRINTLYX = False # whether to output for LyX math array mode
_PRINTLATEXY = False # = printlatex or printlyx
_PRINTVERBOSE = True # = not printlatexy

def main():
    global _PRINTLATEX, _PRINTLYX, _PRINTNUM, _PRINTLATEXY, _PRINTVERBOSE
    if (len(sys.argv) > 1
           and sys.argv[1] == '-printlatex'
           and not _PRINTLATEX):
        del sys.argv[1]
        assert not _PRINTLYX
        _PRINTLATEX = True
        _PRINTNUM = True
    if (len(sys.argv) > 1
           and sys.argv[1] == '-printlyx'
           and not _PRINTLYX):
        del sys.argv[1]
        assert not _PRINTLATEX
        _PRINTLYX = True
        _PRINTNUM = True
    if (len(sys.argv) > 1
           and sys.argv[1] == '-printnum'
           and not _PRINTNUM):
        del sys.argv[1]
        _PRINTNUM = True
    if len(sys.argv) != 1:
        usage()
        sys.exit(1)

    _PRINTLATEXY = _PRINTLATEX or _PRINTLYX
    _PRINTVERBOSE = not _PRINTLATEXY

    verbose = sys.stdin.isatty()

    if verbose:
        printerr("cc.py started. Please input definitions and terms, and end them with enter.")

    try:
        line = ''
        while True:
            if not line:
                # Read a new line
                line = sys.stdin.readline()
                if not line:
                    raise EOFError
                line = line.strip()
            if line.startswith("#"):
                line = None
                continue
            file = buffer.BufferReader(io.StringIO(line))
            try:
                thing = readtermorrule(file)
            except EOFError:
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
            dostuffwith(thing, verbose)
    except EOFError:
        # import traceback
        # traceback.print_exc()
        if verbose:
            printerr("Quitting.")

_keywords = r"\spadesuit \place \star".split(' ')

def readterm(f, onlyname=False):
    # Read head term
    head = None
    # Special cases
    for keyword in _keywords:
        if f.peekornone(len(keyword)) == keyword:
            head = f.read(len(keyword))
            break

    # Else, parse a normal variable or name. (This program doesn't distinguish.)
    if head == None:
        if not f.peek(1).isalnum() and f.peek(1) != '*':
            raise ValueError("term does not start with alnum: {}".format(repr(f.peek(1))))
        head = f.read(1)
        char = f.peekornone(1) or ''
        while char.isalnum() or char in set("'_*{}"):
            head += char
            f.read(1)
            char = f.peekornone(1) or ''

    if onlyname:
        return head

    # Read dots followed by more terms
    restterms = []
    while f.peekornone(1) == '.':
        f.read(1)
        if f.peek(1) == '(':
            f.read(1)
            restterms.append(readterm(f, False))
            if f.read(1) != ')':
                raise ValueError("no closing paren?")
        else:
            restterms.append(readterm(f, True))

    if restterms:
        return [head] + restterms
    else:
        return head

def readtermorrule(f):
    f.skiplinespace()

    if f.peekornone(3) == r"\d{":
        f.read(3)
        # Read a rule
        lhs = readterm(f)
        assert islhs(lhs)
        assert f.read(1) == "}"
        if f.peek(1) == "{":
            f.read(1)
            rhs = readterm(f)
            assert f.read(1) == "}"
        else:
            rhs = f.read(1)
            assert rhs.isalnum()

        return makerule(lhs, rhs)
    else:
        term = readterm(f)
        f.skiplinespace()
        if f.peekornone(1) == '→':
            # Shorthand for ->
            f.read(1)
            f.unread("->")
        if f.peekornone(2) == '->':
            f.read(2)
            lhs = term
            f.skiplinespace()
            rhs = readterm(f)
            return makerule(lhs, rhs)
        else:
            return term

def makerule(lhs, rhs):
    if not allunique(listify(lhs)[1:]):
        raise ValueError("repeated variable in lhs")
    return ['RULE', lhs, rhs]

def allunique(l):
    return len(l) == len(set(l))

def format_termorrule(thing):
    """Serialize a thing or rule for human reading."""
    if thing == 'Zero' and _PRINTNUM:
        return '0'
    if isinstance(thing, str):
        return thing
    else:
        assert isinstance(thing, list) and list
        if isrule(thing):
            return "{} -> {}".format(format_termorrule(thing[1]), format_termorrule(thing[2]))
        else:
            try:
                if _PRINTNUM: return str(try_findnatterm(thing))
            except StopIteration:
                pass
            
            return ".".join(formatted if '.' not in formatted
                            else '({})'.format(formatted)
                            for formatted in map(format_termorrule, thing))

def try_findnatterm(thing):
    # ugly!
    if thing == 'Zero':
        return 0
    elif not isinstance(thing, list) or not len(thing) == 2 or thing[0] != 'S':
        raise StopIteration
    else:
        return 1 + try_findnatterm(thing[1])

def islhs(term):
    return isinstance(term, list) and all(isinstance(part, str) for part in term)

def isrule(thing):
    if isinstance(thing, list) and thing[0] == 'RULE':
        assert len(thing) == 3
        return True
    else:
        return False

def headof(thing):
    """Can be given a LHS of a rule, or a term."""
    if isinstance(thing, str):
        return thing
    else:
        return thing[0]

def dostuffwith(thing, verbose):
    """Given a rule, install or overwrite it. Given a term, reduce it as far as possible."""
    if isrule(thing):
        if headof(thing[1]) not in _defs:
            if _PRINTVERBOSE: 
                printerr("  Installing {}.".format(format_termorrule(thing)))
        else:
            if _PRINTVERBOSE: 
                printerr("  Overwriting {}.".format(format_termorrule(thing)))
        _defs[headof(thing[1])] = thing
    else:
        term = thing
        print(("{}" if not _PRINTLATEXY else r" & \mathit{{{}}}\\")
              .format(format_termorrule(term)),
              end=('\n' if not _PRINTLYX else ''))
        while headof(term) in _defs:
            # Rewrite this term
            term = rewrite(term, _defs[headof(term)])
            print(("-> {}" if not _PRINTLATEXY else r"\rightarrow & \mathit{{{}}}\\")
                  .format(format_termorrule(term)),
                  end=('\n' if not _PRINTLYX else ''))
        if _PRINTLYX: print("(end)")
        printerr("Reduction complete." if not _PRINTLATEX else "\\\\")

def listify(thing):
    if isinstance(thing, list): return thing
    else: return [thing]

def unlistify(thing):
    assert isinstance(thing, list)
    if len(thing) == 1:
        return thing[0]
    else:
        return thing

def rewrite(term, rule):
    """Rewrite a term using a rule."""
    RULE, lhs, rhs = rule
    assert RULE == 'RULE'
    del RULE
    assert headof(term) == headof(lhs)

    # Strip off the head.
    term = term[1:]
    lhs = lhs[1:]

    # Look up the variables.
    assert len(term) == len(lhs)
    vars = dict(zip(lhs, term))

    # Substitute in the RHS
    def subst(subterm):
        subterm = listify(subterm)
        if subterm[0] in vars:
            head = vars[subterm[0]]
        else:
            head = subterm[0]
        result = listify(head) + [subst(subpart) for subpart in subterm[1:]]
        return unlistify(result)

    return subst(rhs)

if __name__ == '__main__':
    main()
