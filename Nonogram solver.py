from tkinter import *
import numpy as np
from itertools import combinations
from time import time
from random import random

#Paramètres
taille_plateau=15
hauteur=800
taux_remplissage=0.6
largeur=hauteur
taille_case=0.7 * hauteur//taille_plateau
origine_x=largeur//2
origine_y=hauteur//2
#coin supérieur gauche du plateau
x0=origine_x-taille_plateau*taille_case/2
y0=origine_y-taille_plateau*taille_case/2



#Initialisation
def initialisation():
	debut=time()

	#source=np.random.randint(1,3,size=(taille_plateau,taille_plateau))
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

	pos_init_lignes=[positions_initiales_possibles(i,source.shape[1]) for i in indices_lignes]
	pos_init_colonnes=[positions_initiales_possibles(i,source.shape[0]) for i in indices_colonnes]

	print("Initialisation effectuée en {} secondes.".format(round(time()-debut,3)))

	jeu(source,plateau,indices_lignes,indices_colonnes,pos_init_lignes,pos_init_colonnes)

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


def solveur(plateau,indices_lignes,indices_colonnes,pos_init_lignes,pos_init_colonnes):
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



def jeu(source,plateau,indices_lignes,indices_colonnes,pos_init_lignes,pos_init_colonnes):
	debut=time()
	comparaison=source==plateau
	while not comparaison.all():
		precedent=np.copy(plateau)
		plateau=solveur(plateau,indices_lignes,indices_colonnes,pos_init_lignes,pos_init_colonnes)
		diff=plateau==precedent
		#si plus de modification
		if diff.all():
			break

		comparaison = source==plateau
	print("Résolution effectuée en {} secondes".format(round(time()- debut,3)))

	if not comparaison.all():
		print("Il y a plusieurs solutions équivalentes possibles")
	else:
		print("Solution trouvée !")

	#affichage
	for row in range(1,plateau.shape[1]+1):
		for column in range(0,plateau.shape[0]):
			if plateau[row-1,column]==0:
				couleur="white"
			elif plateau[row-1,column]==2:
				couleur="red"
			else:
				couleur="black"
			Canevas.create_rectangle(x0+column*taille_case,y0+(row-1)*taille_case,x0+taille_case+column*taille_case,y0+taille_case+(row-1)*taille_case,fill=couleur)
	for i in range(len(indices_lignes)):
		for j in range(len(indices_lignes[i])):
			Canevas.create_text(x0 -14*(len(indices_lignes[i])-j), y0 + i*taille_case + taille_case/2,text=str(indices_lignes[i][j]))
	for i in range(len(indices_colonnes)):
		for j in range(len(indices_colonnes[i])):
			Canevas.create_text(x0 + taille_case/2 + i*taille_case, y0 -14*(len(indices_colonnes[i])-j),text=str(indices_colonnes[i][j]))


fenetre=Tk()
Canevas=Canvas(fenetre,height=hauteur,width=largeur)
Canevas.pack(padx=5,pady=5,side=LEFT)

Bouton1 = Button(fenetre,  text = 'Quitter',  command = fenetre.destroy)
Bouton1.pack()

initialisation()

fenetre.mainloop()