#solidworks api testing

import win32com.client
import pythoncom
swYearLastDigit = 4
sw = win32com.client.Dispatch("SldWorks.Application.%d" % (20+(swYearLastDigit-2)))  # e.g. 20 is SW2012,  23 is SW2015


model = sw.ActiveDoc
modelExt = model.Extension
selMgr = model.SelectionManager
featureMgr = model.FeatureManager
sketchMgr = model.SketchManager
eqMgr = model.GetEquationMgr

print("Equation 1 is: " + eqMgr.Equation(1))
eqMgr.Equation(1, "\"myVar\" = 42")
print("Equation 1 is now: " + eqMgr.Equation(1))

#sw.Rebuild(swForceRebuildAll)