from Tkinter import *
from ttk import *
import stochasticGrammar, stepwise
    
root = Tk()
root.title("L-System and Bangleizer")

"""destroy window and kill program"""
def closeWindow():
	root.destroy()

mainframe = Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

"""12 tone entry scheme"""
r1e1 = IntVar()
r1e2 = IntVar()
r2e1 = IntVar()
r2e2 = IntVar()
r3e1 = IntVar()
r3e2 = IntVar()
r4e1 = IntVar()
r4e2 = IntVar()
r5e1 = IntVar()
r5e2 = IntVar()
r6e1 = IntVar()
r6e2 = IntVar()
r7e1 = IntVar()
r7e2 = IntVar()
r8e1 = IntVar()
r8e2 = IntVar()
r9e1 = IntVar()
r9e2 = IntVar()
r10e1 = IntVar()
r10e2 = IntVar()
r11e1 = IntVar()
r11e2 = IntVar()
r12e1 = IntVar()
r12e2 = IntVar()
PC0 = Label(mainframe, text="PC 0 Rules").grid(column=2, row=3, sticky=(W,E))
rule1entry1 = Entry(mainframe, width=7, textvariable=r1e1).grid(column=3, row=3, sticky=(W,E))
rule1entry2 = Entry(mainframe, width=7, textvariable=r1e2).grid(column=4, row=3, sticky=(W,E))
PC1 = Label(mainframe, text="PC 1 Rules").grid(column=2, row=4, sticky=(W,E))
rule2entry1 = Entry(mainframe, width=7, textvariable=r2e1).grid(column=3, row=4, sticky=(W,E))
rule2entry2 = Entry(mainframe, width=7, textvariable=r2e2).grid(column=4, row=4, sticky=(W,E))
PC2 = Label(mainframe, text="PC 2 Rules").grid(column=2, row=5, sticky=(W,E))
rule3entry1 = Entry(mainframe, width=7, textvariable=r3e1).grid(column=3, row=5, sticky=(W,E))
rule3entry2 = Entry(mainframe, width=7, textvariable=r3e2).grid(column=4, row=5, sticky=(W,E))
PC3 = Label(mainframe, text="PC 3 Rules").grid(column=2, row=6, sticky=(W,E))
rule4entry1 = Entry(mainframe, width=7, textvariable=r4e1).grid(column=3, row=6, sticky=(W,E))
rule4entry2 = Entry(mainframe, width=7, textvariable=r4e2).grid(column=4, row=6, sticky=(W,E))
PC4 = Label(mainframe, text="PC 4 Rules").grid(column=2, row=7, sticky=(W,E))
rule5entry1 = Entry(mainframe, width=7, textvariable=r5e1).grid(column=3, row=7, sticky=(W,E))
rule5entry2 = Entry(mainframe, width=7, textvariable=r5e2).grid(column=4, row=7, sticky=(W,E))
PC5 = Label(mainframe, text="PC 5 Rules").grid(column=2, row=8, sticky=(W,E))
rule6entry1 = Entry(mainframe, width=7, textvariable=r6e1).grid(column=3, row=8, sticky=(W,E))
rule6entry2 = Entry(mainframe, width=7, textvariable=r6e2).grid(column=4, row=8, sticky=(W,E))
PC6 = Label(mainframe, text="PC 6 Rules").grid(column=2, row=9, sticky=(W,E))
rule7entry1 = Entry(mainframe, width=7, textvariable=r7e1).grid(column=3, row=9, sticky=(W,E))
rule7entry2 = Entry(mainframe, width=7, textvariable=r7e2).grid(column=4, row=9, sticky=(W,E))
PC7 = Label(mainframe, text="PC 7 Rules").grid(column=2, row=10, sticky=(W,E))
rule8entry1 = Entry(mainframe, width=7, textvariable=r8e1).grid(column=3, row=10, sticky=(W,E))
rule8entry2 = Entry(mainframe, width=7, textvariable=r8e2).grid(column=4, row=10, sticky=(W,E))
PC8 = Label(mainframe, text="PC 8 Rules").grid(column=2, row=11, sticky=(W,E))
rule9entry1 = Entry(mainframe, width=7, textvariable=r9e1).grid(column=3, row=11, sticky=(W,E))
rule9entry2 = Entry(mainframe, width=7, textvariable=r9e2).grid(column=4, row=11, sticky=(W,E))
PC9 = Label(mainframe, text="PC 9 Rules").grid(column=2, row=12, sticky=(W,E))
rule10entry1 = Entry(mainframe, width=7, textvariable=r10e1).grid(column=3, row=12, sticky=(W,E))
rule10entry2 = Entry(mainframe, width=7, textvariable=r10e2).grid(column=4, row=12, sticky=(W,E))
PC10 = Label(mainframe, text="PC 10 Rules").grid(column=2, row=13, sticky=(W,E))
rule11entry1 = Entry(mainframe, width=7, textvariable=r11e1).grid(column=3, row=13, sticky=(W,E))
rule11entry2 = Entry(mainframe, width=7, textvariable=r11e2).grid(column=4, row=13, sticky=(W,E))
PC11 = Label(mainframe, text="PC 11 Rules").grid(column=2, row=14, sticky=(W,E))
rule12entry1 = Entry(mainframe, width=7, textvariable=r12e1).grid(column=3, row=14, sticky=(W,E))
rule12entry2 = Entry(mainframe, width=7, textvariable=r12e2).grid(column=4, row=14, sticky=(W,E))
Button(mainframe, text="Enter").grid(column=3, row=15, sticky=(W,E))

