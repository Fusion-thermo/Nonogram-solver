from tkinter import *
import tkinter.filedialog
import numpy as np
from itertools import combinations
from time import time
from random import random
import os

#Pour fichier unique : https://webpbn.com/export.cgi

#Paramètres fenetre
fenetre_hauteur=900
fenetre_largeur=fenetre_hauteur
origine_x=fenetre_largeur//2
origine_y=fenetre_hauteur//2


def initialisation(rien):
	global hauteur_plateau, largeur_plateau, taux_remplissage, x0, y0, taille_case
	largeur_plateau=int(plateau_largeur_var.get())
	hauteur_plateau=int(plateau_hauteur_var.get())
	taux_remplissage=float(densite.get())
	if largeur_plateau>hauteur_plateau:
		taille_max=largeur_plateau
	else:
		taille_max=hauteur_plateau
	taille_case=0.7 * fenetre_hauteur//taille_max
	#coin supérieur gauche du plateau
	x0=origine_x-largeur_plateau*taille_case/2
	y0=origine_y-hauteur_plateau*taille_case/2
	if taux_remplissage<0.6 and largeur_plateau*hauteur_plateau>400:
		warning.set("Attention !")
	else:
		warning.set("")

#initialisation_plateau
def initialisation_plateau():
	global indices_lignes,indices_colonnes, filename_lines,filename_columns
	debut=time()
	temps_initialisation.set("")
	temps_resolution.set("")
	Canevas.delete(ALL)

	if fichier_var.get()=="1":
		plateau=np.zeros(shape=(hauteur_plateau,largeur_plateau))
		source=np.zeros(shape=(hauteur_plateau,largeur_plateau))
		for i in range(hauteur_plateau):
			for j in range(largeur_plateau):
				if random()<taux_remplissage:
					source[i,j]=1
				else:
					source[i,j]=2
	
		indices_lignes=[]
		for row in range(1,source.shape[0]+1):
			nb=0
			indice=[]
			for i in source[row-1:row, :][0]:
				if i==1:
					nb+=1
				elif i==2 and nb>0:
					indice.append(nb)
					nb=0
			if nb>0:
				indice.append(nb)
			if indice==[]:
				indice=[0]
			indices_lignes.append(indice)

		indices_colonnes=[]
		for column in range(1,source.shape[1]+1):
			nb=0
			indice=[]
			for i in source[:, column-1:column]:
				if i[0]==1:
					nb+=1
				elif i[0]==2 and nb>0:
					indice.append(nb)
					nb=0
			if nb>0:
				indice.append(nb)
			if indice==[]:
				indice=[0]
			indices_colonnes.append(indice)
	elif fichier_var.get()=="2":
		#path=os.path.realpath(__file__)
		#fin=path.rfind('\\')

		with open(filename_lines) as fichier:
			lignes=fichier.read()
		if "," in lignes:
			lignes=lignes.replace(",",";")
		indices_lignes=[]
		lignes=lignes.split("\n")
		for ligne in lignes:
			if ";" not in ligne:
				continue
			indice=[]
			for symbole in ligne.split(';'):
				if symbole!="":
					indice.append(int(symbole))
			if indice==[]:
				indice=[0]
			indices_lignes.append(indice[:])

		with open(filename_columns) as fichier:
			colonnes=fichier.read()
		if "," in colonnes:
			colonnes=colonnes.replace(",",";")
		indices_colonnes=[]
		colonnes=colonnes.split("\n")
		for colonne in colonnes:
			if ";" not in colonne:
				continue
			indice=[]
			for symbole in colonne.split(';'):
				if symbole!="":
					indice.append(int(symbole))
			if indice==[]:
				indice=[0]
			indices_colonnes.append(indice[:])
	else:
		with open(filename_unique) as fichier:
			lignes=fichier.read()
		indices_lignes=[]
		indices_colonnes=[]
		colonnes_temp=[]
		lignes=lignes.split("\n")
		nombre_indices_colonnes=lignes[0].count(",")
		nombre_indices_lignes=lignes[-1].count(",")
		for ligne in lignes:
			if "," not in ligne:
				continue
			indice=[]
			for symbole in ligne.split(','):
				if symbole!="":
					indice.append(int(symbole))
			if indice==[]:
				indice=[0]
			if ligne.count(",") == nombre_indices_colonnes:
				colonnes_temp.append(ligne.split(","))
			else:
				indices_lignes.append(indice[:])
		for i in range(nombre_indices_lignes+1,nombre_indices_colonnes+1):
			indice=[]
			for liste in colonnes_temp:
				if liste[i]!='':
					indice.append(int(liste[i]))
			indices_colonnes.append(indice[:])


	if fichier_var.get()=="2" or fichier_var.get()=="3":
		plateau_hauteur_var.set(len(indices_lignes))
		plateau_largeur_var.set(len(indices_colonnes))
		densite.set(sum(sum(i for i in ligne) for ligne in indices_lignes)/(len(indices_lignes)*len(indices_colonnes)))
		initialisation("rien")
		plateau=np.zeros(shape=(hauteur_plateau,largeur_plateau))
		source=np.zeros(shape=(hauteur_plateau,largeur_plateau))
	
	#affichage
	for i in range(len(indices_lignes)):
		for j in range(len(indices_lignes[i])):
			Canevas.create_text(x0 -14*(len(indices_lignes[i])-j), y0 + i*taille_case + taille_case/2,text=str(indices_lignes[i][j]))
	for i in range(len(indices_colonnes)):
		for j in range(len(indices_colonnes[i])):
			Canevas.create_text(x0 + taille_case/2 + i*taille_case, y0 -14*(len(indices_colonnes[i])-j),text=str(indices_colonnes[i][j]))
	
	pos_init_lignes=[positions_initiales_possibles(i,source.shape[1]) for i in indices_lignes]
	pos_init_colonnes=[positions_initiales_possibles(i,source.shape[0]) for i in indices_colonnes]

	print("Initialisation effectuée en {} secondes.".format(round(time()-debut,3)))
	temps_initialisation.set("Initialisé en\n"+str(round(time()-debut,3))+" s")

	return plateau,pos_init_lignes,pos_init_colonnes

