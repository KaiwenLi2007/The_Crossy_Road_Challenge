import pygame
import random
import os

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
TILE_SIZE = 50
FPS = 60
HS_FILE = "highscore.txt"

# --- Theme Data ---
THEME_KEYS = ["Classic", "Urban", "Lava"]
THEMES = {
    "Classic": {
        "safe": (86, 176, 0), "road": (44, 44, 44), "line": (120, 120, 120),
        "sky": (135, 206, 235), "hill_dark": (34, 139, 34), "hill_light": (50, 205, 50),
        "accent": (255, 255, 255), "water": (30, 144, 255)
    },
    "Urban": {
        "safe": (100, 100, 110), "road": (20, 20, 25), "line": (255, 215, 0),
        "sky": (10, 10, 30), "build_dark": (25, 25, 45), "build_lite": (40, 40, 65),
        "accent": (255, 255, 100), "water": (20, 80, 150)
    },
    "Lava": {
        "safe": (40, 10, 10), "road": (120, 25, 0), "line": (255, 100, 0),
        "sky": (25, 5, 5), "rock_dark": (15, 0, 0), "rock_lite": (60, 15, 0),
        "accent": (255, 60, 0), "water": (100, 30, 0)
    }
}

SKIN_KEYS = ["Chicken", "Robot", "Alien"]

