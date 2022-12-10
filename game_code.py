import pygame, sys, os, time


# initialize pygame
pygame.init()
pygame.font.init()

# Base settings
CLOCK = pygame.time.Clock()
WHITE = (255, 255, 255)
LIGHT_GREEN = (144, 238, 144)
GRAY = (128, 128, 128)
FPS = 60
WIDTH = 1140
HEIGHT = 900
TRANSPARENT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('arial', 24)
zeroPoint_X = WIDTH / 2
zeroPoint_Y = HEIGHT / 2
zeroPoint = zeroPoint_X, zeroPoint_Y

background = pygame.image.load(os.path.join('assets', 'game_background.png'))

# Sound
sound_crunch = pygame.mixer.Sound(os.path.join('sounds', 'crunch.mp3'))


# Classes
class Cookie:
    """
    Creates a cookie for the users to click on!
    """
    def __init__(self, image: str, win: pygame.Surface) -> None:
        """
        Constructor for cookie class that creates the cookie obj
        :param image: image of the cookie
        :param win: surface the cookie is going to be placed on
        """
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = self.width / 2
        self.y = self.height / 2

        self.win = win

    def draw(self) -> None:
        self.win.blit(self.image, (275, 150))

    def collidepoint(self, mouse_pos: tuple) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(mouse_pos)


class Player:
    def __init__(self):
        self.score = 0
        self.multiplier = 1
        self.cps = 0

    def setScore(self, score):
        self.score = score


class Score:
    """
    Creates the score and cps label that changes according to current value
    """
    def __init__(self, x: int, y: int, win: pygame.Surface, player: Player) -> None:
        """
        Constructor method that creates the Score
        :param x: x position
        :param y: y position
        :param win: Surface labes will be placed on
        :param player: Player class
        """
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.win = win
        self.player = player

    def draw(self) -> None:
        """
        Class method that draws and blits Score and CPS
        """
        font = pygame.font.SysFont('arial', 24)

        SCORE = font.render('{} cookies'.format(int(self.player.score)), True, WHITE)
        CPS = font.render('CPS: {}'.format(int(self.player.cps)), True, WHITE)

        # LABEL POS ON SCREEN
        self.win.blit(SCORE, (275, 50))
        self.win.blit(CPS, (275, 100))

class Item:
    """
    Class that holds the base operations for what an Item does
        Also holds correlated attributes that each Item shares
    """
    def __init__(self, base_cost: int, cps: int, image: str, win: pygame.Surface, pos1: int, pos2: int) -> None:
        """
        Constuctor method that initializes the Item
        :param base_cost: Initial cost for an Item
        :param cps: The amount of Cookies that will be added per second according to total amount of Items
        :param image: Image of the Item
        :param win: Surface that the Image will be placed on
        :param pos1: Places Item Image
        :param pos2: Places Item Cost
        """
        self.amount = 0
        self.bc = base_cost
        self.cps = cps
        self.image = pygame.transform.scale(image, (100, 100))
        self.display_price = FONT.render('{}'.format(int(self.bc)), True, WHITE)
        self.win = win
        self.placement_pos1 = pos1
        self.placement_pos2 = pos2
        self.image.set_colorkey(TRANSPARENT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.placement_pos1

    def draw(self):
        """
        Class method that draws Item image and Cost on Surface
        """
        self.win.blit(self.image, self.placement_pos1)
        self.win.blit(self.display_price, self.placement_pos2)

    def update(self):
        """
        Class method that updates base cost of items
            Changes the Label value associated with Item Cost
            Blits item on Surface
        """
        self.bc *= 2
        self.display_price = FONT.render('{}'.format(int(self.bc)), True, WHITE)
        self.win.blit(self.display_price, self.placement_pos2)


class Gma(Item):
    """
    Class that creates Gma Item!
    """
    def __init__(self, win: pygame.Surface) -> None:
        """
        Constructor Method that initializes GMA Item
        :param win: Surface Item is placed on
        """
        super().__init__(10, 1, pygame.image.load(os.path.join('assets', 'gma.png')), win, (0, 50), (115, 50))


class Gpa(Item):
    """
    Class that creates Gpa Item!
    """
    def __init__(self, win: pygame.Surface) -> None:
        """
        Constructor Method that initializes GPA Item
        :param win: Surface Item is placed on
        """
        super().__init__(100, 2, pygame.image.load(os.path.join('assets', 'grandfather.png')), win, (0, 200), (115, 200))


class Crumble(Item):
    """
    Class that creates Crumble Cookie Item!
    """
    def __init__(self, win: pygame.Surface) -> None:
        """
        Constructor Method that initializes Crumble Cookie Item
        :param win: Surface Item is placed on
        """
        super().__init__(1000, 10, pygame.image.load(os.path.join('assets', 'crumble_cookie.png')), win, (0, 350), (115, 350))



# Window Setup
win = pygame.display.set_mode((WIDTH, HEIGHT))

# Cookie Setup
cookie = Cookie(os.path.join('assets', 'cookie3.png'), win)

player = Player()
score_display = Score(100, 0, win, player)

gma = Gma(win)
gpa = Gpa(win)
crumble = Crumble(win)


# Functions
def draw() -> None:
    """
    Function that Draws everything on Game Surface
    """
    win.blit(background, (0, 0))
    cookie.draw()
    score_display.draw()
    gma.draw()
    gpa.draw()
    crumble.draw()
    pygame.display.update()


def run_game() -> None:
    """
    Function that runs the game loop
    :return:
    """
    # Game loop
    run = True
    while run:
        time.sleep(1)
        player.score += (gma.amount * gma.cps) + (gpa.amount * gpa.cps) + (crumble.amount * crumble.cps)
        # Transparency for Items
        if player.score >= gma.bc:
            gma.image.set_alpha(255)
        else:
            gma.image.set_alpha(128)

        if player.score >= gpa.bc:
            gpa.image.set_alpha(255)
        else:
            gpa.image.set_alpha(128)

        if player.score >= crumble.bc:
            crumble.image.set_alpha(255)
        else:
            crumble.image.set_alpha(128)

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if cookie.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(sound_crunch)
                    pygame.mixer.music.stop()
                    player.score += 1
                elif gma.rect.collidepoint(mouse_pos):
                    if player.score >= gma.bc:
                        player.cps += gma.cps
                        player.score -= gma.bc
                        gma.amount += 1
                        gma.update()
                elif gpa.rect.collidepoint(mouse_pos):
                    if player.score >= gpa.bc:
                        player.cps += gpa.cps
                        player.score -= gpa.bc
                        gpa.amount += 1
                        gpa.update()
                elif crumble.rect.collidepoint(mouse_pos):
                    if player.score >= crumble.bc:
                        player.cps += crumble.cps
                        player.score -= crumble.bc
                        crumble.amount += 1
                        crumble.update()

            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            CLOCK.tick(FPS)
        # Everything is iterated on the screen
        draw()

    pygame.quit()


def test():
    """
    Function that I used to test code on the back end without running game!

    """
    global gma, gpa, crumble


if __name__ == '__main__':
    run_game()