def choix_fichier_lignes():
	global filename_lines
	filename_lines = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('csv files','.csv'),('all files','.*')])
	debut=-1
	while filename_lines[debut] != "/":
		debut-=1
	text_line.set(filename_lines[debut+1:])

def choix_fichier_colonnes():
	global filename_columns
	filename_columns = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('csv files','.csv'),('all files','.*')])
	debut=-1
	while filename_columns[debut] != "/":
		debut-=1
	text_column.set(filename_columns[debut+1:])

def choix_fichier_unique():
	global filename_unique
	filename_unique = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('csv files','.csv'),('all files','.*')])
	debut=-1
	while filename_unique[debut] != "/":
		debut-=1
	text_unique.set(filename_unique[debut+1:])

def decompose(number):
	# returns a generator of tuples (m, n1, r)
	for m in range(1, number+1):
		yield m, number // m, number % m

def decomposition(n):
	#les différentes façons de répartir les invariants dans les espaces dispos
	total=[]
	for m, n1, r in decompose(n):
		temp=[m]*n1
		if r!=0:
			temp.append(r)
		total.append(temp)
	return total

def combin(n, k):
    """Nombre de combinaisons de n objets pris k a k"""
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x

def arrang(n, k):
    """Nombre des arrangements de n objets pris k à k"""
    if k>n:
        return 0
    x = 1
    i = n-k+1
    while i <= n:
        x *= i
        i += 1
    return x

