"""
Ce module représente l'échiquier.
C'est lui qui va gérer les événements des joueurs et prendre en charge l'affichage du jeu sur l'écran. Pour ce faire,
nous avons besoin des packages pygame et chess. Pygame est le moteur de jeu qui réagit aux clicks du souris. chess lui
est le moteur de jeu d'échecs, celui qui valide si le mouvement proposé par le joueur est valide.
Ce module est composé de plusieurs éléments:
1. Une classe pour décrire une pièce du jeu particulière
2. Une classe pour décrire l'échiquier lui-même.
3. Une initiale pour chaque type de pièce, afin de représenter un mouvement.
Les rois se déplacent d'une case dans n'importe quelle direction, tant que cette case n'est pas attaquée par une pièce ennemie. Aditionellement,
les rois sont capables de faire un geste spécial,
connu sous le nom de roque.
Les reines se déplacent en diagonale, horizontalement ou verticalement n'importe quel nombre de carrés. Ils sont incapables de sauter par-dessus des morceaux.
Les tours se déplacent horizontalement ou verticalement sur n'importe quel nombre de carrés. Ils sont incapables de sauter par-dessus des morceaux.
Les tours se déplacent lorsque le roi châteaux.
Les évêques se déplacent en diagonale sur n'importe quel nombre de cases. Ils sont incapables de sauter par-dessus des morceaux.
Les chevaliers se déplacent en forme de «L»: deux carrés dans une direction horizontale ou verticale,
puis déplacez un carré horizontalement ou verticalement. Ils sont la seule pièce capable de sauter par-dessus d'autres pièces.
Les pions avancent verticalement d'une case, avec la possibilité de se déplacer de deux cases s'ils ne se sont pas encore déplacés.
Les pions sont la seule pièce à capturer différente de la façon dont ils se déplacent. Les pions capturent une case en diagonale vers l'avant.
Les pions ne peuvent pas reculer lors des captures ou des mouvements. En atteignant l'autre côté du plateau, un pion promeut
dans n'importe quelle autre pièce, sauf pour un roi. De plus, les pions peuvent effectuer un mouvement spécial nommé En Passant.
"""
import chess
import pygame
import sys


# Nous codons le dictionnaire qui représente les pièces d'échecs. Les initiales sont utilisées pour décrire la pièce lorsqu'elle est
#en mouvement. Par exemple 'e5' représente le mouvement d'un pion vers la case e5, tandis que Nb3 représente le mouvement
# of a jumper to box b3.
piece_initiale = {
    'Roi': 'K',
    'Dame': 'D',
    'Fou': 'B',
    'Cavalier': 'N',
    'Tour': 'R',
    'Pion': ''
}


