from pyjamas.ui.Button import Button
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.InlineLabel import InlineLabel
from pyjamas.ui.InlineHTML import InlineHTML
from pyjamas.ui.Label import Label
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas import Window, DOM

import cc, examples, io, functools
cc._PRINTNUM = True

ncustomfiles = 0

files = examples.predefined_files

inputArea = None
outputPanel = None
fileChooser = None

currentFileIndex = None

def splitlines(s):
    return s.split("\n")

def makeFileChooser():
    l = ListBox()
    for i, tup in enumerate(files):
        name, content = tup
        l.addItem(name, i)
    l.addChangeListener(loadFile)
    return l

def loadFile(sender):
    currentFileIndex = fileChooser.getSelectedIndex()
    assert currentFileIndex >= 0

    contents = files[currentFileIndex][1]
    inputArea.setText(contents)
    inputArea.setVisibleLines(max(10, len(splitlines(contents))))
    pass

def newlinesLabel(text, nlHTML="<br>"):
    """Make a FlowPanel with the specified text; broken up on newlines."""
    fp = FlowPanel()
    lines = splitlines(text)
    if lines == []: return fp
    fp.add(InlineLabel(lines[0]))
    for line in lines[1:]:
        fp.add(InlineHTML(nlHTML))
        fp.add(InlineLabel(line))
    return fp

def showOutputMeta(text):
    """Clear outputPanel and show information in it."""
    outputPanel.clear()
    outputPanel.add(Label(text))
    outputPanel.setStyleName("meta")

def showOutput(output, extra=None):
    """Clear outputPanel and show newline-separated output in it.

    If extra is set, then append that widget."""

    output = output.strip()
    if output:
        outputPanel.clear()
        outputPanel.add(newlinesLabel(output))
        if extra != None:
            outputPanel.add(extra)
        # outputPanel.add(Label(output))
        outputPanel.setStyleName("proper")
    else:
        showOutputMeta("No output.")

class OverlongOutput(Exception):
    """Signals that we have received too much output, and we want to quit the
    reduction computation."""
    pass

def reduce(sender=None, maxlines=300):
    """When the Reduce button is pressed: call cc.runfile with our input.

    There is a maximum number of lines that we will output, to prevent a
    stalling browser and an overfull document. The user can raise this limit
    with a link.
    """

    showOutputMeta("Reducing...")

    input = inputArea.getText()
    output = ""
    nlines = 0
    def catchoutput(s, end="\n"):
        output += s + end
        nlines += 1
        if nlines > maxlines:
            raise OverlongOutput()

    cc._defs = dict()
    try:
        cc.runfile(inputfile=io.StringIO(input), verbose=True,
                   printout=catchoutput, printerr=catchoutput)
    except OverlongOutput:
        extra = FlowPanel(StyleName="terminated")
        extra.add(InlineLabel("Reduction terminated after %s lines. " % (maxlines,)))
        extra.add(Button("Try longer", functools.partial(reduce, maxlines=nextmaxlines(maxlines))))
        showOutput(output, extra=extra)
    except Exception, e:
        Window.alert(e)
    else:
        showOutput(output)

def nextmaxlines(prevmaxlines):
    """Makes the sequence 1, 3, 10, 30, 100, 300, ... . That is, when fed with
    a number in that sequence, return the next number.

    This function is used to make buttons for allowing more computation time,
    step by step, in reduce().    
    """

    orders = 0
    while prevmaxlines >= 10:
        orders += 1
        prevmaxlines /= 10
    if prevmaxlines >= 3:
        maxlines = 10
    else:
        maxlines = 3
    for _ in range(orders):
        maxlines *= 10
    return maxlines

if __name__ == '__main__':
    b = Button("Reduce", reduce)
    RootPanel("buttons").add(b)
    fileChooser = makeFileChooser()
    RootPanel("file-chooser").add(fileChooser)
    RootPanel("loading-notify").setVisible(False)
    inputArea = TextArea(VisibleLines=5, CharacterWidth=80)
    RootPanel("input").add(inputArea)
    outputPanel = RootPanel("output")
    showOutputMeta("Output will appear here. It takes a few seconds to calculate a long reduction.")
    outputPanel.add(HTML("<p>Created with <a href='http://pyjs.org/'>pyjs</a>.</p>"))
    loadFile('called from main')
    b.setFocus(True)
