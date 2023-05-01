from tkinter import *
import numpy as np
from itertools import combinations
from time import time
from random import random
import os

#Paramètres
hauteur=800
largeur=hauteur
origine_x=largeur//2
origine_y=hauteur//2


def initialisation(rien):
	global taille_plateau, taux_remplissage, x0, y0, taille_case
	taille_plateau=int(plateau_taille_var.get())
	taux_remplissage=float(densite.get())
	taille_case=0.7 * hauteur//taille_plateau
	#coin supérieur gauche du plateau
	x0=origine_x-taille_plateau*taille_case/2
	y0=origine_y-taille_plateau*taille_case/2
	if taille_plateau/taux_remplissage>=30:
		warning.set("Attention !")
	else:
		warning.set("")

#initialisation_plateau
def initialisation_plateau():
	global indices_lignes,indices_colonnes
	debut=time()
	temps_initialisation.set("")
	temps_resolution.set("")
	Canevas.delete(ALL)

	#source=np.random.randint(1,3,size=(taille_plateau,taille_plateau))
	if fichier_var.get()=="1":
		plateau=np.zeros(shape=(taille_plateau,taille_plateau))
		source=np.zeros(shape=(taille_plateau,taille_plateau))
		for i in range(taille_plateau):
			for j in range(taille_plateau):
				if random()<taux_remplissage:
					source[i,j]=1
				else:
					source[i,j]=2
	
		indices_lignes=[]
		for row in range(1,source.shape[1]+1):
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
		for column in range(1,source.shape[0]+1):
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
	else:
		path=os.path.realpath(__file__)
		fin=path.rfind('\\')

		with open(path[:fin+1]+"Lines.csv") as fichier:
			lignes=fichier.read()
		if "," in lignes:
			lignes=lignes.replace(",",";")
		indices_lignes=[]
		lignes=lignes.split("\n")
		for ligne in lignes:
			if ";" not in ligne:
				continue
			indice=[]
			for symbole in ligne:
				if symbole!=";":
					indice.append(int(symbole))
			if indice==[]:
				indice=[0]
			indices_lignes.append(indice[:])

		plateau_taille_var.set(len(indices_lignes))
		densite.set(sum(sum(i for i in ligne) for ligne in indices_lignes)/len(indices_lignes)**2)
		initialisation(1)
		plateau=np.zeros(shape=(taille_plateau,taille_plateau))
		source=np.zeros(shape=(taille_plateau,taille_plateau))

		with open(path[:fin+1]+"Columns.csv") as fichier:
			colonnes=fichier.read()
		if "," in colonnes:
			colonnes=colonnes.replace(",",";")
		indices_colonnes=[]
		colonnes=colonnes.split("\n")
		for colonne in colonnes:
			if ";" not in colonne:
				continue
			indice=[]
			for symbole in colonne:
				if symbole!=";":
					indice.append(int(symbole))
			if indice==[]:
				indice=[0]
			indices_colonnes.append(indice[:])
	
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

def positions_initiales_possibles(indice, longueur_ligne):
	if indice==[0]:
		return ['0'*longueur_ligne]

	#Ce qu'on peut directement en déduire
	order=[]
	for i in indice:
		order.append([1]*i)
		order.append([0])
	order.pop()
	nb_vides=longueur_ligne-(len(indice)-1)-sum(indice)

	#s'il n'y a qu'une seule position possible
	if nb_vides==0:
		chaine=""
		for i in indice:
			chaine+="1"*i
			chaine+="0"
		chaine=chaine[:-1]
		return [chaine]


	#Toutes les combinaisons possibles pour les 0, les nombres obtenus représentent le nombre de 0 libres à un seul endroit
	#exemple : [3,1] signifie qu'on met trois 0 libres à un endroit et un 0 libre à un autre endroit.
	
	#choix de la méthode (arrangement ou combinaison) selon celle qui va le plus vite
	# n1=longueur_ligne
	# k1=longueur_ligne - len(order)
	# n2=longueur_ligne+len(order)-sum([len(i) for i in order])
	# k2=len(order)
	# a=arrang(n1,k1)
	# b=combin(n2,k2)
	# print("arrangement",a,"combinaison",b)
	# Conclusion : c'est combinaison qui est le plus rapide
	
	situations=[]
	#positions des blocs
	combinaison=combinations(range(longueur_ligne+len(order)-sum([len(i) for i in order])),len(order))
	for positions in combinaison:
		situation="0"*(longueur_ligne+len(order)-sum([len(i) for i in order]))
		i=0
		decalage=0
		for position in positions:
			situation=situation[:position+decalage] + ''.join(str(j) for j in order[i])+situation[position+decalage+1:]
			decalage+=len(order[i])-1
			i+=1
			
		situations.append(situation)
	chaines=[]
	situations.sort()
	for i in range(len(situations)-1):
		if situations[i]!=situations[i+1]:
			chaines.append(situations[i])
	chaines.append(situations[-1])

	return chaines


def solveur(plateau,pos_init_lignes,pos_init_colonnes):
	'''
	0 : inconnu
	1 : plein
	2 : vide

	'''
	#lignes
	for row in range(1,plateau.shape[1]+1):
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
		probas=[0]*taille_plateau
		for combi in pos_init_lignes[row-1]:
			for i in range(len(combi)):
				probas[i]+=int(combi[i])
		for i in range(len(probas)):
			if probas[i]==len(pos_init_lignes[row-1]):
				plateau[row-1,i]=1
			elif probas[i]==0:
				plateau[row-1,i]=2


	#colonnes
	for column in range(1,plateau.shape[0]+1):
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
		probas=[0]*taille_plateau
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
	for row in range(0,plateau.shape[1]):
		for column in range(0,plateau.shape[0]):
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
	for row in range(0,plateau.shape[1]):
		for column in range(0,plateau.shape[0]):
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
	for row in range(0,plateau.shape[1]):
		for column in range(0,plateau.shape[0]):
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
Canevas=Canvas(fenetre,height=hauteur,width=largeur)
Canevas.pack(padx=5,pady=5,side=LEFT)

fichier_var=StringVar()
fichier_var.set(1)
Choix1=Radiobutton(fenetre, text="Aléatoire",variable=fichier_var, value=1)
Choix2=Radiobutton(fenetre, text="Fichier",variable=fichier_var, value=2)
Choix1.pack()
Choix2.pack()

Reset_bouton = Button(fenetre,  text = 'Démarrer',  command = main)
Reset_bouton.pack()

plateau_taille_var=StringVar()
plateau_taille_var.set(15)
plateau_scale=Scale(fenetre,  orient='horizontal',  from_=2,  to=25,  resolution=1, tickinterval=13,  label='Taille du plateau',  variable=plateau_taille_var, command=initialisation)
plateau_scale.pack(side="top")

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