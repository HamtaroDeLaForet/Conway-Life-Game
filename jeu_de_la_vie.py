import pygame
import random
import time

# Définition des constantes
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Classe Cellule
class Cellule:
    def __init__(self):
        self.actuel = False
        self.futur = False
        self.voisins = None

    def est_vivant(self):
        return self.actuel

    def set_voisins(self, voisins):
        self.voisins = voisins

    def get_voisins(self):
        return self.voisins

    def naitre(self):
        self.futur = True

    def mourir(self):
        self.futur = False

    def basculer(self):
        self.actuel = self.futur

    def __str__(self):
        if self.actuel:
            return "X"
        else:
            return "-"

    def calcule_etat_futur(self):
        nbre_voisins_vivants = sum(1 for voisin in self.get_voisins() if voisin.est_vivant())
        if nbre_voisins_vivants != 2 and nbre_voisins_vivants != 3 and self.est_vivant():
            self.mourir()
        elif (nbre_voisins_vivants == 2 or nbre_voisins_vivants == 3) and not self.est_vivant():
            self.naitre()
        else:
            self.futur = self.actuel

# Classe Grille
class Grille:
    def __init__(self, largeur, hauteur, taux):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taux = taux
        self.matrix = self.set_matrice()

    def set_matrice(self):
        matrice = [[Cellule() for _ in range(self.largeur)] for _ in range(self.hauteur)]
        return matrice

    def dans_grille(self, i, j):
        return 0 <= j < self.largeur and 0 <= i < self.hauteur

    def set_cell(self, i, j, cellule):
        if self.dans_grille(i, j):
            self.matrix[i][j] = cellule
        else:
            raise IndexError(f"({i}, {j}) pas dans la grille")

    def get_cell(self, i, j):
        if self.dans_grille(i, j):
            return self.matrix[i][j]
        else:
            raise IndexError(f"({i}, {j}) pas dans la grille")

    def get_largeur(self):
        return self.largeur

    def get_hauteur(self):
        return self.hauteur

    def est_voisin(self, x, y, i, j):
        return abs(x - i) == 1 or abs(y - j) == 1

    def get_voisins(self, x, y):
        voisins = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if self.dans_grille(i, j) and (i != x or j != y):
                    voisins.append(self.get_cell(i, j))
        return voisins

    def set_voisins(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                cellule = self.get_cell(i, j)
                cellule.set_voisins(self.get_voisins(i, j))

    def remplir_alea(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if random.random() <= (self.taux / 100):
                    cellule = self.get_cell(i, j)
                    cellule.naitre()
                    cellule.basculer()

    def jeu(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                cellule = self.get_cell(i, j)
                cellule.calcule_etat_futur()

    def actualise(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                cellule = self.get_cell(i, j)
                cellule.basculer()

# Fonction principale
def main():
    # Demande à l'utilisateur les paramètres de la grille
    h = int(input("Quelle hauteur de tableau ? "))
    l = int(input("Quelle largeur de tableau ? "))
    t = int(input("Quel taux de cellule vivante souhaitez-vous avoir (en %) "))

    # Initialisation de Pygame
    pygame.init()

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((l * CELL_SIZE, h * CELL_SIZE))
    pygame.display.set_caption("Jeu de la Vie")

    # Création de la grille
    grille = Grille(l, h, t)
    grille.remplir_alea()
    grille.set_voisins()

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mise à jour de la grille
        grille.jeu()
        grille.actualise()

        # Affichage de la grille
        fenetre.fill(WHITE)
        for i in range(grille.get_hauteur()):
            for j in range(grille.get_largeur()):
                cellule = grille.get_cell(i, j)
                couleur = BLACK if cellule.est_vivant() else WHITE
                pygame.draw.rect(fenetre, couleur, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(fenetre, GREEN, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Contour

        pygame.display.flip()
        time.sleep(0.2)  # Délai entre les itérations

    # Fermeture de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
