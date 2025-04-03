import pygame
import time
import json
import math

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Idle Space Mining")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Variables du jeu
class GameState:
    def __init__(self):
        self.resources = {
            "minerals": 0,
            "credits": 0
        }
        self.miners = {
            "basic": {"count": 1, "production": 1, "cost": 10},
            "advanced": {"count": 0, "production": 5, "cost": 50},
            "automatic": {"count": 0, "production": 20, "cost": 200}
        }
        self.last_save = time.time()

game = GameState()

# Fonction de sauvegarde
def save_game():
    with open("save_game.json", "w") as f:
        save_data = {
            "resources": game.resources,
            "miners": game.miners,
            "timestamp": time.time()
        }
        json.dump(save_data, f)

# Fonction de chargement
def load_game():
    try:
        with open("save_game.json", "r") as f:
            data = json.load(f)
            game.resources = data["resources"]
            game.miners = data["miners"]
            # Calcul des ressources gagnées hors-ligne
            offline_time = time.time() - data["timestamp"]
            offline_production = calculate_total_production() * offline_time
            game.resources["minerals"] += offline_production
    except FileNotFoundError:
        pass

def calculate_total_production():
    total = 0
    for miner_type, info in game.miners.items():
        total += info["count"] * info["production"]
    return total

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Gestion des clics pour acheter des mineurs
            # À implémenter selon les zones de clic

    # Mise à jour des ressources
    game.resources["minerals"] += calculate_total_production() / 60  # Production par frame

    # Affichage
    screen.fill(BLACK)
    
    # Affichage des ressources
    minerals_text = font.render(f"Minerals: {int(game.resources['minerals'])}", True, WHITE)
    screen.blit(minerals_text, (20, 20))
    
    # Affichage des mineurs et leurs coûts
    y_pos = 100
    for miner_type, info in game.miners.items():
        miner_text = font.render(f"{miner_type.capitalize()}: {info['count']} (Cost: {info['cost']})", True, WHITE)
        screen.blit(miner_text, (20, y_pos))
        y_pos += 40

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
