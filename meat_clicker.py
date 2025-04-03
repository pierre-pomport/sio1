import pygame
import math
import random
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
DARK_BG = (25, 25, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 160)
DARK_GRAY = (50, 50, 60)
RED = (220, 80, 80)
BRIGHT_RED = (255, 100, 100)
DARK_RED = (150, 30, 30)
BLUE = (80, 120, 220)
GREEN = (80, 220, 120)
GOLD = (255, 200, 60)

# Font setup
pygame.font.init()

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE, font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size)
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, (color[0]//2, color[1]//2, color[2]//2), self.rect, 2, border_radius=5)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

class MeatClicker:
    def __init__(self):
        self.meat = 0
        self.meat_per_click = 1
        self.meat_per_second = 0
        self.prestige_points = 0
        self.total_clicks = 0
        self.multiplier = 1.0
        
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Meat Clicker")
        
        # Load fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.header_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        # Current tab
        self.current_tab = "upgrades"
        self.tabs = [
            {"id": "upgrades", "name": "Améliorations", "color": RED},
            {"id": "prestige", "name": "Prestige", "color": GOLD},
            {"id": "stats", "name": "Statistiques", "color": BLUE}
        ]
        
        # Create meat sprite
        self.meat_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 120, 200, 200)
        self.meat_click_effect = 0
        
        # Create meat images
        self.meat_imgs = [
            self.create_meat_image(200, 200, RED),
            self.create_meat_image(210, 210, BRIGHT_RED)
        ]
        
        # Upgrades
        self.upgrades = {
            "knife": {
                "name": "Etale de viande", 
                "desc": "la ou bea a commencé",
                "base_cost": 10, 
                "cost": 10,
                "count": 0, 
                "production": 0.1,
                "color": (200, 200, 200),
                "icon": "🔪"
            },
            "butcher": {
                "name": "Boucherie", 
                "desc": "https://www.facebook.com/pages/Chez-Bea/1894622534088109",
                "base_cost": 50, 
                "cost": 50,
                "count": 0, 
                "production": 0.5,
                "color": RED,
                "icon": "👨‍🍳"
            },
            "grinder": {
                "name": "Client", 
                "desc": "AD Laurent, nage libre, vivet. Il y sont tous passé",
                "base_cost": 200, 
                "cost": 200,
                "count": 0, 
                "production": 2,
                "color": (180, 180, 180),
                "icon": "⚙️"
            },
            "farm": {
                "name": "Ferme d'Élevage", 
                "desc": "Produit de la viande fraîche",
                "base_cost": 1000, 
                "cost": 1000,
                "count": 0, 
                "production": 10,
                "color": GREEN,
                "icon": "🐄"
            },
            "slaughterhouse": {
                "name": "Abattoir", 
                "desc": "Traitement industriel de la viande",
                "base_cost": 5000, 
                "cost": 5000,
                "count": 0, 
                "production": 40,
                "color": DARK_RED,
                "icon": "🏭"
            },
            "lab": {
                "name": "Laboratoire", 
                "desc": "Création de viande synthétique",
                "base_cost": 25000, 
                "cost": 25000,
                "count": 0, 
                "production": 200,
                "color": BLUE,
                "icon": "🧪"
            },
            "factory": {
                "name": "Usine de Transformation", 
                "desc": "Production massive de produits carnés",
                "base_cost": 100000, 
                "cost": 100000,
                "count": 0, 
                "production": 1000,
                "color": (100, 100, 150),
                "icon": "🏭"
            },
            "temple": {
                "name": "Temple de la Viande", 
                "desc": "Culte de la viande éternelle",
                "base_cost": 500000, 
                "cost": 500000,
                "count": 0, 
                "production": 5000,
                "color": GOLD,
                "icon": "🏛️"
            }
        }
        
        # Bonus upgrades that appear after certain milestones
        self.bonus_upgrades = {
            "sharp_blade": {
                "name": "Lame Affûtée",
                "desc": "Améliore l'efficacité du couteau par 2",
                "cost": 100,
                "requires": {"knife": 5},
                "affects": "knife",
                "multiplier": 2,
                "purchased": False,
                "color": (220, 220, 230)
            },
            "master_butcher": {
                "name": "Maître Boucher",
                "desc": "Améliore l'efficacité du boucher par 2",
                "cost": 500,
                "requires": {"butcher": 10},
                "affects": "butcher",
                "multiplier": 2,
                "purchased": False,
                "color": RED
            },
            "electric_grinder": {
                "name": "Hachoir Électrique",
                "desc": "Améliore l'efficacité du hachoir par 2",
                "cost": 2000,
                "requires": {"grinder": 10},
                "affects": "grinder",
                "multiplier": 2,
                "purchased": False,
                "color": (180, 180, 180)
            },
            "industrial_farm": {
                "name": "Ferme Industrielle",
                "desc": "Améliore l'efficacité de la ferme par 2",
                "cost": 10000,
                "requires": {"farm": 10},
                "affects": "farm",
                "multiplier": 2,
                "purchased": False,
                "color": GREEN
            },
            "automated_slaughter": {
                "name": "Abattage Automatisé",
                "desc": "Améliore l'efficacité de l'abattoir par 2",
                "cost": 50000,
                "requires": {"slaughterhouse": 10},
                "affects": "slaughterhouse",
                "multiplier": 2,
                "purchased": False,
                "color": DARK_RED
            },
            "genetic_enhancement": {
                "name": "Amélioration Génétique",
                "desc": "Améliore l'efficacité du laboratoire par 2",
                "cost": 250000,
                "requires": {"lab": 10},
                "affects": "lab",
                "multiplier": 2,
                "purchased": False,
                "color": BLUE
            },
            "quantum_meat": {
                "name": "Viande Quantique",
                "desc": "Double toute la production",
                "cost": 1000000,
                "requires": {"meat": 1000000},
                "affects": "all",
                "multiplier": 2,
                "purchased": False,
                "color": (100, 0, 200)
            }
        }
        
        # Create buttons
        self.tab_buttons = []
        self.upgrade_buttons = []
        self.bonus_upgrade_buttons = []
        self.update_buttons()
        
        self.last_update = datetime.now()
        
    def create_meat_image(self, width, height, color):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw meat shape
        pygame.draw.ellipse(surface, color, (0, 0, width, height))
        pygame.draw.ellipse(surface, (255, 255, 255, 100), (width//4, height//4, width//2, height//2))
        return surface
        
    def update_buttons(self):
        # Tab buttons
        button_width = WINDOW_WIDTH // len(self.tabs)
        self.tab_buttons = []
        for i, tab in enumerate(self.tabs):
            btn = Button(i * button_width, 350, button_width, 40, 
                       tab["name"], DARK_GRAY, tab["color"])
            self.tab_buttons.append({"id": tab["id"], "button": btn})
        
        # Upgrade buttons
        self.upgrade_buttons = []
        card_width = 230
        card_height = 160
        cards_per_row = 4
        margin = (WINDOW_WIDTH - (cards_per_row * card_width)) // (cards_per_row + 1)
        
        for i, (key, upgrade) in enumerate(self.upgrades.items()):
            row = i // cards_per_row
            col = i % cards_per_row
            
            x = margin + col * (card_width + margin)
            y = 410 + row * (card_height + 20)
            
            can_afford = self.meat >= upgrade["cost"]
            color = upgrade["color"] if can_afford else DARK_GRAY
            
            self.upgrade_buttons.append({
                "key": key,
                "rect": pygame.Rect(x, y, card_width, card_height),
                "name": upgrade["name"],
                "desc": upgrade["desc"],
                "cost": upgrade["cost"],
                "count": upgrade["count"],
                "production": upgrade["production"],
                "color": color,
                "icon": upgrade["icon"],
                "button": Button(x + 20, y + card_height - 40, card_width - 40, 30, 
                               "Acheter", RED if can_afford else DARK_GRAY, BRIGHT_RED if can_afford else DARK_GRAY)
            })
            
        # Bonus upgrade buttons
        self.bonus_upgrade_buttons = []
        for i, (key, upgrade) in enumerate(self.bonus_upgrades.items()):
            # Check if requirements are met
            available = True
            for req_key, req_count in upgrade["requires"].items():
                if req_key == "meat":
                    if self.meat < req_count:
                        available = False
                else:
                    if self.upgrades[req_key]["count"] < req_count:
                        available = False
            
            if available and not upgrade["purchased"]:
                can_afford = self.meat >= upgrade["cost"]
                color = upgrade["color"] if can_afford else DARK_GRAY
                
                row = len(self.bonus_upgrade_buttons) // cards_per_row
                col = len(self.bonus_upgrade_buttons) % cards_per_row
                
                x = margin + col * (card_width + margin)
                y = 410 + row * (card_height + 20)
                
                self.bonus_upgrade_buttons.append({
                    "key": key,
                    "rect": pygame.Rect(x, y, card_width, card_height),
                    "name": upgrade["name"],
                    "desc": upgrade["desc"],
                    "cost": upgrade["cost"],
                    "color": color,
                    "button": Button(x + 20, y + card_height - 40, card_width - 40, 30, 
                                   "Acheter", RED if can_afford else DARK_GRAY, BRIGHT_RED if can_afford else DARK_GRAY)
                })
    
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
    
    def buy_upgrade(self, key):
        upgrade = self.upgrades[key]
        if self.meat >= upgrade["cost"]:
            self.meat -= upgrade["cost"]
            upgrade["count"] += 1
            # Update cost with 15% increase per purchase
            upgrade["cost"] = math.floor(upgrade["base_cost"] * (1.15 ** upgrade["count"]))
            
            self.calculate_mps()
            self.update_buttons()
            return True
        return False
    
    def buy_bonus_upgrade(self, key):
        upgrade = self.bonus_upgrades[key]
        if self.meat >= upgrade["cost"] and not upgrade["purchased"]:
            self.meat -= upgrade["cost"]
            upgrade["purchased"] = True
            
            # Apply effect
            if upgrade["affects"] == "all":
                # Double all production
                self.multiplier *= upgrade["multiplier"]
            else:
                # Increase specific upgrade's production
                target = self.upgrades[upgrade["affects"]]
                target["production"] *= upgrade["multiplier"]
            
            self.calculate_mps()
            self.update_buttons()
            return True
        return False
    
    def calculate_mps(self):
        base_mps = 0
        for upgrade in self.upgrades.values():
            base_mps += upgrade["count"] * upgrade["production"]
        
        # Apply global multiplier
        self.meat_per_second = base_mps * self.multiplier
    
    def update(self):
        now = datetime.now()
        dt = (now - self.last_update).total_seconds()
        
        # Add meat based on production rate
        self.meat += self.meat_per_second * dt
        
        # Update click animation
        if self.meat_click_effect > 0:
            self.meat_click_effect -= dt * 5
            if self.meat_click_effect < 0:
                self.meat_click_effect = 0
        
        # Update buttons based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        for tab in self.tab_buttons:
            tab["button"].update(mouse_pos)
        
        if self.current_tab == "upgrades":
            for upgrade in self.upgrade_buttons:
                upgrade["button"].update(mouse_pos)
                
            for upgrade in self.bonus_upgrade_buttons:
                upgrade["button"].update(mouse_pos)
        
        self.last_update = now
        
        # Check if new bonus upgrades are available
        self.update_buttons()
    
    def draw(self):
        # Draw background
        self.screen.fill(DARK_BG)
        
        # Draw top panel
        top_panel = pygame.Rect(0, 0, WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, DARK_GRAY, top_panel)
        pygame.draw.line(self.screen, GRAY, (0, 80), (WINDOW_WIDTH, 80), 2)
        
        # Draw meat counter
        meat_text = self.title_font.render(f"{self.format_number(self.meat)} viande", True, RED)
        self.screen.blit(meat_text, (WINDOW_WIDTH // 2 - meat_text.get_width() // 2, 20))
        
        # Draw meat per second
        mps_text = self.font.render(f"{self.format_number(self.meat_per_second)} viande/seconde", True, WHITE)
        self.screen.blit(mps_text, (WINDOW_WIDTH // 2 - mps_text.get_width() // 2, 80))
        
        # Draw meat image
        meat_img = self.meat_imgs[1 if self.meat_click_effect > 0.5 else 0]
        self.screen.blit(meat_img, self.meat_rect)
        
        # Draw click text
        click_text = self.font.render("Cliquez pour gagner de la viande!", True, WHITE)
        self.screen.blit(click_text, (WINDOW_WIDTH // 2 - click_text.get_width() // 2, 330))
        
        # Draw tabs
        for tab in self.tab_buttons:
            tab["button"].draw(self.screen)
            if self.current_tab == tab["id"]:
                # Draw indicator for active tab
                pygame.draw.rect(self.screen, tab["button"].hover_color, 
                              (tab["button"].rect.left, tab["button"].rect.bottom - 3, 
                               tab["button"].rect.width, 3))
        
        # Draw current tab content
        if self.current_tab == "upgrades":
            self.draw_upgrades()
        elif self.current_tab == "prestige":
            self.draw_prestige()
        elif self.current_tab == "stats":
            self.draw_stats()
        
        pygame.display.flip()
    
    def draw_upgrades(self):
        # Draw section title
        title = self.header_font.render("Améliorations", True, WHITE)
        self.screen.blit(title, (20, 400))
        
        # Draw bonus upgrades first (if any)
        if self.bonus_upgrade_buttons:
            bonus_title = self.font.render("Améliorations Spéciales", True, GOLD)
            self.screen.blit(bonus_title, (WINDOW_WIDTH - 300, 400))
            
            for upgrade in self.bonus_upgrade_buttons:
                pygame.draw.rect(self.screen, upgrade["color"], upgrade["rect"], border_radius=5)
                pygame.draw.rect(self.screen, GRAY, upgrade["rect"], 2, border_radius=5)
                
                # Draw name
                name = self.font.render(upgrade["name"], True, WHITE)
                self.screen.blit(name, (upgrade["rect"].left + 10, upgrade["rect"].top + 10))
                
                # Draw description
                desc = self.small_font.render(upgrade["desc"], True, WHITE)
                self.screen.blit(desc, (upgrade["rect"].left + 10, upgrade["rect"].top + 40))
                
                # Draw cost
                cost = self.small_font.render(f"Coût: {self.format_number(upgrade['cost'])}", True, WHITE)
                self.screen.blit(cost, (upgrade["rect"].left + 10, upgrade["rect"].top + 70))
                
                # Draw button
                upgrade["button"].draw(self.screen)
        
        # Draw regular upgrades
        for upgrade in self.upgrade_buttons:
            pygame.draw.rect(self.screen, upgrade["color"], upgrade["rect"], border_radius=5)
            pygame.draw.rect(self.screen, GRAY, upgrade["rect"], 2, border_radius=5)
            
            # Draw icon
            icon = self.header_font.render(upgrade["icon"], True, WHITE)
            self.screen.blit(icon, (upgrade["rect"].right - 40, upgrade["rect"].top + 10))
            
            # Draw name
            name = self.font.render(upgrade["name"], True, WHITE)
            self.screen.blit(name, (upgrade["rect"].left + 10, upgrade["rect"].top + 10))
            
            # Draw count
            count = self.small_font.render(f"Niveau: {upgrade['count']}", True, WHITE)
            self.screen.blit(count, (upgrade["rect"].left + 10, upgrade["rect"].top + 40))
            
            # Draw production
            production = self.small_font.render(f"+{self.format_number(upgrade['production'])}/s", True, GREEN)
            self.screen.blit(production, (upgrade["rect"].left + 10, upgrade["rect"].top + 60))
            
            # Draw total production
            total = self.small_font.render(f"Total: {self.format_number(upgrade['production'] * upgrade['count'])}/s", True, GREEN)
            self.screen.blit(total, (upgrade["rect"].left + 10, upgrade["rect"].top + 80))
            
            # Draw cost
            cost = self.small_font.render(f"Coût: {self.format_number(upgrade['cost'])}", True, WHITE)
            self.screen.blit(cost, (upgrade["rect"].left + 10, upgrade["rect"].top + 100))
            
            # Draw button
            upgrade["button"].draw(self.screen)
    
    def draw_prestige(self):
        # Placeholder for prestige tab
        text = self.header_font.render("Prestige (à venir)", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 450))
        
        info = self.font.render("Réinitialisez votre progression pour des bonus permanents", True, WHITE)
        self.screen.blit(info, (WINDOW_WIDTH // 2 - info.get_width() // 2, 500))
        
        # Show prestige button if enough meat
        if self.meat >= 1e6:
            points = math.floor(math.log(self.meat / 1e6, 10))
            if points > 0:
                prestige_btn = Button(WINDOW_WIDTH // 2 - 150, 550, 300, 50, 
                                   f"Prestige pour {points} points", GOLD, (255, 230, 100))
                prestige_btn.update(pygame.mouse.get_pos())
                prestige_btn.draw(self.screen)
    
    def draw_stats(self):
        # Placeholder for stats tab
        text = self.header_font.render("Statistiques", True, WHITE)
        self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 450))
        
        # Display stats
        stats = [
            f"Total de clics: {self.total_clicks}",
            f"Viande par clic: {self.format_number(self.meat_per_click)}",
            f"Viande par seconde: {self.format_number(self.meat_per_second)}",
            f"Multiplicateur global: x{self.format_number(self.multiplier)}",
            f"Prestige points: {self.prestige_points}"
        ]
        
        for i, stat in enumerate(stats):
            stat_text = self.font.render(stat, True, WHITE)
            self.screen.blit(stat_text, (WINDOW_WIDTH // 2 - stat_text.get_width() // 2, 500 + i * 40))
    
    def handle_click(self, pos):
        # Handle meat click
        if self.meat_rect.collidepoint(pos):
            self.meat += self.meat_per_click * self.multiplier
            self.total_clicks += 1
            self.meat_click_effect = 1.0
            return
        
        # Handle tab clicks
        for tab in self.tab_buttons:
            if tab["button"].is_clicked(pos, True):
                self.current_tab = tab["id"]
                return
        
        # Handle upgrade buttons based on current tab
        if self.current_tab == "upgrades":
            # Handle bonus upgrades
            for upgrade in self.bonus_upgrade_buttons:
                if upgrade["button"].is_clicked(pos, True):
                    self.buy_bonus_upgrade(upgrade["key"])
                    return
            
            # Handle regular upgrades
            for upgrade in self.upgrade_buttons:
                if upgrade["button"].is_clicked(pos, True):
                    self.buy_upgrade(upgrade["key"])
                    return
        
        elif self.current_tab == "prestige":
            # Handle prestige button
            if self.meat >= 1e6:
                points = math.floor(math.log(self.meat / 1e6, 10))
                if points > 0:
                    prestige_btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 550, 300, 50)
                    if prestige_btn_rect.collidepoint(pos):
                        self.prestige_points += points
                        self.meat = 0
                        for upgrade in self.upgrades.values():
                            upgrade["count"] = 0
                            upgrade["cost"] = upgrade["base_cost"]
                        
                        # Reset bonus upgrades
                        for upgrade in self.bonus_upgrades.values():
                            upgrade["purchased"] = False
                        
                        # Set multiplier based on prestige points
                        self.multiplier = 1 + (self.prestige_points * 0.1)
                        
                        self.calculate_mps()
                        self.update_buttons()
                        return

def main():
    game = MeatClicker()
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