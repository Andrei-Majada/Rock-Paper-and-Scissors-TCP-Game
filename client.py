import pygame
from network import Network
pygame.font.init()

width = 500
height = 300
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pedra, Papel e Tesoura")

class Input:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 20)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def clickPosition(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

btns = [Input("Pedra", 50, 200, (50,50,50)), Input("Papel", 200, 200, (50,50,50)), Input("Tesoura", 350, 200, (50,50,50))]

def Screen(window, game, player):
    window.fill((20,20,20))

    if not(game.connected()):
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Você é o Player 1", 1, (5,57,253), True)
        window.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("arial", 20)
        text = font.render("PEDRA, PAPEL E TESOURA", 1, (255,198,23))
        window.blit(text, (width/2 - text.get_width()/2, 50 - text.get_height()/2))

        if player == 1:
            move = game.get_player_move(1)
        else:
            move = game.get_player_move(0)

        font = pygame.font.SysFont("arial", 20)
        text = font.render(move, 1, (64,31,255))
        window.blit(text, (width/2 - text.get_width()/2, 100 - text.get_height()))

        for btn in btns:
            btn.draw(window)

    pygame.display.update()

def main():
    keep = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("Jogador ", player)

    while keep:
        try:
            game = n.send("get")
        except:
            keep = False
            print("Nao foi possivel iniciar o jogo!")
            break
        
        if game.bothWent():
            Screen(win, game, player)
            pygame.time.delay(300)
            try:
                game = n.send("reset")
            except:
                keep = False
                print("Impossivel encontrar partida!")
                break

            font = pygame.font.SysFont("arial", 40)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Você venceu!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Empate!", 1, (255,0,0))
            else:
                text = font.render("Você perdeu!", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.clickPosition(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                print("escolha", btn.text)
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                print("escolha ", btn.text)
                                n.send(btn.text)

        Screen(win, game, player)   

def menuGame():
    play = True
    clock = pygame.time.Clock()

    while play:
        clock.tick(60)
        win.fill((20,20,20))
        font = pygame.font.SysFont("arial", 20)
        text = font.render("PEDRA, PAPEL E TESOURA", 1, (77,192,69))
        win.blit(text, (width/2 - text.get_width()/2, 50 - text.get_height()/4))
        font = pygame.font.SysFont("arial", 40)
        text = font.render("PLAY", 1, (77,192,69))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play = False

    main()

while True:
    menuGame()
