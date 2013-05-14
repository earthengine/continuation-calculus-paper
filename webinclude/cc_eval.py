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
from pyjamas.ui.DisclosurePanel import DisclosurePanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.Timer import Timer
from pyjamas import Window, DOM

import cc, examples, io, functools
cc._PRINTNUM = True

BEGINMESSAGES = [HTML(s.strip()) for s in [
"""
<p>Output will appear here. It takes a few seconds to calculate a long
reduction.</p>
""", """
<p>This script evaluates continuation calculus or CC, a variant of lambda
calculus. A submitted paper by Bram Geron and <a
href="http://www.cs.ru.nl/~herman/">Herman Geuvers</a> argues that CC is a
suitable formalism for modeling programs with control, and for
mixing call-by-value and call-by-name code.</p>
""", """
<p>Created with <a href='http://pyjs.org/'>pyjs</a>.</p>
"""]]

# not functional yet
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
    showOutputMeta("Press Reduce to see output here.")
    pass

def showOutputMeta(message, iswidgetlist=False):
    """Clear outputPanel and show information in it."""
    outputPanel.clear()
    if iswidgetlist:
        for m in message:
            outputPanel.add(m)
    else:
        outputPanel.add(Label(message))
    outputPanel.setStyleName("meta")

def showOutput(output, extra=None, nlHTML="<br>"):
    """Clear outputPanel and show newline-separated output in it.

    The following types of lines will be parsed differently:

    - A sequence of "-> term", "-> term" will get a DisclosurePanel.
    - Definitions will be collapsed in a DisclosurePanel.

    If extra is set, then append that widget."""

    lines = splitlines(output.strip())
    if lines:
        outputPanel.clear()
        fp = FlowPanel()
        outputPanel.add(fp)

        # Add content to the FlowPanel

        # We distinguish a number of line groups:
        # 
        # 0: no special handling.
        # 1: definition group
        # 2: reduction group

        curgroup = 0
        curgroupwidgets = []
        curgrouphead = None
        RARROW=chr(0x2192)
        def fixarrow(line):
            return line
        def addline(line):
            global curgroup, curgroupwidgets, curgrouphead, fp
            line = line.strip()
            line = line.replace("->", RARROW)
            if line.startswith("Installing "):
                # New group: 1
                if curgroup != 1: finishgroup()
                curgroup = 1
                curgroupwidgets.append(Label(line))
            elif line.startswith(RARROW):
                # New group: 2.
                if curgroup == 0:
                    # The last line is still stored in curgroupwidgets. We use
                    # it as the DisclosurePanel head.
                    assert curgrouphead == None
                    if curgroupwidgets == []:
                        curgrouphead = "unknown reduction"
                    else:
                        assert len(curgroupwidgets) == 1
                        curgrouphead = curgroupwidgets[0].getText()
                        curgroupwidgets = []
                elif curgroup != 2:
                    finishgroup()
                curgroup = 2
                curgroupwidgets.append(Label(line))
                # Window.alert(curgroupwidgets)
            else:
                # New group: 0
                finishgroup()
                curgroup = 0
                curgroupwidgets = [Label(line)]
        def finishgroup():
            global curgroup, curgroupwidgets, curgrouphead, fp
            if curgroup == 0:
                for widget in curgroupwidgets:
                    fp.add(widget)
            elif curgroup == 1:
                dp = DisclosurePanel("Definitions")
                dpflow = FlowPanel()
                dp.add(dpflow)
                for widget in curgroupwidgets:
                    dpflow.add(widget)
                fp.add(dp)
            elif curgroup == 2:
                curgrouphead += " (%s steps)" % (len(curgroupwidgets),)
                dp = DisclosurePanel(curgrouphead)
                dpflow = FlowPanel()
                dp.add(dpflow)
                for widget in curgroupwidgets[:-1]:
                    dpflow.add(widget)
                fp.add(dp)
                fp.add(curgroupwidgets[-1])
            curgroup = 0
            curgroupwidgets = []
            curgrouphead = None

        for line in lines:
            addline(line)
        finishgroup()

        # fp.add(InlineLabel(lines[0]))
        # for line in lines[1:]:
        #     fp.add(InlineHTML(nlHTML))
        #     fp.add(InlineLabel(line))

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

def queuereduce(sender, maxlines=1000):
    showOutputMeta("Reducing...")

    outputPanel.add(HTML("&nbsp;"))
    outputPanel.add(HTML("&nbsp;"))
    outputPanel.add(HTML("""
    <p>Takes too long? Try the <a href="https://bitbucket.org/bgeron
    </continuation-calculus-paper/">Python evaluator.</a>.</p>
    """.strip()))

    # Schedule reduceterm(maxlines) really soon.
    timer = Timer(notify=functools.partial(reduceterm, maxlines=maxlines))
    timer.schedule(50) # after 50 milliseconds

def reduceterm(sender, maxlines):
    """When the Reduce button is pressed: call cc.runfile with our input.

    There is a maximum number of lines that we will output, to prevent a
    stalling browser and an overfull document. The user can raise this limit
    with a link.
    """

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
        cc.runfile(inputfile=io.StringIO(input), verbose=False,
                   printout=catchoutput, printerr=catchoutput)
    except OverlongOutput:
        extra = FlowPanel(StyleName="terminated")
        extra.add(InlineLabel("Reduction terminated after %s lines. " % (maxlines,)))
        extra.add(Button("Try longer", functools.partial(queuereduce, maxlines=nextmaxlines(maxlines))))
        showOutput(output, extra=extra)
    except Exception, e:
        Window.alert(e)
    else:
        showOutput(output)

def nextmaxlines(prevmaxlines):
    """Makes the sequence 1, 3, 10, 30, 100, 300, ... . That is, when fed with
    a number in that sequence, return the next number.

    This function is used to make buttons for allowing more computation time,
    step by step, in reduceterm().    
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
    b = Button("Reduce", queuereduce)
    RootPanel("buttons").add(b)
    fileChooser = makeFileChooser()
    RootPanel("file-chooser").add(fileChooser)
    RootPanel("loading-notify").setVisible(False)
    inputArea = TextArea(VisibleLines=5, CharacterWidth=80)
    RootPanel("input").add(inputArea)
    outputPanel = RootPanel("output")
    loadFile('called from main')
    showOutputMeta(BEGINMESSAGES, iswidgetlist=True)
    b.setFocus(True)