memoire={}
def positions_initiales_possibles(indice, longueur_ligne):
	#si aucun bloc
	if indice==[0]:
		return ['0'*longueur_ligne]

	#Ordre des blocs
	order=[]
	for i in indice:
		order.append([1]*i)

	#s'il n'y a qu'une seule position possible : techniquement pas nécessaire mais évite de lancer combination()
	nb_vides=longueur_ligne-(len(indice)-1)-sum(indice) #nombre de vides non libres (car au moins 1 entre chaque bloc)
	if nb_vides==0:
		chaine=""
		for i in indice:
			chaine+="1"*i
			chaine+="0"
		chaine=chaine[:-1]
		return [chaine]
	
	situations=[]
	nb_indices_possibles=longueur_ligne-sum(len(i) for i in order)
	#combinations() donne l'ordre de placement de chaque bloc de 1 dans
	#une chaîne de 0 libres, par insertion dans la chaîne.
	#positions des blocs
	#combinaison=combinations(range(nb_indices_possibles+1),len(order))
	#memoire[(nb_indices_possibles+1,len(order))] = [i for i in combinaison]
	if (nb_indices_possibles+1,len(order)) not in memoire.keys():
		combinaison=combinations(range(nb_indices_possibles+1),len(order))
		memoire[(nb_indices_possibles+1,len(order))] = [i for i in combinaison]
	combinaison=memoire[(nb_indices_possibles+1,len(order))][:]
	#print(memoire[(nb_indices_possibles+1,len(order))])
	#nb_indices_possibles représente le nombre maximal d'indices possibles pouvant accueillir les blocs de order.
	#Par exemple longueur ligne=5 et order=[[1,1,1]]. Alors évidemment ce bloc ne peut pas être placé en 3 ou 4
	# sinon il dépasserait. Donc nb_indices_possibles = 2
	#Les positions (par exemple (3,4,7,10)) indiquent l'ordre des blocs
	#dans la ligne. Ici le premier bloc ira en position 3, le deuxième ira
	# en position 4, mais comme ajouter le premier bloc dans la liste "décale" les indices, il faut tenir compte du décalage.
	#Ici, le deuxième bloc n'ira plus en position 4 mais 4 + nombre de "1" dans le premier bloc.
	#Chaque bloc ainsi ajouté s'intercale entre deux "0" dans la chaîne. Donc les blocs ajoutent des nombres à la chaîne,
	#jusqu'à atteindre naturellement longueur_ligne
	#cette boucle for est la partie lente de l'initialisation, tout le reste est négligeable
	for positions in combinaison:
		#print(positions)
		situation="0"*nb_indices_possibles
		i=0
		decalage=0
		for position in positions:
			situation=situation[:position+decalage] + ''.join(str(j) for j in order[i]) + situation[position+decalage:]
			decalage+=len(order[i])
			i+=1
			
		situations.append(situation)

	return situations


def solveur(plateau,pos_init_lignes,pos_init_colonnes):
	'''
	0 : inconnu
	1 : plein
	2 : vide

	'''
	#lignes
	for row in range(1,plateau.shape[0]+1):
		#état actuel de la ligne
		etat=""
		for i in plateau[row-1:row,:][0]:
			if i==1:
				etat+="1"
			elif i==2:
				etat+="2"
			else:
				etat+="0"
		#supprime les placements possibles qui ne sont pas en accord avec l'état actuel (càd s'ils prévoient un 0 là où il y a déjà un 1)
		restant=pos_init_lignes[row-1][:]
		for combi in pos_init_lignes[row-1]:
			for i in range(len(combi)):
				if (combi[i]=="0" and etat[i]=="1") or (combi[i]=="1" and etat[i]=="2"):
					restant.remove(combi)
					break
		pos_init_lignes[row-1]=restant[:]
		#parmi celles qui restent, si toutes prévoient un 1 à un même endroit alors on le met sur le plateau.
		#et si toutes prévoient 0 alors c'est un vide, marqué 2 sur le plateau.
		probas=[0]*largeur_plateau
		for combi in pos_init_lignes[row-1]:
			for i in range(len(combi)):
				probas[i]+=int(combi[i])
		for i in range(len(probas)):
			if probas[i]==len(pos_init_lignes[row-1]):
				plateau[row-1,i]=1
			elif probas[i]==0:
				plateau[row-1,i]=2


	#colonnes
	for column in range(1,plateau.shape[1]+1):
		#état actuel de la ligne
		etat=""
		for i in plateau[:, column-1:column]:
			if i[0]==1:
				etat+="1"
			elif i[0]==2:
				etat+="2"
			else:
				etat+="0"
		#supprime les placements possibles qui ne sont pas en accord avec l'état actuel (càd s'ils prévoient un 0 là où il y a un 1)
		restant=pos_init_colonnes[column-1][:]
		for combi in pos_init_colonnes[column-1]:
			for i in range(len(combi)):
				if (combi[i]=="0" and etat[i]=="1") or (combi[i]=="1" and etat[i]=="2"):
					restant.remove(combi)
					break
		pos_init_colonnes[column-1]=restant[:]
		#parmi celles qui restent, si toutes prévoient un 1 à un même endroit alors on le met sur le plateau.
		probas=[0]*hauteur_plateau
		for combi in pos_init_colonnes[column-1]:
			for i in range(len(combi)):
				if combi[i]=="1":
					probas[i]+=1
		for i in range(len(probas)):
			if probas[i]==len(pos_init_colonnes[column-1]):
				plateau[i,column-1]=1
			elif probas[i]==0:
				plateau[i,column-1]=2

	return plateau


