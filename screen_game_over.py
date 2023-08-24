#modules nécessaires
import pgzrun
import pygame

#dimensions de la fenêtre et autre variable
WIDTH = 800
HEIGHT = 600
game_over = False
#variable globale pour suivre l'état du "restart"
restart_button = None



#def de la function `game_over_screen` qui affiche l'écran de fin de partie
def game_over_screen():
    screen.clear()
    screen.draw.text("Game Over !!", center=(WIDTH/2, HEIGHT/2), fontsize=70, color="red")
#autres éléments ajoutés à l'écran de fin de partie
    global restart_button
    restart_button = Actor("restart_button", conter=(WIDTH/2, HEIGHT/2 + 100))
    restart_button.draw()

def on_restart_click():
    global game_over, restart_button
    game_over = False
    restart_button = None
    ################### réinitialiser les éléments jeu



#def function `update` qui vérifie si les conditions (if) de fin de partie sont remplies
def update():
    global game_over
    #pour vérifier les conditions de fin de partie => game_over mettre = True
    if game_over:
        game_over_screen()



#def function `draw` qui dessine les éléments à écran
def draw():
    if not game_over:
        #éléments jeu normal
        pass    

pgzrun.go()