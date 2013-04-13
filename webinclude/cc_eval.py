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

import cc, io
cc._PRINTNUM = True

ncustomfiles = 0

FIBCC = """
Zero.z.s -> z
S.m.z.s -> s.m
Nil.ifempty.iflist -> ifempty
Cons.n.l.ifempty.iflist -> iflist.n.l

# Call-by-value

AddCBV.x.y.r -> x.(r.y).(AddCBV'.y.r)
AddCBV'.y.r.x -> AddCBV.x.(S.y).r

FibCBV.x.r -> x.(r.Zero).(FibCBV_1.r)
FibCBV_1.r.y -> y.(r.(S.Zero)).(FibCBV_2.r.y)
FibCBV_2.r.y.y' -> FibCBV.y.(FibCBV_3.r.y')
FibCBV_3.r.y'.fib_{y} -> FibCBV.y'.(FibCBV_4.r.fib_{y})
FibCBV_4.r.fib_{y}.fib_{y'} -> AddCBV.fib_{y}.fib_{y'}.r

# Call-by-name

AddCBN.x.y.z.s -> x.(y.z.s).(AddCBN'.y.s)
AddCBN'.y.s.x' -> s.(AddCBN.x'.y)

FibCBN.x.z.s -> x.z.(FibCBN_1.z.s)
FibCBN_1.z.s.y -> y.(s.Zero).(FibCBN_2.z.s.y)
FibCBN_2.z.s.y.y' -> AddCBN.(FibCBN.y).(FibCBN.y').z.s

# To see fib(6) = 8:
FibCBV.(S.(S.(S.(S.(S.(S.Zero)))))).fr
""".strip()


files = [("First Example", FIBCC)]

inputArea = None
outputPanel = None

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
    contents = files[0][1]
    inputArea.setText(contents)
    inputArea.setVisibleLines(len(splitlines(contents)))
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
    outputPanel.clear()
    outputPanel.add(Label(text))
    outputPanel.setStyleName("meta")

def showOutput(output):
    output = output.strip()
    if output:
        outputPanel.clear()
        outputPanel.add(newlinesLabel(output))
        # outputPanel.add(Label(output))
        outputPanel.setStyleName("proper")
    else:
        showOutputMeta("No output.")

def reduce(sender):
    """When the Reduce button is pressed: call cc.runfile with our input."""

    showOutputMeta("Reducing...")

    input = inputArea.getText()
    output = ""
    def catchoutput(s, end="\n"):
        output += s + end

    cc._defs = dict()
    try:
        cc.runfile(inputfile=io.StringIO(input), verbose=True,
                   printout=catchoutput, printerr=catchoutput)
    except Exception, e:
        Window.alert(e)

    showOutput(output)

if __name__ == '__main__':
    b = Button("Reduce", reduce)
    RootPanel("buttons").add(b)
    RootPanel("file-chooser").add(makeFileChooser())
    RootPanel("loading-notify").setVisible(False)
    inputArea = TextArea(VisibleLines=5, CharacterWidth=80)
    RootPanel("input").add(inputArea)
    outputPanel = RootPanel("output")
    showOutputMeta("Output will appear here. It takes a few seconds to calculate a long reduction.")
    loadFile('called from main')
    b.setFocus(True)