SG = stochasticGrammar.grammar(0.5)

def assignPC():
	SG.axiomOneReplacementOne = r1e1
	SG.axiomOneReplacementTwo = r1e2
	SG.axiomTwoReplacementOne = r2e1
	SG.axiomTwoReplacementTwo = r2e2
	SG.axiomThreeReplacementOne = r3e1
	SG.axiomThreeReplacementTwo = r3e2
	SG.axiomFourReplacementOne = r4e1
	SG.axiomFourReplacementTwo = r4e2
	SG.axiomFiveReplacementOne = r5e1
	SG.axiomFiveReplacementTwo = r5e2
	SG.axiomSixReplacementOne = r6e1
	SG.axiomSixReplacementTwo = r6e2
	SG.axiomSevenReplacementOne = r7e1
	SG.axiomSevenReplacementTwo = r7e2
	SG.axiomEightReplacementOne = r8e1
	SG.axiomEightReplacementTwo = r8e2
	SG.axiomNineReplacementOne = r9e1
	SG.axiomNineReplacementTwo = r9e2
	SG.axiomTenReplacementOne = r10e1
	SG.axiomTenReplacementTwo = r10e2
	SG.axiomElevenReplacementOne = r11e1
	SG.axiomElevenReplacementTwo = r11e2
	SG.axiomTwelveReplacementOne = r12e1
	SG.axiomTwelveReplacementTwo = r12e2	

