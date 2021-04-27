"""
Ce modulerepresents the chessboard.

It is he who will manage the events of the players and take charge of the display of the game on the screen. To do this,
we need the pygame and chess packages. Pygame is the game engine that reacts to mouse clicks. chess him
is the engine of the chess game, the one that validates if the movement proposed by the player is valid.

This module is made up of several elements:
1. A class to describe a particular game piece
2. A class to describe the chess board itself.
3. An initial for each type of part, to represent a movement.
"" "


import chess
import pygame
import sys


# We code the dictionary which represents the chess pieces. The initials are used to describe the piece when it is
# movement. For example 'e5' represents the movement of a pawn towards the e5 square, while Nb3 represents the movement
# of a jumper to box b3.
initial_piece = {
    'King': 'K',
    'Lady': 'D',
    'Crazy': 'B',
    'Jumper': 'N',
    'Tour': 'R',
    'Pawn': ''
}



class Piece:
    """
Represents
a
simple
chess
piece.

A
part
has
a
name and a
color.It
also
has
a
box, and therefore
has
coordinates
on
the
screen.It
finally has
an
image, and a
reference
to
the
playing
surface
to
be
displayed.

"""
    def __init__(self, nom, couleur, x, y, taille, image, ecran):
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.ecran = ecran
        self.image = image

    def affiche(self):
        """
        Cette méthode force l'affichage de la pièce sur l'écran.

        A rectangle of the playing surface is redefined for its display. To display the rectangle, we will have
        need to know the coordinates of its top left corner. These will be the coordinates possessed by the
        piece itself. The size of the rectangle will come from the dimension of the image itself.



             (x, y)
                  +------largeur --------+
                  |                      |
                  |                      |
              longueur                   |  <----- Zone a afficher sur l'ecran.
                  |                      |
                  |                      |
                  +----------------------+
        """
        r = self.image.get_rect()       # On récupère la taille de l'image à afficher
        r.topleft = self.x, self.y      # On passe les coordonnées de la pièce comme coin en haut à gauche du rectangle
        self.ecran.blit(self.image, r)  # On affichage l'image dans le rectangle crée à l'intérieur de la zone écran

    def case(self):
        """
        Retourne la case correspondante de la piece affichee a l'ecran.
        """
        return chr(97 + (self.x // 85)) + str(((680 - self.y) // 85) + 1)


class Echiquier:
    """
    Représente un echiquier.
    """
    def __init__(self, ecran, echiquier, image):
        self.moteur = chess.Board()  # Moteur va valider si les mouvements sont valables.
        self.ecran = ecran
        self.echiquier = echiquier
        self.pieces = [Piece("Roi",      "Noir",  85 * 4, 0,      85, self._image(image, (68, 70, 85, 85)),   ecran),
                       Piece("Dame",     "Noir",  85 * 3, 0,      85, self._image(image, (234, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 0, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Tour",     "Noir",  85 * 7, 0,      85, self._image(image, (400, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 2, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Fou",      "Noir",  85 * 5, 0,      85, self._image(image, (566, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 1, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Cavalier", "Noir",  85 * 6, 0,      85, self._image(image, (736, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 0, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 1, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 2, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 3, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 4, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 5, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 6, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Pion",     "Noir",  85 * 7, 85,     85, self._image(image, (902, 70, 85, 85)),  ecran),
                       Piece("Roi",      "Blanc", 85 * 4, 85 * 7, 85, self._image(image, (68, 214, 85, 85)),  ecran),
                       Piece("Dame",     "Blanc", 85 * 3, 85 * 7, 85, self._image(image, (234, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 0, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Tour",     "Blanc", 85 * 7, 85 * 7, 85, self._image(image, (400, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 2, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Fou",      "Blanc", 85 * 5, 85 * 7, 85, self._image(image, (566, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 1, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Cavalier", "Blanc", 85 * 6, 85 * 7, 85, self._image(image, (736, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 0, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 1, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 2, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 3, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 4, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 5, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 6, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran),
                       Piece("Pion",     "Blanc", 85 * 7, 85 * 6, 85, self._image(image, (902, 214, 85, 85)), ecran)]

    def jouer(self):
        """
        C'est ici que se trouve la boucle de jeu, dans laquelle se rafraichit l'image de l'echiquier.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)

            self.ecran.fill((255, 255, 255))
            self.ecran.blit(self.echiquier, self.echiquier.get_rect())

            [p.affiche() for p in self.pieces]
            pygame.display.update()

    def _image(self, image, pos):
        """
        Genere la piece de l'image a partir de l'image generale du jeu d'echec.
        """
        r = pygame.Rect(pos)
        obj = pygame.Surface(r.size).convert()
        obj.blit(image, (0, 0), r)
        return obj


def nouvelle_partie():
    """
    C'est ici que l'on cree une nouvelle partie.

    La fonction retourne un echiquier et ses pieces disposees pour debuter une partie.
    """
    pygame.init()                                # Initialisation du moteur de jeu pygame
    ecran = pygame.display.set_mode((680, 680))  # On cree une fenetre de 680 pixel par 680 pixels
    pygame.display.set_caption("Echecs")         # Le titre de la fenetre s'appelle Echecs

    echiquier = pygame.Surface((680, 680))       # On definit une surface a l'ecran pour representer l'echiquier
    echiquier.fill((175, 141, 120))              # Que l'on peint en marron (uni) voici le RGB(175, 141, 120)

    # Les lignes suivantes permettent de peindre dans un marron legerement different les cases de l'echiquier
    # precedemment defini.
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    # Ici, on cree enfin le jeu d'echecs ainsi que les nouvelles pieces a afficher
    return Echiquier(ecran, echiquier, pygame.image.load("ressources/img.png").convert())


if __name__ == '__main__':
    partie = nouvelle_partie()
    partie.jouer()