def jeu(plateau,pos_init_lignes,pos_init_colonnes):
	debut=time()
	plateaux=[]
	diff=plateau
	while not diff.all():
		plateaux.append(np.copy(plateau))
		precedent=np.copy(plateau)
		plateau=solveur(plateau,pos_init_lignes,pos_init_colonnes)
		diff=plateau==precedent


	print("Résolution effectuée en {} secondes".format(round(time()- debut,3)))
	temps_resolution.set("Résolu en\n"+str(round(time()-debut,3))+" s")

	if np.count_nonzero(plateau == 0) >0:
		complet=False
	else:
		complet=True
	if not complet:
		print("Il y a plusieurs solutions équivalentes possibles\n\n")
	else:
		print("Solution trouvée !\n\n")

	return plateaux, plateaux[:]

def dessin(plateau):
	for row in range(0,plateau.shape[0]):
		for column in range(0,plateau.shape[1]):
			if plateau[row,column]==0:
				couleur="white"
			elif plateau[row,column]==2:
				couleur="red"
			else:
				couleur="black"
			Canevas.create_rectangle(x0+column*taille_case,y0+row*taille_case,x0+taille_case+column*taille_case,y0+taille_case+row*taille_case,fill=couleur)

def dessin_etapes():
	global plateaux
	recursif = fenetre.after(300,dessin_etapes)
	plateau=plateaux[0]
	for row in range(0,plateau.shape[0]):
		for column in range(0,plateau.shape[1]):
			if plateau[row,column]==0:
				couleur="white"
			elif plateau[row,column]==2:
				couleur="red"
			else:
				couleur="black"
			Canevas.create_rectangle(x0+column*taille_case,y0+row*taille_case,x0+taille_case+column*taille_case,y0+taille_case+row*taille_case,fill=couleur)
	if len(plateaux)>1:
		plateaux.remove(plateau)
	else:
		fenetre.after_cancel(recursif)

def dessin_etape_unique(numero):
	plateau=copie_plateau[int(numero)-1]
	Canevas.delete(ALL)
	for row in range(0,plateau.shape[0]):
		for column in range(0,plateau.shape[1]):
			if plateau[row,column]==0:
				couleur="white"
			elif plateau[row,column]==2:
				couleur="red"
			else:
				couleur="black"
			Canevas.create_rectangle(x0+column*taille_case,y0+row*taille_case,x0+taille_case+column*taille_case,y0+taille_case+row*taille_case,fill=couleur)
	for i in range(len(indices_lignes)):
		for j in range(len(indices_lignes[i])):
			Canevas.create_text(x0 -14*(len(indices_lignes[i])-j), y0 + i*taille_case + taille_case/2,text=str(indices_lignes[i][j]))
	for i in range(len(indices_colonnes)):
		for j in range(len(indices_colonnes[i])):
			Canevas.create_text(x0 + taille_case/2 + i*taille_case, y0 -14*(len(indices_colonnes[i])-j),text=str(indices_colonnes[i][j]))

