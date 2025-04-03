import pygame
import json
import math
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GOLD = (255, 215, 0)

class MagicalBakery:
    def __init__(self):
        self.cookies = 0
        self.cookies_per_click = 1
        self.cookies_per_second = 0
        self.prestige_points = 0
        self.level = 1
        self.xp = 0
        self.xp_needed = 100
        
        # Upgrades
        self.upgrades = {
            "magic_whisk": {"count": 0, "base_cost": 10, "cps": 0.1, "name": "Magic Whisk"},
            "enchanted_oven": {"count": 0, "base_cost": 50, "cps": 0.5, "name": "Enchanted Oven"},
            "fairy_assistant": {"count": 0, "base_cost": 200, "cps": 2, "name": "Fairy Assistant"},
            "time_bending_mixer": {"count": 0, "base_cost": 1000, "cps": 10, "name": "Time-Bending Mixer"},
            "cosmic_flour": {"count": 0, "base_cost": 5000, "cps": 50, "name": "Cosmic Flour"}
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Magical Bakery Idle")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.last_update = datetime.now()
        
    def format_number(self, num):
        if num >= 1e12:
            return f"{num/1e12:.1f}T"
        elif num >= 1e9:
            return f"{num/1e9:.1f}B"
        elif num >= 1e6:
            return f"{num/1e6:.1f}M"
        elif num >= 1e3:
            return f"{num/1e3:.1f}K"
        return f"{num:.1f}"
        
    def get_upgrade_cost(self, upgrade_key):
        base_cost = self.upgrades[upgrade_key]["base_cost"]
        count = self.upgrades[upgrade_key]["count"]
        return math.floor(base_cost * (1.15 ** count))
        
    def buy_upgrade(self, upgrade_key):
        cost = self.get_upgrade_cost(upgrade_key)
        if self.cookies >= cost:
            self.cookies -= cost
            self.upgrades[upgrade_key]["count"] += 1
            self.calculate_cps()
            return True
        return False
        
    def calculate_cps(self):
        self.cookies_per_second = 0
        for upgrade in self.upgrades.values():
            self.cookies_per_second += upgrade["count"] * upgrade["cps"]
        self.cookies_per_second *= (1 + self.prestige_points * 0.1)
        
    def prestige(self):
        if self.cookies >= 1e6:  # Need 1 million cookies to prestige
            gained_points = math.floor(math.log(self.cookies / 1e6, 10))
            if gained_points > 0:
                self.prestige_points += gained_points
                self.cookies = 0
                for upgrade in self.upgrades.values():
                    upgrade["count"] = 0
                self.calculate_cps()
                return gained_points
        return 0
        
    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed = math.floor(self.xp_needed * 1.5)
            self.cookies_per_click += 1
            
    def update(self):
        now = datetime.now()
        dt = (now - self.last_update).total_seconds()
        self.cookies += self.cookies_per_second * dt
        self.last_update = now
        
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw cookies and CPS
        cookie_text = self.font.render(f"Magical Cookies: {self.format_number(self.cookies)}", True, BLACK)
        cps_text = self.font.render(f"Per Second: {self.format_number(self.cookies_per_second)}", True, BLACK)
        self.screen.blit(cookie_text, (20, 20))
        self.screen.blit(cps_text, (20, 60))
        
        # Draw level and XP
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        xp_text = self.font.render(f"XP: {self.format_number(self.xp)}/{self.format_number(self.xp_needed)}", True, BLACK)
        self.screen.blit(level_text, (20, 100))
        self.screen.blit(xp_text, (20, 140))
        
        # Draw prestige info
        prestige_text = self.font.render(f"Prestige Points: {self.prestige_points}", True, GOLD)
        self.screen.blit(prestige_text, (20, 180))
        
        # Draw upgrades
        y = 250
        for key, upgrade in self.upgrades.items():
            cost = self.get_upgrade_cost(key)
            color = BLACK if self.cookies >= cost else GRAY
            
            upgrade_text = self.small_font.render(
                f"{upgrade['name']}: {upgrade['count']} (Cost: {self.format_number(cost)})", 
                True, color
            )
            self.screen.blit(upgrade_text, (20, y))
            y += 40
            
        # Draw prestige button
        if self.cookies >= 1e6:
            gained_points = math.floor(math.log(self.cookies / 1e6, 10))
            if gained_points > 0:
                prestige_button = self.font.render(
                    f"Prestige for +{gained_points} points", True, GOLD
                )
                self.screen.blit(prestige_button, (20, WINDOW_HEIGHT - 60))
                
        pygame.display.flip()
        
    def handle_click(self, pos):
        # Cookie click area (top of screen)
        if pos[1] < 200:
            self.cookies += self.cookies_per_click * (1 + self.prestige_points * 0.1)
            self.add_xp(1)
            
        # Upgrade buttons
        y = 250
        for key in self.upgrades.keys():
            if 20 <= pos[0] <= 400 and y <= pos[1] <= y + 30:
                self.buy_upgrade(key)
            y += 40
            
        # Prestige button
        if self.cookies >= 1e6 and WINDOW_HEIGHT - 60 <= pos[1] <= WINDOW_HEIGHT - 20:
            self.prestige()

def main():
    game = MagicalBakery()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.handle_click(event.pos)
                    
        game.update()
        game.draw()
        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main() 
