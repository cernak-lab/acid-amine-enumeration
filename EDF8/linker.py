import pickle
from rdkit import Chem
import pandas as pd
from rdkit.Chem import AllChem, Draw
import json
from rdkit.Chem import rdMolDescriptors, Descriptors
import matplotlib
matplotlib.use('Agg')
matplotlib.matplotlib_fname()
import matplotlib.pyplot as plt
import numpy
from openpyxl import Workbook, load_workbook
from pprint import pprint
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

def loader():
	wb = load_workbook(filename = "acid_amine_final_320.xlsx")
	sheet = wb['Sheet1']

	allprods = []
	first = True
	mapper = {}
	rxn_names = []
	c = 1
	for f in sheet:
		mapper[c] = 0
		rxn_names.append(c)
		mol = Chem.MolFromSmiles(f[0].value)
		Chem.SanitizeMol(mol)
		Chem.Kekulize(mol, clearAromaticFlags=True)
		allprods.append(mol)
		c = c + 1
	print(len(allprods))

	pprint(mapper)
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
	drug_counter=0
	all_links = []
	for drug in mols:
		reaction_counter = 9300
		rxn_counter = 0
		for prod, rxn in zip(allprods,rxn_names):
			hits = drug.GetSubstructMatches(prod)
			if hits:
				inter = numpy.interp(len(hits), (1, 10), (-0, +1))
				color = tuple(255*x for x in cmap(inter)[0:3])

				link = "hs1 " + str(drug_counter) + " " + str(drug_counter+1) + " hs2 " + str(reaction_counter) + " " + str(reaction_counter+dist) + " color=(" + str(color[0])+","+ str(color[1])+","+str(color[2])+",.1)"
				all_links.append(link)
				mapper[rxn] = mapper[rxn] + len(hits)
			reaction_counter = reaction_counter + dist
			rxn_counter = rxn_counter + 1
		drug_counter = drug_counter + 1

	s = [(k, mapper[k]) for k in sorted(mapper, key=mapper.get, reverse=True)]
	pprint(s)

	xV = []
	yV = []
	for rxn in mapper:
		xV.append(rxn)
		yV.append(mapper[rxn])

	fig = plt.figure(figsize=(8,5))
	ax = fig.add_subplot(1,1,1)
	ax.bar(xV,yV, log=True, color='grey')
	c = 0
	real_xV = []
	tick = []
	for f in xV:
		if c % 10 == 0:
			tick.append(c)
			real_xV.append(c)
		c = c + 1
	ax.xaxis.set_major_locator(MultipleLocator(10))
	ax.xaxis.set_minor_locator(MultipleLocator(1))
	ax.set_xlim(1,320)
	plt.xlabel("Transformation",fontfamily="arial", fontsize="7")
	plt.ylabel("Frequency of Occurrence",fontfamily="arial", fontsize="7")
	plt.title("Frequency of occurrence of each transformation in complex molecules from DrugBank", fontfamily="arial", fontsize="8")

	plt.xticks(tick,real_xV, rotation='horizontal',fontsize="6", fontfamily='arial')
	fig.savefig("Mahjour_EDfig8.png")



loader()
