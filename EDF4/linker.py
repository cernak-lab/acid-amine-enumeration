from rdkit import Chem
import json
import matplotlib
matplotlib.use('Agg')
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt
import numpy
from openpyxl import Workbook, load_workbook

def loader():
	wb = load_workbook(filename = "acid_amine_final_320.xlsx")
	sheet = wb['Sheet1']

	allprods = []
	first = True
	for f in sheet:
		mol = Chem.MolFromSmiles(f[0].value)
		Chem.SanitizeMol(mol)
		Chem.Kekulize(mol, clearAromaticFlags=True)
		allprods.append(mol)
	print(len(allprods))


	with open('alldrugsprops.json') as f:
		drugProps = json.load(f) #load info into drugProps

	mols = []
	for f in drugProps:
		mol = Chem.MolFromSmiles(f["SMILES"])
		Chem.SanitizeMol(mol)
		Chem.Kekulize(mol, clearAromaticFlags=True)
		mols.append(mol)

	N = 320
	dist = int(200100/N)


	cmap = plt.get_cmap(name='plasma')
	drug_counter=7000
	all_links = []
	single = Chem.MolFromSmiles("C1CN2C(=NN=C2C(F)(F)F)CN1C(=O)CC(CC3=CC(=C(C=C3F)F)F)N")
	sit = Chem.MolFromSmiles("FC1=CC(C[C@H](N)CC(N2CCN3C(C2)=NN=C3C(F)(F)F)=O)=C(F)C(F)=C1")
	quin = Chem.MolFromSmiles("C=C[C@@H]1[C@@H]2CC([C@@H](C3=C(C=C(OC)C=C4)C4=NC=C3)O)[N@](C1)CC2")
	nos = Chem.MolFromSmiles("[H][C@]1([C@]2([H])C(C=CC(OC)=C3OC)=C3C(O2)=O)C4=C(OC)C5=C(OCO5)C=C4CCN1C")
	single=sit
	Chem.SanitizeMol(single)
	Chem.Kekulize(single, clearAromaticFlags=True)
	mols = [single]
	for drug in mols:
		reaction_counter = 9300
		rxn_counter = 0
		for prod in allprods:
			hits = drug.GetSubstructMatches(prod)
			if hits:
				inter = numpy.interp(len(hits), (1, 10), (-0, +1))
				color = tuple(255*x for x in cmap(inter)[0:3])
				print(rxn_counter)
				link = "hs1 " + str(drug_counter) + " " + str(drug_counter+1) + " hs2 " + str(reaction_counter) + " " + str(reaction_counter+dist) + " color=(" + str(color[0])+","+ str(color[1])+","+str(color[2])+",.75)"
				all_links.append(link)
			reaction_counter = reaction_counter + dist
			rxn_counter = rxn_counter + 1
		drug_counter = drug_counter + 1

	print(len(all_links))
	with open("sitagliptin_links.txt", "w") as output:
		for s in all_links:
			output.write("%s\n" % s)



loader()