def main():
	global plateaux,copie_plateau
	plateau,pos_init_lignes,pos_init_colonnes=initialisation_plateau()
	plateaux,copie_plateau=jeu(plateau,pos_init_lignes,pos_init_colonnes)
	scale_etape.config(to=len(plateaux))
	if int(etapes.get())==2:
		dessin(plateaux[-1])
	else:
		dessin_etapes()


fenetre=Tk()
Canevas=Canvas(fenetre,height=fenetre_hauteur,width=fenetre_largeur)
Canevas.pack(padx=5,pady=5,side=LEFT)

fichier_var=StringVar()
fichier_var.set(1)
Choix1=Radiobutton(fenetre, text="Aléatoire",variable=fichier_var, value=1)
Choix2=Radiobutton(fenetre, text="Fichiers lignes et colonnes",variable=fichier_var, value=2)
Choix3=Radiobutton(fenetre, text="Fichier unique",variable=fichier_var, value=3)
Choix1.pack()
Choix2.pack()
Choix3.pack()

line_bouton = Button(fenetre,  text = 'Lignes',  command = choix_fichier_lignes)
line_bouton.pack()
text_line=StringVar()
text_line.set("")
Label(fenetre,textvariable=text_line).pack()

column_bouton = Button(fenetre,  text = 'Colonnes',  command = choix_fichier_colonnes)
column_bouton.pack()
text_column=StringVar()
text_column.set("")
Label(fenetre,textvariable=text_column).pack()

unique_bouton = Button(fenetre,  text = 'Fichier unique',  command = choix_fichier_unique)
unique_bouton.pack()
text_unique=StringVar()
text_unique.set("")
Label(fenetre,textvariable=text_unique).pack()

Reset_bouton = Button(fenetre,  text = 'Démarrer',  command = main)
Reset_bouton.pack()

plateau_largeur_var=StringVar()
plateau_largeur_var.set(15)
plateau_largeur_scale=Scale(fenetre,  orient='horizontal',  from_=2,  to=30,  resolution=1, tickinterval=13,  label='Largeur du plateau',  variable=plateau_largeur_var, command=initialisation)
plateau_largeur_scale.pack(side="top")

plateau_hauteur_var=StringVar()
plateau_hauteur_var.set(15)
plateau_hauteur_scale=Scale(fenetre,  orient='horizontal',  from_=2,  to=30,  resolution=1, tickinterval=13,  label='Hauteur du plateau',  variable=plateau_hauteur_var, command=initialisation)
plateau_hauteur_scale.pack(side="top")

densite=StringVar()
densite.set(0.6)
densite_scale=Scale(fenetre,  orient='horizontal',  from_=0.1,  to=0.9,  resolution=0.1, tickinterval=0.4,  label='Densité',  variable=densite, command=initialisation)
densite_scale.pack(side="top")

warning=StringVar()
warning.set("")
Label(fenetre,textvariable=warning).pack()

etapes=StringVar()
etapes.set(1)
Choix1=Radiobutton(fenetre, text="Afficher les étapes",variable=etapes, value=1)
Choix2=Radiobutton(fenetre, text="Ne pas afficher les étapes",variable=etapes, value=2)
Choix1.pack()
Choix2.pack()

voir_etapes=StringVar()
voir_etapes.set(1)
scale_etape=Scale(fenetre,  orient='horizontal',  from_=1,  to=2,  resolution=1, tickinterval=2,  label='Voir une étape :',  variable=voir_etapes, command=dessin_etape_unique)
scale_etape.pack(side="top")

Bouton1 = Button(fenetre,  text = 'Quitter',  command = fenetre.destroy)
Bouton1.pack()

temps_initialisation=StringVar()
temps_initialisation.set("")
Label(fenetre,textvariable=temps_initialisation).pack()

temps_resolution=StringVar()
temps_resolution.set("")
Label(fenetre,textvariable=temps_resolution).pack()

initialisation(0)

fenetre.mainloop()