class SpriteGenerator:
    @staticmethod
    def draw_player(skin):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        c = TILE_SIZE // 2
        if skin == "Chicken":
            pygame.draw.circle(surf, (255, 255, 255), (c, c), 18)
            pygame.draw.rect(surf, (220, 0, 0), (c - 4, 4, 8, 10), border_radius=3)
            pygame.draw.circle(surf, (0, 0, 0), (c + 8, c - 4), 3)
            pygame.draw.polygon(surf, (255, 165, 0), [(c + 18, c), (c + 10, c - 4), (c + 10, c + 4)])
            # Feet
            pygame.draw.line(surf, (255, 165, 0), (c - 5, c + 15), (c - 5, c + 22), 3)
            pygame.draw.line(surf, (255, 165, 0), (c + 5, c + 15), (c + 5, c + 22), 3)
        elif skin == "Robot":
            pygame.draw.rect(surf, (140, 140, 150), (10, 10, 30, 30), border_radius=5)
            pygame.draw.rect(surf, (0, 255, 255), (14, 18, 22, 6))
            pygame.draw.line(surf, (100, 100, 100), (c, 10), (c, 4), 2)
            pygame.draw.circle(surf, (255, 0, 0), (c, 4), 3)
            # Side Bolts
            pygame.draw.circle(surf, (80, 80, 80), (12, 15), 2)
            pygame.draw.circle(surf, (80, 80, 80), (38, 15), 2)
        elif skin == "Alien":
            pygame.draw.ellipse(surf, (50, 220, 50), (12, 6, 26, 40))
            pygame.draw.ellipse(surf, (0, 0, 0), (c - 10, c - 8, 9, 15))
            pygame.draw.ellipse(surf, (0, 0, 0), (c + 1, c - 8, 9, 15))
            # Glowing Antennas
            pygame.draw.line(surf, (50, 220, 50), (c - 5, 10), (c - 12, 2), 2)
            pygame.draw.line(surf, (50, 220, 50), (c + 5, 10), (c + 12, 2), 2)
        return surf

    @staticmethod
    def draw_car(width, theme, direction):
        surf = pygame.Surface((width, TILE_SIZE), pygame.SRCALPHA)
        h = TILE_SIZE
        
        if theme == "Classic":
            main_c = random.choice([(190, 30, 30), (30, 100, 190), (210, 170, 0)])
            dark_c = (max(0, main_c[0]-40), max(0, main_c[1]-40), max(0, main_c[2]-40))
            
            # Chassis shadow
            pygame.draw.rect(surf, dark_c, (5, 14, width - 10, h - 20), border_radius=12)
            # Main body
            pygame.draw.rect(surf, main_c, (5, 8, width - 10, h - 20), border_radius=12)
            # Roofline
            pygame.draw.rect(surf, main_c, (12, 4, width - 24, 8), border_radius=3)
            
            # Wheels with detail
            for x in [20, width - 25]:
                # Tire
                pygame.draw.circle(surf, (10, 10, 10), (x, h - 8), 8)
                # Rim
                pygame.draw.circle(surf, (180, 180, 180), (x, h - 8), 5)
                pygame.draw.circle(surf, (220, 220, 220), (x, h - 8), 2)
            
            # Windows
            if direction > 0:
                # Rear window
                pygame.draw.rect(surf, (220, 240, 255), (8, 10, 18, 12), border_radius=3)
                pygame.draw.line(surf, (180, 200, 220), (17, 10), (17, 22), 1)
                # Front window
                pygame.draw.rect(surf, (220, 240, 255), (width - 26, 10, 18, 12), border_radius=3)
                pygame.draw.line(surf, (180, 200, 220), (width - 17, 10), (width - 17, 22), 1)
            else:
                # Rear window
                pygame.draw.rect(surf, (220, 240, 255), (width - 26, 10, 18, 12), border_radius=3)
                pygame.draw.line(surf, (180, 200, 220), (width - 17, 10), (width - 17, 22), 1)
                # Front window
                pygame.draw.rect(surf, (220, 240, 255), (8, 10, 18, 12), border_radius=3)
                pygame.draw.line(surf, (180, 200, 220), (17, 10), (17, 22), 1)
            
            # Headlights
            if direction > 0:
                pygame.draw.circle(surf, (255, 255, 150), (width - 4, h // 2 - 4), 2)
                pygame.draw.circle(surf, (255, 255, 150), (width - 4, h // 2 + 4), 2)
            else:
                pygame.draw.circle(surf, (255, 255, 150), (4, h // 2 - 4), 2)
                pygame.draw.circle(surf, (255, 255, 150), (4, h // 2 + 4), 2)
            
            # Taillights
            if direction > 0:
                pygame.draw.circle(surf, (200, 0, 0), (2, h // 2 - 4), 2)
                pygame.draw.circle(surf, (200, 0, 0), (2, h // 2 + 4), 2)
            else:
                pygame.draw.circle(surf, (200, 0, 0), (width - 2, h // 2 - 4), 2)
                pygame.draw.circle(surf, (200, 0, 0), (width - 2, h // 2 + 4), 2)
            
            # Door line
            pygame.draw.line(surf, dark_c, (width // 2, 12), (width // 2, h - 12), 1)
            
        elif theme == "Urban":
            is_taxi = random.random() > 0.7
            body_c = (240, 190, 0) if is_taxi else (40, 45, 55)
            shadow_c = (max(0, body_c[0]-20), max(0, body_c[1]-20), max(0, body_c[2]-20))
            
            # Shadow base
            pygame.draw.rect(surf, (10, 10, 10), (2, 10, width - 4, h - 16), border_radius=5)
            # Main body
            pygame.draw.rect(surf, body_c, (2, 6, width - 4, h - 16), border_radius=5)
            # Roof accent
            pygame.draw.rect(surf, shadow_c, (4, 4, width - 8, 3), border_radius=2)
            
            # Wheels
            for x in [18, width - 18]:
                pygame.draw.circle(surf, (0, 0, 0), (x, h - 6), 7)
                pygame.draw.circle(surf, (100, 100, 100), (x, h - 6), 4)
                pygame.draw.circle(surf, (150, 150, 150), (x, h - 6), 1)
            
            # Windows (modern style)
            if direction > 0:
                pygame.draw.rect(surf, (100, 150, 200), (10, 8, 16, 10), border_radius=2)
                pygame.draw.rect(surf, (100, 150, 200), (width - 26, 8, 16, 10), border_radius=2)
            else:
                pygame.draw.rect(surf, (100, 150, 200), (width - 26, 8, 16, 10), border_radius=2)
                pygame.draw.rect(surf, (100, 150, 200), (10, 8, 16, 10), border_radius=2)
            
            # LED Headlights
            if direction > 0:
                pygame.draw.rect(surf, (200, 200, 100), (width - 5, h // 2 - 5, 3, 3), border_radius=1)
                pygame.draw.rect(surf, (200, 200, 100), (width - 5, h // 2 + 2, 3, 3), border_radius=1)
            else:
                pygame.draw.rect(surf, (200, 200, 100), (2, h // 2 - 5, 3, 3), border_radius=1)
                pygame.draw.rect(surf, (200, 200, 100), (2, h // 2 + 2, 3, 3), border_radius=1)
            
            # LED Taillights
            if direction > 0:
                pygame.draw.rect(surf, (255, 0, 0), (2, h // 2 - 5, 3, 3), border_radius=1)
                pygame.draw.rect(surf, (255, 0, 0), (2, h // 2 + 2, 3, 3), border_radius=1)
            else:
                pygame.draw.rect(surf, (255, 0, 0), (width - 5, h // 2 - 5, 3, 3), border_radius=1)
                pygame.draw.rect(surf, (255, 0, 0), (width - 5, h // 2 + 2, 3, 3), border_radius=1)
            
            # Door line
            pygame.draw.line(surf, shadow_c, (width // 2, 8), (width // 2, h - 8), 1)
            
            # Taxi top sign
            if is_taxi:
                pygame.draw.rect(surf, (0, 0, 0), (width // 2 - 14, 2, 28, 4), border_radius=1)
                pygame.draw.rect(surf, (255, 255, 255), (width // 2 - 12, 3, 24, 2))
                
        elif theme == "Lava":
            # Obsidian body
            pygame.draw.rect(surf, (20, 20, 25), (4, 8, width - 8, h - 16), border_radius=4)
            pygame.draw.rect(surf, (40, 30, 35), (4, 6, width - 8, 4), border_radius=2)
            
            # Heat vents/grill
            for x in [12, width // 2, width - 12]:
                pygame.draw.line(surf, (100, 40, 20), (x, 10), (x, h - 10), 2)
                pygame.draw.line(surf, (60, 20, 15), (x - 2, 10), (x - 2, h - 10), 1)
            
            # Magma exhaust core
            core_x = 0 if direction > 0 else width - 12
            pygame.draw.circle(surf, (255, 100, 0), (core_x + 6, h // 2), 8)
            pygame.draw.circle(surf, (255, 180, 0), (core_x + 6, h // 2), 4)
            
            # Wheels (glowing)
            for x in [16, width - 16]:
                pygame.draw.circle(surf, (10, 5, 5), (x, h - 6), 7)
                pygame.draw.circle(surf, (100, 40, 20), (x, h - 6), 4)
                pygame.draw.circle(surf, (255, 100, 0), (x, h - 6), 1)
            
            # Heat radiation lines
            if direction > 0:
                for i in range(3):
                    pygame.draw.line(surf, (255, 80, 20), (width - 12 - i*4, h // 2), (width - 8 - i*4, h // 2 - 3), 1)
                    pygame.draw.line(surf, (255, 80, 20), (width - 12 - i*4, h // 2), (width - 8 - i*4, h // 2 + 3), 1)
            else:
                for i in range(3):
                    pygame.draw.line(surf, (255, 80, 20), (12 + i*4, h // 2), (8 + i*4, h // 2 - 3), 1)
                    pygame.draw.line(surf, (255, 80, 20), (12 + i*4, h // 2), (8 + i*4, h // 2 + 3), 1)
            
        return surf

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.skin = "Chicken"
        self.image = SpriteGenerator.draw_player(self.skin)
        self.rect = self.image.get_rect()
        self.move_delay = 140
        self.last_move = 0
        self.game = None  # Reference to game for collision checking
        self.reset()

    def set_game(self, game):
        self.game = game

    def update_skin(self, skin_name):
        self.skin = skin_name
        self.image = SpriteGenerator.draw_player(self.skin)

    def reset(self):
        self.grid_x, self.grid_y = 6, (SCREEN_HEIGHT // TILE_SIZE) - 1
        self.max_reached_y = self.grid_y
        self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)

    def move(self, dx, dy):
        now = pygame.time.get_ticks()
        if now - self.last_move > self.move_delay:
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            # Boundary check
            if not (0 <= new_x < (SCREEN_WIDTH // TILE_SIZE)): return False
            if not (0 <= new_y < (SCREEN_HEIGHT // TILE_SIZE)): return False
            
            # Check for tree collision (block movement)
            if self.game:
                temp_sprite = pygame.sprite.Sprite()
                temp_sprite.rect = pygame.Rect(new_x * TILE_SIZE, new_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if pygame.sprite.spritecollide(temp_sprite, self.game.trees, False):
                    return False  # Block movement if tree is there
            
            self.grid_x = new_x
            self.grid_y = new_y
            self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)
            self.last_move = now
            return True
        return False

class Car(pygame.sprite.Sprite):
    def __init__(self, lane_y, speed, theme):
        super().__init__()
        self.speed = speed
        self.image = SpriteGenerator.draw_car(random.randint(95, 130), theme, speed)
        self.rect = self.image.get_rect(topleft=(random.randint(0, SCREEN_WIDTH), lane_y))

    def update(self):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0: self.rect.left = SCREEN_WIDTH

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, theme):
        super().__init__()
        self.theme = theme
        self.image = self.draw_tree(theme)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    @staticmethod
    def draw_tree(theme):
        surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        c = TILE_SIZE // 2
        
        if theme == "Classic":
            # Trunk
            pygame.draw.rect(surf, (101, 67, 33), (c - 4, c + 5, 8, 15), border_radius=2)
            # Foliage layers
            pygame.draw.circle(surf, (34, 139, 34), (c, c - 5), 15)
            pygame.draw.circle(surf, (50, 205, 50), (c - 8, c + 2), 12)
            pygame.draw.circle(surf, (50, 205, 50), (c + 8, c + 2), 12)
        elif theme == "Urban":
            # Metal pole
            pygame.draw.rect(surf, (120, 120, 130), (c - 3, c - 8, 6, 25), border_radius=3)
            # Light fixture
            pygame.draw.rect(surf, (255, 200, 0), (c - 8, c - 10, 16, 4), border_radius=2)
            pygame.draw.circle(surf, (255, 255, 150), (c, c - 8), 3)
        elif theme == "Lava":
            # Rock formation
            pygame.draw.polygon(surf, (60, 15, 0), [(c, 5), (c + 12, c), (c, c + 15), (c - 12, c)])
            pygame.draw.circle(surf, (100, 40, 20), (c, c), 8)
            pygame.draw.polygon(surf, (80, 20, 0), [(c - 3, c - 5), (c + 3, c - 5), (c + 2, c + 5)])
        
        return surf

class Bridge(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, theme):
        super().__init__()
        self.speed = speed
        self.theme = theme
        self.image = self.draw_bridge(theme)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x_float = float(x)
        # Safe zone is only the middle part of the bridge
        self.safe_left = 8
        self.safe_right = self.safe_left + TILE_SIZE - 4
    
    @staticmethod
    def draw_bridge(theme):
        surf = pygame.Surface((TILE_SIZE + 20, TILE_SIZE), pygame.SRCALPHA)
        
        if theme == "Classic":
            # Wooden bridge with unsafe edges (darker)
            pygame.draw.rect(surf, (80, 40, 20), (0, TILE_SIZE // 2, TILE_SIZE + 20, 15), border_radius=3)  # Unsafe edges
            pygame.draw.rect(surf, (139, 90, 43), (8, TILE_SIZE // 2, TILE_SIZE - 4, 15), border_radius=3)   # Safe middle
            for i in range(8, TILE_SIZE + 4, 8):
                pygame.draw.line(surf, (101, 67, 33), (i, TILE_SIZE // 2), (i, TILE_SIZE // 2 + 15), 2)
        elif theme == "Urban":
            # Metal bridge with unsafe edges (darker)
            pygame.draw.rect(surf, (60, 60, 80), (0, TILE_SIZE // 2, TILE_SIZE + 20, 15), border_radius=2)   # Unsafe edges
            pygame.draw.rect(surf, (100, 100, 120), (8, TILE_SIZE // 2, TILE_SIZE - 4, 15), border_radius=2)  # Safe middle
            pygame.draw.rect(surf, (150, 150, 170), (10, TILE_SIZE // 2 + 2, TILE_SIZE - 8, 11))
            for i in range(8, TILE_SIZE + 4, 6):
                pygame.draw.line(surf, (80, 80, 100), (i, TILE_SIZE // 2 + 7), (i, TILE_SIZE // 2 + 13), 1)
        elif theme == "Lava":
            # Obsidian bridge with unsafe crumbling edges
            pygame.draw.rect(surf, (20, 5, 5), (0, TILE_SIZE // 2, TILE_SIZE + 20, 15), border_radius=3)      # Unsafe edges (crumbling)
            pygame.draw.rect(surf, (40, 10, 10), (8, TILE_SIZE // 2, TILE_SIZE - 4, 15), border_radius=3)     # Safe middle
            pygame.draw.rect(surf, (80, 20, 20), (10, TILE_SIZE // 2 + 2, TILE_SIZE - 8, 11))
            for i in range(8, TILE_SIZE + 4, 8):
                pygame.draw.circle(surf, (255, 100, 0), (i, TILE_SIZE // 2 + 7), 1)
        
        return surf
    
    def update(self):
        self.x_float += self.speed
        if self.speed > 0 and self.x_float > SCREEN_WIDTH + 20:
            self.x_float = -TILE_SIZE - 20
        elif self.speed < 0 and self.x_float < -TILE_SIZE - 40:
            self.x_float = SCREEN_WIDTH
        self.rect.x = int(self.x_float)
    
    def is_safe(self, player_rect):
        """Check if player is on the safe part of the bridge"""
        # Only the middle section is safe
        bridge_safe_left = self.rect.x + self.safe_left
        bridge_safe_right = self.rect.x + self.safe_right
        player_center = player_rect.centerx
        return bridge_safe_left <= player_center <= bridge_safe_right

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Crossy Road: Ultra Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_title = pygame.font.SysFont("Impact", 110)
        self.font_ui = pygame.font.SysFont("Verdana", 26, bold=True)
        self.font_key = pygame.font.SysFont("Courier New", 20, bold=True)
        
        self.state = "MENU"
        self.theme_idx = 0
        self.skin_idx = 0
        self.score = 0
        self.high_score = self.load_hs()
        self.player = Player()
        self.player.set_game(self)  # Set game reference for collision checks
        self.cars = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.bridges = pygame.sprite.Group()
        self.lane_data = []
        self.lane_types = []  # "safe", "road", "river"

    def load_hs(self):
        if os.path.exists(HS_FILE):
            try:
                with open(HS_FILE, "r") as f:
                    return int(f.read().strip())
            except: return 0
        return 0

    def setup_level(self):
        self.cars.empty()
        self.trees.empty()
        self.bridges.empty()
        self.lane_data = []
        self.lane_types = []
        theme_name = THEME_KEYS[self.theme_idx]
        
        for i in range(SCREEN_HEIGHT // TILE_SIZE):
            if i == 0 or i == (SCREEN_HEIGHT // TILE_SIZE) - 1 or (i % 3 == 0):
                self.lane_data.append("safe")
                self.lane_types.append("safe")
                # Add more trees to safe zones (but not start/end)
                if i != 0 and i != (SCREEN_HEIGHT // TILE_SIZE) - 1 and random.random() > 0.4:
                    num_trees = random.randint(2, 4)
                    available_positions = list(range(SCREEN_WIDTH // TILE_SIZE))
                    tree_positions = random.sample(available_positions, min(num_trees, len(available_positions)))
                    for tx in tree_positions:
                        self.trees.add(Tree(tx * TILE_SIZE, i * TILE_SIZE, theme_name))
            elif random.random() > 0.85:  # 15% chance for river
                self.lane_data.append("water")
                self.lane_types.append("river")
                # Add moving bridges with reduced spawning (fewer bridges per river)
                speed = random.uniform(0.3, 0.6) * random.choice([-1, 1])
                for bx in range(-TILE_SIZE, SCREEN_WIDTH + TILE_SIZE, TILE_SIZE * 2):
                    self.bridges.add(Bridge(bx, i * TILE_SIZE, int(speed) if speed != 0 else 1, theme_name))
            else:
                self.lane_data.append("road")
                self.lane_types.append("road")
                s = (random.uniform(2.5, 4.5) + (self.score / 55)) * random.choice([-1, 1])
                self.cars.add(Car(i * TILE_SIZE, int(s) if s != 0 else 2, theme_name))

    def draw_menu_scene(self):
        t_key = THEME_KEYS[self.theme_idx]
        t = THEMES[t_key]
        self.screen.fill(t["sky"])

        if t_key == "Urban":
            for _ in range(30):
                pygame.draw.circle(self.screen, (255, 255, 255), (random.randint(0, 600), random.randint(0, 400)), 1)
            for i in range(0, SCREEN_WIDTH, 100):
                h = 280 + (i * 13 % 180)
                pygame.draw.rect(self.screen, t["build_dark"], (i, SCREEN_HEIGHT - h, 90, h))
                for wy in range(SCREEN_HEIGHT - h + 30, SCREEN_HEIGHT, 45):
                    if (i + wy) % 4 != 0:
                        pygame.draw.rect(self.screen, t["accent"], (i + 20, wy, 15, 15), border_radius=2)
            pygame.draw.circle(self.screen, (230, 230, 230), (520, 100), 45)
            pygame.draw.circle(self.screen, t["sky"], (490, 100), 45)

        elif t_key == "Classic":
            pygame.draw.circle(self.screen, (255, 230, 0), (520, 80), 50)
            for cx in [70, 420]:
                for off in [0, 35, 70]:
                    pygame.draw.circle(self.screen, (255, 255, 255), (cx + off, 50), 30 + (off % 20))
            pygame.draw.ellipse(self.screen, t["hill_dark"], (-200, 480, 700, 500))
            pygame.draw.ellipse(self.screen, t["hill_light"], (100, 520, 750, 500))
            for i in range(5): # Trees
                tx = 50 + i * 120
                pygame.draw.rect(self.screen, (100, 60, 20), (tx, 550, 10, 40))
                pygame.draw.circle(self.screen, (34, 100, 34), (tx + 5, 540), 25)

        elif t_key == "Lava":
            for i in range(3):
                pygame.draw.polygon(self.screen, t["rock_dark"], [(i*250-100, 800), (i*250+100, 350), (i*250+300, 800)])
            pygame.draw.rect(self.screen, (255, 40, 0), (0, 740, 600, 60))
            for _ in range(15):
                pygame.draw.circle(self.screen, (255, 120, 0), (random.randint(0, 600), random.randint(300, 740)), 3)

    def draw_button(self, label, value, y, key_pair):
        # Container
        pygame.draw.rect(self.screen, (0, 0, 0, 140), (60, y - 10, 480, 60), border_radius=15)
        # Keys
        for i, k in enumerate(key_pair):
            kx = 75 if i == 0 else 485
            pygame.draw.rect(self.screen, (80, 80, 90), (kx, y, 40, 40), border_radius=8)
            pygame.draw.rect(self.screen, (120, 120, 130), (kx, y, 40, 36), border_radius=8)
            k_surf = self.font_key.render(k, True, (20, 20, 20))
            self.screen.blit(k_surf, (kx + 20 - k_surf.get_width() // 2, y + 8))
        # Text
        main_surf = self.font_ui.render(f"{label}: {value}", True, (255, 255, 255))
        self.screen.blit(main_surf, (SCREEN_WIDTH // 2 - main_surf.get_width() // 2, y + 2))

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key == pygame.K_RIGHT: self.theme_idx = (self.theme_idx + 1) % len(THEME_KEYS)
                        elif event.key == pygame.K_LEFT: self.theme_idx = (self.theme_idx - 1) % len(THEME_KEYS)
                        elif event.key == pygame.K_d: 
                            self.skin_idx = (self.skin_idx + 1) % len(SKIN_KEYS)
                            self.player.update_skin(SKIN_KEYS[self.skin_idx])
                        elif event.key == pygame.K_a:
                            self.skin_idx = (self.skin_idx - 1) % len(SKIN_KEYS)
                            self.player.update_skin(SKIN_KEYS[self.skin_idx])
                        elif event.key == pygame.K_SPACE:
                            self.score, self.state = 0, "PLAYING"
                            self.player.reset()
                            self.setup_level()
                    elif self.state == "GAMEOVER" and event.key == pygame.K_r: self.state = "MENU"

            if self.state == "PLAYING":
                k = pygame.key.get_pressed()
                moved = False
                if k[pygame.K_UP]: moved = self.player.move(0, -1)
                elif k[pygame.K_DOWN]: moved = self.player.move(0, 1)
                elif k[pygame.K_LEFT]: moved = self.player.move(-1, 0)
                elif k[pygame.K_RIGHT]: moved = self.player.move(1, 0)
                
                if moved and self.player.grid_y < self.player.max_reached_y:
                    self.score += 1
                    self.player.max_reached_y = self.player.grid_y
                
                self.cars.update()
                self.bridges.update()
                
                # Check collision with cars
                if pygame.sprite.spritecollide(self.player, self.cars, False):
                    if self.score > self.high_score:
                        self.high_score = self.score
                        with open(HS_FILE, "w") as f: f.write(str(self.high_score))
                    self.state = "GAMEOVER"
                
                # Check if player is on river - must be on safe part of a bridge or die
                player_lane = self.player.grid_y
                if player_lane < len(self.lane_types) and self.lane_types[player_lane] == "river":
                    on_bridge = pygame.sprite.spritecollide(self.player, self.bridges, False)
                    if not on_bridge:
                        # Not on a bridge - fall in river and die
                        if self.score > self.high_score:
                            self.high_score = self.score
                            with open(HS_FILE, "w") as f: f.write(str(self.high_score))
                        self.state = "GAMEOVER"
                    else:
                        # Check if player is on the safe part of the bridge
                        bridge = on_bridge[0]
                        if not bridge.is_safe(self.player.rect):
                            # On unsafe edge of bridge - die
                            if self.score > self.high_score:
                                self.high_score = self.score
                                with open(HS_FILE, "w") as f: f.write(str(self.high_score))
                            self.state = "GAMEOVER"
                
                if self.player.grid_y == 0:
                    self.score += 10
                    self.player.reset()
                    self.setup_level()

            # Render
            if self.state == "MENU":
                self.draw_menu_scene()
                title = self.font_title.render("CROSSY", True, (255, 255, 255))
                self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 110))
                self.draw_button("THEME", THEME_KEYS[self.theme_idx], 420, ["<", ">"])
                self.draw_button("SKIN", SKIN_KEYS[self.skin_idx], 500, ["A", "D"])
                prompt = self.font_ui.render("PRESS SPACE TO START", True, (255, 255, 255))
                self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 680))
            else:
                curr_t = THEMES[THEME_KEYS[self.theme_idx]]
                theme_name = THEME_KEYS[self.theme_idx]
                
                # Draw lanes with road markings
                for i, l_type in enumerate(self.lane_data):
                    if l_type == "water":
                        # Draw river with water effect
                        pygame.draw.rect(self.screen, curr_t["water"], (0, i * TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))
                        
                        if theme_name == "Classic":
                            # Water ripples
                            for x in range(0, SCREEN_WIDTH, 20):
                                pygame.draw.line(self.screen, (70, 170, 255), (x, i * TILE_SIZE + 10), 
                                                (x + 10, i * TILE_SIZE + 10), 1)
                                pygame.draw.line(self.screen, (70, 170, 255), (x, i * TILE_SIZE + 30), 
                                                (x + 10, i * TILE_SIZE + 30), 1)
                        elif theme_name == "Urban":
                            # Tech water
                            for x in range(0, SCREEN_WIDTH, 25):
                                pygame.draw.line(self.screen, (100, 150, 200), (x, i * TILE_SIZE + 15), 
                                                (x + 12, i * TILE_SIZE + 15), 2)
                        elif theme_name == "Lava":
                            # Lava flow
                            for x in range(0, SCREEN_WIDTH, 20):
                                pygame.draw.circle(self.screen, (255, 100, 0), (x, i * TILE_SIZE + 15), 3)
                    else:
                        pygame.draw.rect(self.screen, curr_t[l_type], (0, i * TILE_SIZE, SCREEN_WIDTH, TILE_SIZE))
                        
                        # Add road lane markings
                        if l_type == "road":
                            if theme_name == "Classic":
                                # Yellow dashed center lines
                                for x in range(0, SCREEN_WIDTH, 40):
                                    pygame.draw.line(self.screen, curr_t["line"], (x, i * TILE_SIZE + TILE_SIZE // 2), 
                                                    (x + 20, i * TILE_SIZE + TILE_SIZE // 2), 3)
                            elif theme_name == "Urban":
                                # Yellow dashed lines with edge markings
                                for x in range(0, SCREEN_WIDTH, 35):
                                    pygame.draw.line(self.screen, curr_t["line"], (x, i * TILE_SIZE + TILE_SIZE // 2), 
                                                    (x + 18, i * TILE_SIZE + TILE_SIZE // 2), 2)
                                # Edge lines
                                pygame.draw.line(self.screen, (100, 100, 100), (0, i * TILE_SIZE), 
                                                (SCREEN_WIDTH, i * TILE_SIZE), 1)
                            elif theme_name == "Lava":
                                # Orange magma flow lines
                                for x in range(0, SCREEN_WIDTH, 40):
                                    pygame.draw.line(self.screen, curr_t["line"], (x, i * TILE_SIZE + TILE_SIZE // 2), 
                                                    (x + 20, i * TILE_SIZE + TILE_SIZE // 2), 2)
                                # Lava cracks
                                pygame.draw.line(self.screen, (80, 15, 5), (0, i * TILE_SIZE + 8), 
                                                (SCREEN_WIDTH, i * TILE_SIZE + 8), 1)
                
                self.bridges.draw(self.screen)
                self.cars.draw(self.screen)
                self.trees.draw(self.screen)
                self.screen.blit(self.player.image, self.player.rect)
                score_txt = self.font_ui.render(f"SCORE: {self.score}", True, (255, 255, 255))
                self.screen.blit(score_txt, (20, 20))
                
                if self.state == "GAMEOVER":
                    overlay = pygame.Surface((600, 800), pygame.SRCALPHA); overlay.fill((0, 0, 0, 200))
                    self.screen.blit(overlay, (0, 0))
                    go_msg = self.font_title.render("CRASHED", True, (255, 60, 60))
                    self.screen.blit(go_msg, (SCREEN_WIDTH // 2 - go_msg.get_width() // 2, 300))
                    restart = self.font_ui.render("Press 'R' for Menu", True, (255, 255, 255))
                    self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 450))

            pygame.display.flip()

if __name__ == "__main__":
    
    Game().run()