"""modal tone entry scheme"""
#FIXME: root pitch and/or key changes
#perhaps an entry for starting pitch, entry for mode?
#entries perhaps in steps instead of actual pc?
s1r1 = StringVar()
s1r2 = StringVar()
s2r1 = StringVar()
s2r2 = StringVar()
s3r1 = StringVar()
s3r2 = StringVar()
s4r1 = StringVar()
s4r2 = StringVar()
s5r1 = StringVar()
s5r2 = StringVar()
s6r1 = StringVar()
s6r2 = StringVar()
s7r1 = StringVar()
s7r2 = StringVar()
step1 = Label(mainframe, text="Step 1 Rules").grid(column=5, row=3, sticky=(W,E))
rule1entry1 = Entry(mainframe, width=7, textvariable=s1r1).grid(column=6, row=3, sticky=(W,E))
rule1entry2 = Entry(mainframe, width=7, textvariable=s1r2).grid(column=7, row=3, sticky=(W,E))
step2 = Label(mainframe, text="Step 2 Rules").grid(column=5, row=4, sticky=(W,E))
rule2entry1 = Entry(mainframe, width=7, textvariable=s2r1).grid(column=6, row=4, sticky=(W,E))
rule2entry2 = Entry(mainframe, width=7, textvariable=s2r2).grid(column=7, row=4, sticky=(W,E))
step3 = Label(mainframe, text="Step 3 Rules").grid(column=5, row=5, sticky=(W,E))
rule3entry1 = Entry(mainframe, width=7, textvariable=s3r1).grid(column=6, row=5, sticky=(W,E))
rule3entry2 = Entry(mainframe, width=7, textvariable=s3r2).grid(column=7, row=5, sticky=(W,E))
step4 = Label(mainframe, text="Step 4 Rules").grid(column=5, row=6, sticky=(W,E))
rule4entry1 = Entry(mainframe, width=7, textvariable=s4r1).grid(column=6, row=6, sticky=(W,E))
rule4entry2 = Entry(mainframe, width=7, textvariable=s4r2).grid(column=7, row=6, sticky=(W,E))
step5 = Label(mainframe, text="Step 5 Rules").grid(column=5, row=7, sticky=(W,E))
rule5entry1 = Entry(mainframe, width=7, textvariable=s5r1).grid(column=6, row=7, sticky=(W,E))
rule5entry2 = Entry(mainframe, width=7, textvariable=s5r2).grid(column=7, row=7, sticky=(W,E))
step6 = Label(mainframe, text="Step 6 Rules").grid(column=5, row=8, sticky=(W,E))
rule6entry1 = Entry(mainframe, width=7, textvariable=s6r1).grid(column=6, row=8, sticky=(W,E))
rule6entry2 = Entry(mainframe, width=7, textvariable=s6r2).grid(column=7, row=8, sticky=(W,E))
step7 = Label(mainframe, text="Step 7 Rules").grid(column=5, row=9, sticky=(W,E))
rule7entry1 = Entry(mainframe, width=7, textvariable=s7r1).grid(column=6, row=9, sticky=(W,E))
rule7entry2 = Entry(mainframe, width=7, textvariable=s7r2).grid(column=7, row=9, sticky=(W,E))
Button(mainframe, text="Enter").grid(column=6, row=10, sticky=(W,E))

SWG = stepwise.stepwiseGrammar(0.5)

def assignSteps():
	SWG.A1R1 = s1r1
	SWG.A1R2 = s1r2
	SWG.A2R1 = s2r1
	SWG.A2R2 = s2r2
	SWG.A3R1 = s3r1
	SWG.A3R2 = s3r2
	SWG.A4R1 = s4r1
	SWG.A4R2 = s4r2
	SWG.A5R1 = s5r1
	SWG.A5R2 = s5r2
	SWG.A6R1 = s6r1
	SWG.A6R2 = s6r2
	SWG.A7R1 = s7r1
	SWG.A7R2 = s7r2

"""pitch field entry scheme"""
ruleLabel = Label(mainframe, text="Rule for Field:").grid(column=8, row=3, sticky=(W,E))
PFRule = StringVar()
pitchFieldRule = Entry(mainframe, width=20, textvariable=PFRule).grid(column=9, row=3, sticky=(W,E))
SPLabel = Label(mainframe, text="Starting Pitch:").grid(column=8, row=4, sticky=(W,E))
startPC = IntVar()
startPitch = Entry(mainframe, width=5, textvariable=startPC).grid(column=9, row=4, sticky=(W,E))

#Quit Button
Button(mainframe, text="Quit", command=closeWindow).grid(column=3, row=40, sticky=(W,E))

root.mainloop()