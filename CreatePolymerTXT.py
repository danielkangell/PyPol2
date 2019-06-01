import numpy as np
import sys
import os

argv = sys.argv
if len(argv) != 4:
  print("Syntax: please write Monomercount LatSize and MonomerDistance")
  sys.exit()

use = sys.argv[1:]

def generateYs(x,z,MonDistance):
    """
    decomposed function to generate a list of y values so that each point is, on average, mondistance apart
    """
    y = [np.random.normal(5,1)]
    for i in range(1,len(x)):
        dist = np.random.normal(MonDistance,MonDistance/5)
        xsquared = (x[i]-x[i-1])*(x[i]-x[i-1])
        zsquared = (z[i]-z[i-1])*(z[i]-z[i-1])
        if dist*dist-xsquared-zsquared > 0 : needed = np.sqrt(dist*dist-xsquared-zsquared)
        else : needed = 0
        y.append(y[i-1] + needed)
    return y

def writeHeader(MonomerCount = 50, latsize = 100):
    """
    generates the header for the polymer file based on (n) the number of atoms
    output is a string, 
    
    input MonomerCount is an interger
    Latsize is an interger or float, default is 100 
    """
    header = ""
    header += "{}\tatoms\n".format(MonomerCount)
    header += "{}\tbonds\n".format(MonomerCount -1)
    header += "{}\tangles\n".format(MonomerCount -2)
    header += "{}\tdihedrals\n".format(MonomerCount -3)
     
    header += "1\tatom types\n"
    header += "1\tbond types\n"
    header += "1\tangle types\n"
    header += "1\tdihedral types\n"

    header += "0.0000\t{} xlo xhi\n".format(latsize)
    header += "0.0000\t{} ylo yhi\n".format(latsize)
    header += "0.0000\t{} zlo zhi\n".format(latsize)  
    return header

def writeMasses(mass):
    masses = ""
    masses += "Masses\n"

    masses += "\t1\t{}".format(mass)
    return masses

def writeAtoms(MonomerCount = 50, MonDistance = 2.3, latsize = 100):
    """
    As of right now this function really only works if MonomerCount < latsize
    although we can change the algorithm in the future
    output is the string input of Atoms for Lammps
    
    MonomerCount ... interger number of monomers in the polymer
    Mon distance ... is an int or float and the average spacing between monomer units
    Latsize ... is an int or float is the lattice size
    
    """
    z = np.random.normal(latsize/2,.2,MonomerCount)
    x = [np.random.normal(5,1)]
    for i in range(1,MonomerCount):
        x.append(x[i-1] + np.random.normal(np.sqrt(MonDistance),.3))
    y = generateYs(x,z,MonDistance)
    atoms = ""
    atoms += "Atoms\n"
    for i in range(MonomerCount):
        atoms += "\t{}\t1\t1\t{}\t{}\t{}\n".format(i+1,x[i],y[i],z[i])
    return atoms

def writeBonds(MonomerCount = 50):
    bonds = "Bonds\n"
    for i in range(MonomerCount-1):
        bonds += "\t{}\t{}\t{}\t{}\n".format(i+1,1,i+1,i+2)
    return bonds

def writeAngles(MonomerCount = 50):
    angles = "Angles\n"
    for i in range(MonomerCount-2):
        angles += "\t{}\t{}\t{}\t{}\t{}\n".format(i+1,1,i+1,i+2,i+3)
    return angles

def writeDihedrals(MonomerCount = 50):
    dihedrals = "Dihedrals\n"
    for i in range(MonomerCount-3):
        dihedrals += "\t{}\t{}\t{}\t{}\t{}\t{}\n".format(i+1,1,i+1,i+2,i+3,i+4)
    return dihedrals


def compileString(MonomerCount = 50 , latsize = 100, MonDistance=2.3):
    """
    Creates a txt file in the parent folder /// this should be modified to call in system arguments 
    """
    
    finalString = ""
    finalString += writeHeader(MonomerCount, latsize)
    finalString += "\n"
    finalString += writeMasses(14)
    finalString += "\n"
    finalString += writeAtoms(MonomerCount,MonDistance,latsize)
    finalString += "\n"
    finalString += writeBonds()
    finalString += "\n"
    finalString += writeAngles()
    finalString += "\n"
    finalString += writeDihedrals()
    
    with open(os.getcwd()+'/polyinfo.txt', "w") as text_file:
        text_file.write(finalString)

compileString(int(use[0]),float(use[1]),float(use[2]))
