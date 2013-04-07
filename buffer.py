class BufferReader:

    """A strange file-like object, but you can peek from and unread to it. The
    data must come from a file object.

    This object is not thread-safe or something. Subject to race conditions and
    such. Just play normal please.

    WARNING this is a different thing than io.BufferedReader.
    """

    __slots__ = ['source', 'unreadbuf']

    def __init__(self, source):
        self.source = source
        self.unreadbuf = ''

    def read(self, maxlen=1):
        """Read at most maxlen bytes. Reads a byte by default."""
        found = ''
        # First, use the unread buffer if possible
        if 0 < maxlen < len(self.unreadbuf):
            # a prefix of the unread buffer is enough, use that
            found = self.unreadbuf[:maxlen]
            self.unreadbuf = self.unreadbuf[maxlen:]
            return found
        elif maxlen >= len(self.unreadbuf):
            # we can use all of it
            found = self.unreadbuf
            self.unreadbuf = ''
            maxlen -= len(found)
        # If that is not enough, use the source
        if maxlen >= 0:
            newdata = self.source.read(maxlen)
            found += newdata
        return found

    def unread(self, string):
        """Unread string, so it becomes available for the next read."""
        self.unreadbuf = string + self.unreadbuf

    def peek(self, length=1):
        """Peek what would be read, but don't remove the string from the
        imaginary stream."""
        string = self.read(length)
        self.unread(string)
        if len(string) != length: raise EOFError
        return string

    def peekornone(self, length=1):
        """Same as peek, but don't raise an exception on EOF. Return None
        instead."""
        try:
            return self.peek(length)
        except EOFError:
            return None

    def tell(self):
        return self.source.tell() - len(self.unreadbuf)

    def skiplinespace(self):
        """Skip whitespace on this line; return the whitespace."""
        space = ''
        while True:
            c = self.read(1)
            if len(c) == 0: # EOF
                return space
            if c.isspace() and c != '\n':
                # ok, read more whitespace
                space += c
            elif c == '#' and self.peek(1) == '#':
                # End a line with ## to continue on the following line.
                c = self.read(1) # skip second hash
                # Skip everything until and including newline
                while c != '\n':
                    c = self.read(1)
            else:
                # oops
                self.unread(c)
                return space

def spacenolf(c):
    return c.isspace() and c != '\n'