class Piece:
    """
    Représente une simple pièce d'échec.
    Une pièce a un nom et une couleur. Il a également une boîte, et a donc des coordonnées à l'écran. Il
    a enfin une image et une référence à la surface de jeu à afficher.
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
        Cette méthode force l'affichage de la pièce à l'écran
        Un rectangle de la surface de jeu est redéfini pour son affichage. Pour afficher le rectangle, nous aurons
        besoin de connaître les coordonnées de son coin supérieur gauche. Ce seront les coordonnées possédées par le
        morceau lui-même. La taille du rectangle proviendra de la dimension de l'image elle-même.
             (x, y)
                  +------largeur --------+
                  |                      |
                  |                      |
              longueur                   |  <----- Zone a afficher sur l'ecran.
                  |                      |
                  |                      |
                  +----------------------+
        """
        r = self.image.get_rect()       # Nous obtenons la taille de l'image à afficher
        r.topleft = self.x, self.y      # On passe les coordonnées de la pièce comme coin supérieur gauche du rectangle
        self.ecran.blit(self.image, r)  # Nous affichons l'image dans le rectangle créé à l'intérieur de la zone de l'écran

    def case(self):
        """
        Renvoie la case correspondante de la pièce affichée à l'écran.
        """
        return chr(97 + (self.x // 85)) + str(((680 - self.y) // 85))

    def get_colour(self):
        return self.couleur

class Echiquier:
    """
    Représente un échiquier.
    """
    def __init__(self, ecran, echiquier, image):
        self.make_move = False
        self.move_coord = ""
        self.last_move = ""
        self.moteur = chess.Board()  # Le moteur validera si les mouvements sont valides.
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

    def jouer(self,colour):
        """
        C'est là que se trouve la boucle de jeu, dans laquelle l'image de l'échiquier est rafraîchie.
        """
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Mouse click or press
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)
                        print("self.moteur = ", self.moteur)
                        print("From position: ", chr(97 + (x // 85)) + str(((680 - y) // 85) + 1))
                        curr_pos = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)


                elif event.type == pygame.MOUSEBUTTONUP:
                    # Mouse release
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)
                        # Calcul de la position finale en divisant par 85 (longueur du côté du carré)
                        # l'entier le plus proche juste en dessous de la valeur doit être comme type: int ()
                        x_new = int(x / 85) * 85
                        y_new = int(y / 85) * 85
                        # print("To position: ", chr(97 + (x // 85)) + str(((680 - y) // 85) + 1))
                        final_pos = chr(97 + (x // 85)) + str(((680 - y) // 85) + 1)
                        check_move = curr_pos + final_pos
                        # print("check move", check_move)
                        new_pos = 0
                        for p in self.pieces:
                            # Obtenir la pièce dans la position donnée calculée comme curr_pos
                            print("p.get_colour()",p.get_colour())
                            print("get_colour()",colour)

                            if p.case() == curr_pos and p.get_colour()==colour:
                                valid_moves = self.moteur.generate_legal_moves()
                                move_made = chess.Move.from_uci(check_move)
                                self.make_move = False
                                for k in valid_moves:
                                    print("k =", k)
                                    if k == move_made:
                                        self.make_move = True
                                if self.make_move:
                                    p.x = x_new
                                    p.y = y_new
                                    self.moteur.push(move_made)
                                    self.pieces[new_pos] = p
                                    self.last_move = check_move
                                    # Si la valeur x n'est pas de 3 chiffres, faites-en 3 en mettant un 0 avant la valeur
                                    # First the x and y values are converted to strings
                                    x_new_str = str(x_new)
                                    y_new_str = str(y_new)
                                    # Mettre 0 jusqu'à ce que la longueur soit de 3
                                    while len(x_new_str)<3:
                                        x_new_str = "0" + x_new_str
                                    while len(y_new_str) < 3:
                                         y_new_str = "0" + x_new_str
                                    # C'est la chaîne qui est passée au serveur
                                    self.move_coord = str(x_new_str) + str(y_new_str)

                                    play = False
                            new_pos += 1
            self.update_screen()

    def make_auto_move(self, data):
        print("data =",data)
        curr_pos = data[0:2]
        print("curr_pos new",curr_pos)
        check_move = data[0:4]
        x_new = int(data[4:7])
        y_new = int(data[7:10])
        new_pos = 0
        for p in self.pieces:
            # Obtenir la pièce dans la position donnée calculée comme curr_pos
            if p.case() == curr_pos:
                move_made = chess.Move.from_uci(check_move)
                p.x = x_new
                p.y = y_new
                self.moteur.push(move_made)
                self.pieces[new_pos] = p
                self.last_move = check_move
            new_pos += 1
        self.update_screen()

    def update_screen(self):
            self.ecran.fill((255, 255, 255))
            self.ecran.blit(self.echiquier, self.echiquier.get_rect())

            [p.affiche() for p in self.pieces]
            pygame.display.update()

    def _image(self, image, pos):
        """
        Génère la pièce d'image à partir de l'image générale du jeu d'échecs
        """
        r = pygame.Rect(pos)
        obj = pygame.Surface(r.size).convert()
        obj.blit(image, (0, 0), r)
        return obj


def nouvelle_partie(sid):
    """
    C'est là que nous créons un nouveau jeu.
    La fonction renvoie un échiquier et ses pièces disposées pour démarrer une partie.
    """
    pygame.init()                                # Initialisation du moteur de jeu pygame
    ecran = pygame.display.set_mode((680, 680))  # On cree une fenetre de 680 pixel par 680 pixels
    pygame.display.set_caption("Echecs : " + sid)         # Le titre de la fenetre s'appelle Echecs

    echiquier = pygame.Surface((680, 680))       # On definit une surface a l'ecran pour representer l'echiquier
    echiquier.fill((175, 141, 120))              # Que l'on peint en marron (uni) voici le RGB(175, 141, 120)

    # Les lignes suivantes vous permettent de peindre les cases de l'échiquier dans un marron légèrement différent
    # précédemment défini
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    for x in range(1, 9, 2):
        for y in range(1, 9, 2):
            pygame.draw.rect(echiquier, (250, 240, 230), (x * 85, y * 85, 85, 85))

    #Ici, nous créons enfin le jeu d'échecs ainsi que les nouvelles pièces à afficher
    return Echiquier(ecran, echiquier, pygame.image.load("ressources/img.png").convert())


if __name__ == '__main__':
    partie = nouvelle_partie('sid')
    partie.jouer('sid')
