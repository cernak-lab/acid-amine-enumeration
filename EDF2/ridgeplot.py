import pickle
from rdkit import Chem
from rdkit.Chem import AllChem, Draw
import pandas as pd
from openpyxl import Workbook, load_workbook
from rdkit.Chem import rdMolDescriptors, Descriptors
import numpy as np
import numpy
import matplotlib
matplotlib.use('Agg')
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt
import seaborn as sns

def loader():
	wb = load_workbook(filename = "acid_amine_final_320_ionized.xlsx")
	sheet = wb['Sheet1']

	sanitized, failed = Sanitizer(sheet)

	minmax = getMinMax(sanitized)

	testBorn(sanitized, minmax)

def getMinMax(mols):
	logp = []
	qed = []
	mw = []
	psa = []
	fsp3 = []
	rotb = []
	fc = []
	hba = []
	hbd = []

	minmax = []

	for f in mols:
		logp.append(getLogP(f))
	print("logp", np.min(logp),np.max(logp))

	for f in mols:
		qed.append(getQED(f))
	print("qed", np.min(qed),np.max(qed))

	for f in mols:
		mw.append(getMW(f))
	print("mw", np.min(mw),np.max(mw))

	for f in mols:
		psa.append(getPSA(f))
	print("psa", np.min(psa),np.max(psa))

	for f in mols:
		fsp3.append(getFSP3(f))
	print("fsp3", np.min(fsp3),np.max(fsp3))

	for f in mols:
		rotb.append(getROTB(f))
	print("rotb", np.min(rotb),np.max(rotb))

	for f in mols:
		fc.append(getFC(f))
	print("fc", np.min(fc),np.max(fc))

	for f in mols:
		hba.append(getHBA(f))
	print("hba", np.min(hba),np.max(hba))

	for f in mols:
		hbd.append(getHBD(f))
	print("hbd", np.min(hbd),np.max(hbd))


	minmax.append((int(float(truncate(np.min(mw),0))),int(float(truncate(np.max(mw),0)))))
	minmax.append((float(truncate(np.min(logp),1)),float(truncate(np.max(logp),1))))
	minmax.append((int(float(truncate(np.min(hba),0))),int(float(truncate(np.max(hba),0)))))
	minmax.append((int(float(truncate(np.min(hbd),0))),int(float(truncate(np.max(hbd),0)))))
	minmax.append((float(truncate(np.min(psa),1)),float(truncate(np.max(psa),1))))
	minmax.append((float(truncate(np.min(fsp3),1)),float(truncate(np.max(fsp3),1))))
	minmax.append((int(float(truncate(np.min(rotb),0))),int(float(truncate(np.max(rotb),0)))))
	minmax.append((int(float(truncate(np.min(fc),0))),int(float(truncate(np.max(fc),0)))))
	minmax.append((float(truncate(np.min(qed),2)),float(truncate(np.max(qed),2))))


	print(minmax)
	return minmax

def label(x, color, label):
	ax = plt.gca()
	# ax.text(3.3,0.05,label,color="black",fontsize=16)
	ax.spines['bottom'].set_color('0.5')
	ax.spines['top'].set_color(None)
	ax.spines['right'].set_color('0.5')
	ax.spines['left'].set_color(None)


def xlabel(x, color, label):
    ax = plt.gca()
    ax.set_xlabel(3.3,0.05,label,color="black",fontsize=16)

def title_function(color,label):
	ax = plt.gca()
	ax.set_title(label)


