import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import diffpy as dp
from diffpy.Structure import loadStructure

import sys
sys.path.append('/home/ben/mPDFmodules/mpdfcalculator')
from mcalculator import *

# Create the structure from our cif file, update the lattice params
structureFile = "MnO_R-3m.cif"
MnOStructure = loadStructure(structureFile)
lat=MnOStructure.lattice
lat.a,lat.b,lat.c=3.1505626,3.1505626,7.5936979
MnOStructure.lattice=lat

# Set up the mPDF calculator
mc=mPDFcalculator(struc=MnOStructure,magIdxs=[0,1,2],rmax=20.0,gaussPeakWidth=0.2)

mc.makeAtoms()
mc.svec=2.5*np.array([1,0,0])
mc.kvec=np.array([0,0,1.5])
mc.spinOrigin=mc.atoms[0]
mc.makeSpins()
mc.ffqgrid=np.arange(0,10,0.01)
mc.ff=jCalc(mc.ffqgrid,getFFparams('Mn2'))
mc.calcList=np.arange(1)

# Load the data
PDFfitFile='MnOfit_PDFgui.fgr'
rexp,Drexp=getDiffData([PDFfitFile])
mc.rmin=rexp.min()
mc.rmax=rexp.max()

# Do the refinement
def residual(p,yexp,mcalc):
    mcalc.paraScale,mcalc.ordScale=p
    return yexp-mcalc.calc(both=True)[2]

p0=[5.0,3.0]
pOpt=leastsq(residual,p0,args=(Drexp,mc))
print pOpt

fit=mc.calc(both=True)[2]

# Plot the results
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(rexp,Drexp,marker='o',mfc='none',mec='b',linestyle='none')
ax.plot(rexp,fit,'r-',lw=2)
ax.set_xlim(xmin=mc.rmin,xmax=mc.rmax)
ax.set_xlabel('r ($\AA$)')
ax.set_ylabel('d(r) ($\AA^{-2}$)')

plt.show()

