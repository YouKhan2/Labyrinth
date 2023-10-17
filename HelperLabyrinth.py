import numpy as np
from random import randint, random, choice
from time import perf_counter, time, sleep
from matplotlib.pyplot import title, xlabel, ylabel, legend, plot, show, savefig
from IPython.display import clear_output
from tkinter import *

class Generation:
    
    def __init__(self, lines, cols):
        self.lines = lines#nombre de lignes du labyrinthe
        self.cols = cols#nombre de colonnes du labyrinthe
        self.grille = None #on memorise le labyrinthe dans cette liste (qui n'existe pas a l'initialisation)
        self.ch = ""
    
    def init(self):
        """initialise le labyrinthe"""
        self.grille = []
        for i in range(self.lines):
            self.grille.append([])
            for j in range(self.cols):
                self.grille[i].append([0, [False, False, False, False]]) #0 pour "non visité", le reste pour "pas de mur"
                #                          haut   droite  bas   gauche
    def full(self):
        """active tous les murs"""
        for i in range(self.lines):
            for j in range(self.cols):
                self.grille[i][j][1] = [True, True, True, True] #On met des murs partout partout partout
                
    def enleverMur(self, x, y, n): #x, y pour la position ; n pour la direction du mur a enlever par rapport a la case
        """enleve le mur a la position (x, y) en direction n :\n-si n vaut 0 : haut\n-si n vaut 1 : droite\n-si n vaut 2 : bas\n-si n vaut 3 : gauche"""
        if n == 0 and x > 0: #direction haut
            self.grille[x][y][1][0] = False #On enleve le mur haut de la case...
            self.grille[x - 1][y][1][2] = False #...et celui du mur bas de la case au dessus
        if n == 1 and y < self.cols - 1: #direction droite
            self.grille[x][y][1][1] = False
            self.grille[x][y + 1][1][3] = False
        if n == 2 and x < self.lines - 1: #direction bas
            self.grille[x][y][1][2] = False
            self.grille[x + 1][y][1][0] = False
        if n == 3 and y > 0: #direction gauche
            self.grille[x][y][1][3] = False
            self.grille[x][y - 1][1][1] = False
            
    def random(self, p = 0.5):
        """enleve des murs au hasard selon la probabilite 'p'"""
        for i in range(self.lines):
            for j in range(self.cols): #Pour chaque case,
                for k in range(4): #pour chaque mur, 
                    val = random()
                    if val < p: #on effectue un test
                        self.enleverMur(i, j, k) #s'il reussi, on anihile le mur
        
    def maj_ch(self):
        """mets a jour la chaine de caractere associee au labyrinthe"""
        self.ch = ""
        for i in range(self.lines):
            for j in range(self.cols):#affichage des horizontaux
                if self.grille[i][j][1][0]:#position (i, j), [1] = on regarde les murs ; [0] = on check le mur haut
                    self.ch += "+---"
                else:
                    self.ch += "+   "
            self.ch += "+\n"
            for j in range(self.cols):#affichage des verticaux
                if not self.grille[i][j][1][3] or (i == 0 and j == 0):#position (i, j), [1] = on regarde les murs ; [3] = on check le mur gauche
                    self.ch += "    "
                else:
                    self.ch += "|   "
            if i != self.lines - 1:
                self.ch += "|\n"
            else:
                self.ch += " \n"
        for i in range(self.cols):
            self.ch += "+---"
        self.ch += "+"
        
    def maj_ch_res(self, sol):
        """mets a jour la chaine de caractere associee au labyrinthe en marquant la solution"""
        self.ch = ""
        for i in range(self.lines):
            for j in range(self.cols):#affichage des horizontaux
                if self.grille[i][j][1][0]:#position (i, j), [1] = on regarde les murs ; [0] = on check le mur haut
                    self.ch += "+---"
                else:
                    self.ch += "+   "
            self.ch += "+\n"
            for j in range(self.cols):#affichage des verticaux
                if not self.grille[i][j][1][3] or (i == 0 and j == 0):#position (i, j), [1] = on regarde les murs ; [3] = on check le mur gauche
                    if (i, j) in sol:
                        self.ch += "  x "
                    else:
                        self.ch += "    "
                else:
                    if (i, j) in sol:
                        self.ch += "| x "
                    else:
                        self.ch += "|   "
            if i != self.lines - 1:
                self.ch += "|\n"
            else:
                self.ch += " \n"
        for i in range(self.cols):
            self.ch += "+---"
        self.ch += "+"
    
    def show(self, sol = False):
        """affiche le labyrinthe"""
        if sol:
            self.maj_ch_res(sol)
        else:
            self.maj_ch()
        print(self.ch)
        
    def check_all(self):
        """renvoie True si toutes les cases sont marquees et False sinon"""
        for ligne in self.grille:
            for case in ligne:
                if case[0] == 0: #si l'une des cases n'est pas visitée...
                    return False #on renvoie False
        return True #sinon on renvoie True
    
    def maze(self):
        """cree un labyrinthe via la methode appelee 'recursive backtracker'"""
        self.init()
        self.full()
        def cases_possibles(x, y): #fonction qui renvoie un tableau avec les cases voisines 
                                   #(par rapport à la position (x,y)) valides (non visitées)
            l = []
            if x != 0:#si on n'est pas tout à gauche
                if self.grille[x - 1][y][0] == 0:#si la case juste à gauche n'a pas été visitée
                    l.append((x - 1, y, 2))#on ajoute la position aux cases qu'on peut visiter
            if y != self.cols - 1:
                if self.grille[x][y + 1][0] == 0:#idem pour les autres directions
                    l.append((x, y + 1, 3))
            if x != self.lines - 1:
                if self.grille[x + 1][y][0] == 0:
                    l.append((x + 1, y, 0))
            if y != 0:
                if self.grille[x][y - 1][0] == 0:
                    l.append((x, y - 1, 1))
            return l
        
        pos_x = randint(0, self.lines - 1) #on tire un point de départ aleatoirement
        pos_y = randint(0, self.cols - 1)
        mem = [(pos_x, pos_y)] #cette liste retiendra en mémoire l'ordre des cases visitées
        self.grille[pos_x][pos_y][0] = 1 #à l'initialisation, on note que cette case est visitée en la marquant d'un '1'
        while not self.check_all(): #tant que des cases ne sont pas visitées...
            possibles = cases_possibles(pos_x, pos_y)
            if possibles != []: #si l'une des cases adjacentes n'a pas été visitée et est valide
                new = choice(possibles)#on tire l'une d'elles au hasard 
                self.enleverMur(new[0], new[1], new[2])#on vire le mur attenant dans la bonne direction
                pos_x, pos_y = new[:-1]#et on bouge
                mem.append((pos_x, pos_y))#on met à jour l'ordre des cases visitées
                self.grille[pos_x][pos_y][0] = 1 #et on marque la nouvelle case 
            else:
                new = mem.pop() #on revient en arrière
                pos_x, pos_y = new

    def affiche(self): #Pas utile sauf pour nous, pour voir les "situations" de chaque mur du Labb
        """affiche la situation des murs du labyrinthe"""
        for i in range(self.lines):
            for j in range(self.cols):
                print(self.grille[i][j][1], end = "")
            print()
            
    def numerote(self):
        """numerote les cases du labyrinthe de 0 a longueur * largeur - 1"""
        for i in range(self.lines):
            for j in range(self.cols):
                self.grille[i][j][0] = i * (self.cols) + j
            
    def id_(self, x, y):
        """renvoie le numero de la case (x, y)"""
        return self.grille[x][y][0]
    
    def chosir_mur_a_enlever(self):
        """renvoie une position et une direction valide"""
        n = randint(0, 3)
        if n == 0:
            x = randint(1, self.lines - 1)
            y = randint(0, self.cols - 1)
        elif n == 1:
            x = randint(0, self.lines - 1)
            y = randint(0, self.cols - 2)
        elif n == 2:
            x = randint(0, self.lines - 2)
            y = randint(0, self.cols - 1)
        else:
            x = randint(0, self.lines - 1)
            y = randint(1, self.cols - 1)
        return (x, y, n)
    
    def fusion1(self):
        """cree un labyrinthe en utilisant la methode de la fusion aleatoire de chemins"""
        self.init()
        self.full()
        self.numerote()#on initialise la grille du labyrinthe
        iter_ = 0
        while iter_ < self.lines * self.cols - 1: #il faut enlever ce nombre de mur pour que l'algorithme finisse
            pos_x, pos_y, n = self.chosir_mur_a_enlever()
            if n == 0: #si la direction est "haut"
                if self.id_(pos_x, pos_y) != self.id_(pos_x - 1, pos_y): #si les deux cases n'ont pas le même id_
                    temp = self.id_(pos_x, pos_y) # on retient l'id de la case la plus forte entre les deux
                    for i in range(self.lines):
                        for j in range(self.cols): #et pour chaque case de la grille, 
                            if self.id_(i, j) == temp: #si son id est le même que la case la plus forte 
                                self.grille[i][j][0] = self.id_(pos_x - 1, pos_y) #on change cet id en celui de la case faible
                                #en effet, si son id est le même que celui de la case forte, alors ces deux cases faisaient parti du
                                #même chemin ; cette affection permet de fusionner les chemins
                    self.enleverMur(pos_x, pos_y, n) #on enlève le mur en question
                    iter_ += 1 # et on incrémente notre variable
            elif n == 1: #direction droite
                if self.id_(pos_x, pos_y) != self.id_(pos_x, pos_y + 1):
                    temp = self.id_(pos_x, pos_y + 1)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
            elif n == 2: #direction bas
                if self.id_(pos_x, pos_y) != self.id_(pos_x + 1, pos_y):
                    temp = self.id_(pos_x + 1, pos_y)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
            else: #direction gauche
                if self.id_(pos_x, pos_y) != self.id_(pos_x, pos_y - 1):
                    temp = self.id_(pos_x, pos_y)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y - 1)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
                    
    def fusion2(self):
        def creer_liste():
            l = []
            for i in range(self.lines - 1):
                for j in range(self.cols - 1):
                    l.append((i, j, 1))
                    l.append((i, j, 2))
            l.append((self.lines - 1, self.cols - 1, 0))
            l.append((self.lines - 1, self.cols - 1, 3))
            return l
        def chose(liste):
            x, y, n = choice(liste)
            liste.remove((x, y, n))
            return (x, y, n)
        """cree un labyrinthe en utilisant la methode de la fusion aleatoire de chemins"""
        self.init()
        self.full()
        iter_ = 0
        l = creer_liste()
        self.numerote()#on initialise la grille du labyrinthe
        while iter_ < self.lines * self.cols - 1: #il faut enlever ce nombre de mur pour que l'algorithme finisse
            #print(iter_)
            pos_x, pos_y, n = chose(l)
            if n == 0: #si la direction est "haut"
                if self.id_(pos_x, pos_y) != self.id_(pos_x - 1, pos_y): #si les deux cases n'ont pas le même id_
                    temp = self.id_(pos_x, pos_y) # on retient l'id de la case la plus forte entre les deux
                    for i in range(self.lines):
                        for j in range(self.cols): #et pour chaque case de la grille, 
                            if self.id_(i, j) == temp: #si son id est le même que la case la plus forte 
                                self.grille[i][j][0] = self.id_(pos_x - 1, pos_y) #on change cet id en celui de la case faible
                                #en effet, si son id est le même que celui de la case forte, alors ces deux cases faisaient parti du
                                #même chemin ; cette affection permet de fusionner les chemins
                    self.enleverMur(pos_x, pos_y, n) #on enlève le mur en question
                    iter_ += 1 # et on incrémente notre variable
            elif n == 1: #direction droite
                if self.id_(pos_x, pos_y) != self.id_(pos_x, pos_y + 1):
                    temp = self.id_(pos_x, pos_y + 1)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
            elif n == 2: #direction bas
                if self.id_(pos_x, pos_y) != self.id_(pos_x + 1, pos_y):
                    temp = self.id_(pos_x + 1, pos_y)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
            else: #direction gauche
                if self.id_(pos_x, pos_y) != self.id_(pos_x, pos_y - 1):
                    temp = self.id_(pos_x, pos_y)
                    for i in range(self.lines):
                        for j in range(self.cols):
                            if self.id_(i, j) == temp:
                                self.grille[i][j][0] = self.id_(pos_x, pos_y - 1)
                    self.enleverMur(pos_x, pos_y, n)
                    iter_ += 1
                    
    def affiche_id(self):
        """affiche le numero des cases"""
        for ligne in self.grille:
            print()
            for case in ligne:
                print(case[0], end = " " * len(str(self.id_(self.lines - 1, self.cols - 1))))
    
    def export_to_txt(self, nom, sol = False):
        """cree un fichier texte representant le labyrinthe"""
        if sol:
            self.maj_ch_res(sol)
        else:
            self.maj_ch()
        fichier = open(nom + ".txt", "w")
        fichier.write(self.ch)
        fichier.close()          

