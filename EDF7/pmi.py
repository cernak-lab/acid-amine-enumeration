from rdkit import Chem
from rdkit.Chem import AllChem, Draw
from rdkit.Chem import rdMolDescriptors, Descriptors
from openpyxl import Workbook, load_workbook
import matplotlib
matplotlib.use('Agg')
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def loader():
	wb = load_workbook(filename = "acid_amine_with_bprime_1005_updated_unionized_schem.xlsx")
	sheet = wb['Sheet1']

	sanitized, failed = Sanitizer(sheet)
	pmi(sanitized)

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

def getQED(x): return Chem.QED.qed(x)


def pmi(mols):
	x = []
	y = []
	x_spec = []
	y_spec = []
	prods = []
	qed = []
	counter = 0
	for j in mols:
		AllChem.EmbedMolecule(j)
		try:
			AllChem.UFFOptimizeMolecule(j)
		except:
			continue
		x1 = Chem.Descriptors3D.NPR1(j)
		y1 = Chem.Descriptors3D.NPR2(j)
		# if counter in [212, 159, 429, 432, 836, 707]:
			# print(counter, Chem.MolToSmiles(j), x1, y1)
			# x_spec.append(x1)
			# y_spec.append(y1)
		qed.append(getQED(j))
		counter = counter + 1
		x.append(x1)
		y.append(y1)

	fig = plt.figure(figsize=(6.88976,6.88976))
	ax = fig.add_subplot(1,1,1)

	ax.set_xlim([0,1])
	ax.set_ylim([0.5,1])
	ax.plot([0,.5], [1,0.5],color='gray')
	ax.plot([.5,1], [0.5,1],color='gray')
	ax.plot([0,1], [1,1],color='gray')

	im = ax.scatter(
	x=x,
	y=y,
	c=qed,
	cmap="plasma",
	s=70,
	alpha=0.5)

	# im2 = ax.scatter(
	# x=x_spec,
	# y=y_spec,
	# c='r',
	# s=70,
	# alpha=1)

	ax.tick_params(axis='both', which='major', labelsize=7)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=.1)
	pt = plt.colorbar(im, cax=cax, orientation="vertical")
	pt.ax.tick_params(labelsize=7)

	ax.set_title("Principal Moment of Inertia for 1005 Amine-Acid Coupling Products Incorporating Stereochemistry and Regiochemistry",fontname="Arial", fontsize=7)
	fig.savefig("Mahjour_EDfig6.png")

	return ax

loader()
