from p4_funct import *


def new_grille():
    grille = [[a for a in ["0"]*7] for b in ["0"]*6]
    return grille

a = new_grille()
pleine = [False]*7

def afficher():
    for grille in reversed(a):
        print(grille)

################################################################################

#copier ici la partie buggée

################################################################################