class Resolution:
    
    def __init__(self, laby):
        self.laby = laby
    
    def bouge(self, x, y, direc):
        """modifie les parametre 'x' et 'y' en fonction du troisième 'direction' et renvoie le nouveau couple (x, y)"""
        if direc == 0: #si la direction est haut,
            return (x - 1, y) #on monte
        elif direc == 1:#droite
            return (x, y + 1)
        elif direc == 2:#bas
            return (x + 1, y)
        elif direc == 3:#gauche
            return (x, y - 1)
        else:
            print("cette direction n'existe pas : il faut 0, 1, 2, ou 3")
    
    def reorganiser(self, liste, ordre, stop):
        """décale une liste passée en paramètre de 'stop' crans vers la gauche si ordre vaut -1, et vers la droite
        si ordre vaut 1. Ne modifie pas la taille de la liste !"""
        if stop == 0: #la condition d'arrêt
            return liste
        if ordre == 1: #si on veut la décaler vers la droite,
            liste.append(0) #on ajoute d'abord un element à la liste,
            for i in range(len(liste) - 1, 0, -1): #et on décale tout vers la droite
                liste[i] = liste[i - 1] #(on n'écrase aucune valeur en faisant ça dans cet ordre)
            liste[0] = liste.pop() #on met dans la première case la valeur de la dernière et on supprime la dernière case
            return self.reorganiser(liste, ordre, stop - 1) #et en relance en décrémentant la variable 'stop'
        elif ordre == -1: #pour la gauche c'est différent :
            liste.append(liste[0]) #on ajoute à la fin de la liste le premier élément de celle-ci
            liste = liste[1:] #et on raccourci la liste de 1 par la gauche
            return self.reorganiser(liste, ordre, stop - 1) #on relance en décrémentant 'stop'
        else:
            print("cette facon de reorganiser la liste n'est pas valide : il faut 1 ou -1")
    
    def resoudre(self, direction):
        """résoud le labyrinthe 'laby' avec la technique de la main sur le mur gauche si 'direction' vaut -1
        et celle de la main sur le mur droit si 'direction' vaut 1"""
        sol = [] # stocke le chemin dans cette liste sous forme de coordonnées
        if direction == 1: #on initialise la liste en fonction de 'direction' : 
            #ici, on veut en priorité aller en bas car en posant la main toujours à droite, quand la personne
            #dans le labyrinthe ira en bas, vu du haut elle se déplacera vers la bas.
            #En procédant ainsi pour chaque direction on arrive à la conclusion suivante :
            #droite -> bas | tout droit -> droite | gauche -> haut | marche arrière -> gauche
            l = [2, 1, 0, 3]
        elif direction == -1:
            #la différence entre la technique sur la droite et sur la gauche est unique et se trouve ici :
            #on veut en priorité aller a gauche donc on garde la même attribution des deux différents points de vue
            #mais on change l'ordre (en effet, l'ordre a une importance dans le code qui suit)
            l = [0, 1, 2, 3]
        else:
            print("la direction n'est pas valide, il faut 1 ou -1")
        x, y = 0, 0 #on commence sur la case départ
        sol.append((x, y))
        arrivee = (self.laby.lines - 1, self.laby.cols - 1) #on définit notre objectif
        while (x, y) != arrivee: #tant qu'on ne l'a pas atteind,
            cpt = -1#on initialise un compteur a -1. Il comptera le nombre de non-mur autour de (x, y)
            for direc in l:# c'est ici que l'ordre intervient car on utilise l'instruction 'break' dès qu'une condition est réalisée
                cpt += 1
                if not self.laby.grille[x][y][1][direc]:
                    x, y = self.bouge(x, y, direc) #voilà pourquoi l'ordre est important : comme dit plus haut, 
                                                   #on veut aller en bas, puis si c'est impossible, à droite etc...
                    if cpt == 0: #en focntion du nombre de non-mur autour de l'ancienne case, on réorganise la liste
                        #En effet, après avoir tourné (ici à droite pour 'direction' = 1), les attributions des 
                        #différents points de vue changent et on obtient alors :
                        #droite -> gauche | tout droit -> bas | gauche -> droite | marche arrière -> haut
                        l = self.reorganiser(l, 1, 1)
                        break
                    if cpt == 2:
                        #ici on réorganise de l'autre manière
                        l = self.reorganiser(l, -1, 1)
                        break
                    if cpt == 3:
                        #et ici on fait marche arrière ce qui est équivalent a tourner sur soi-même deux fois de 90°
                        #on réorganise donc deux fois la liste (par la gauche ou la droite, c'est équivalent)
                        l = self.reorganiser(l, 1, 2)
                        break
                    break
            sol.append((x, y)) #on met à jour la solution
        return sol