def testBorn(mols, minmax):
	mol = 0
	data = []
	for f in mols:
		mol = mol + 1

		row3 = []
		row3.append("MW" + str(minmax[0]))
		inter = numpy.interp(getMW(f), (minmax[0][0],minmax[0][1]), (-0, +1))
		row3.append(inter)
		data.append(row3)

		row = []
		row.append("LOGP" + str(minmax[1]))
		inter = numpy.interp(getLogP(f), (minmax[1][0],minmax[1][1]), (-0, +1))
		row.append(inter)
		data.append(row)

		row8 = []
		row8.append("HBA" + str(minmax[2]))
		inter = numpy.interp(getHBA(f), (minmax[2][0],minmax[2][1]), (-0, +1))
		row8.append(inter)
		data.append(row8)

		row9 = []
		row9.append("HBD" + str(minmax[3]))
		inter = numpy.interp(getHBD(f), (minmax[3][0],minmax[3][1]), (-0, +1))
		row9.append(inter)
		data.append(row9)

		row4 = []
		row4.append("PSA" + str(minmax[4]))
		inter = numpy.interp(getPSA(f), (minmax[4][0],minmax[4][1]), (-0, +1))
		row4.append(inter)
		data.append(row4)

		row5 = []
		row5.append("FSP3" + str(minmax[5]))
		inter = numpy.interp(getFSP3(f), (minmax[5][0],minmax[5][1]), (-0, +1))
		row5.append(inter)
		data.append(row5)

		row6 = []
		row6.append("ROTB" + str(minmax[6]))
		inter = numpy.interp(getROTB(f), (minmax[6][0],minmax[6][1]), (-0, +1))
		row6.append(inter)
		data.append(row6)


		row7 = []
		row7.append("FC" + str(minmax[7]))
		inter = numpy.interp(getFC(f), (minmax[7][0],minmax[7][1]), (-0, +1))
		row7.append(inter)
		data.append(row7)

		row2 = []
		row2.append("qed" + str(minmax[8]))
		inter = numpy.interp(getQED(f), (minmax[8][0],minmax[8][1]), (-0, +1))
		row2.append(inter)
		data.append(row2)


	df = pd.DataFrame(data=data,columns=["attribute","value"])
	print(minmax)
	titles = ["LOGP","QED","MW","PSA","FSP3","ROTB","FC","HBA","HBD"]
	titles = ["MW","LOGP","HBA","HBD","PSA","FSP3","ROTB","FC","QED"]

	sns.set(rc={'figure.figsize':(10,10)})
	sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)},font_scale=1.5)
	pal = sns.cubehelix_palette(10, rot=-.25, light=.7)

	# set up the facet grid
	g = sns.FacetGrid(df, col="attribute", hue="attribute", aspect=1, height=2.25, palette=pal, col_wrap=3, sharex=False)

	# plot the kde plots
	g.map(sns.kdeplot,"value",clip_on=True,shade=True,alpha=1,lw=1.5,bw=0.2)
	g.map(sns.kdeplot, "value", clip_on=False, color="w", lw=2, bw=.2)
	g.map(plt.axhline, y=0, lw=2, clip_on=False)

	g.set(yticks=[])
	g.set(xticks=[0.0,1.0])
	g.despine(top=False, right=False)

	for i, ax in enumerate(g.axes.flat): # set every-other axis for testing purposes
		print(minmax[i][0],minmax[i][1])
		# ax.set
		# ax.set_xlabel(str(minmax[i]))
		ax.set_title(titles[i], fontweight='bold', fontsize=8, fontname='Arial')
		ax.tick_params(axis='both', which='major', labelsize=7)
		ax.set_xticklabels([minmax[i][0],minmax[i][1]])
		ax.set_xlim(-.5,1.5)

	g.fig.tight_layout()

	g.savefig("acid_amine_ionized.png")



def Sanitizer(smile_array):
	sanitized_mols = []
	failed_mols = []
	for f in smile_array:
		try:
			mol = Chem.MolFromSmiles(f[0].value)
			Chem.SanitizeMol(mol)
			sanitized_mols.append(mol)
		except:
			failed_mols.append(f[0].value)
			continue

	return sanitized_mols, failed_mols


def getAll(x):
	return [getLogP(x),getMW(x),getHBD(x),getHBA(x),getPSA(x),getROTB(x),getFSP3(x),getFC(x),getQED(x)]

def getLogP(x): return Chem.rdMolDescriptors.CalcCrippenDescriptors(x)[0]
def getMW(x): return Chem.Descriptors.MolWt(x)
def getHBD(x): return Chem.rdMolDescriptors.CalcNumHBD(x)
def getHBA(x): return Chem.rdMolDescriptors.CalcNumHBA(x)
def getPSA(x): return Chem.rdMolDescriptors.CalcTPSA(x)
def getROTB(x): return Chem.rdMolDescriptors.CalcNumRotatableBonds(x)
def getAROM(x): return Chem.rdMolDescriptors.CalcNumAromaticRings(x)
def getFSP3(x): return Chem.rdMolDescriptors.CalcFractionCSP3(x)
def getFC(x): return Chem.rdmolops.GetFormalCharge(x)
def getQED(x): return Chem.QED.qed(x)



def truncate(f, n):
	"""Truncates/pads a float f to n decimal places without rounding."""
	s = '{}'.format(f)
	if 'e' in s or 'E' in s:
		return '{0:.{1}f}'.format(f, n)
	i, p, d = s.partition('.')
	return '.'.join([i, (d+'0'*n)[:n]])

loader()
