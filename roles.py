# Class Declarations for Hero and Enemy Archetypes, as well as the Dialog class object

import pygame
import random
import os

pygame.font.init()
WIDTH, HEIGHT = 800, 600

# Defining Text Fonts
combat_font = pygame.font.SysFont("comicsans", 25, bold=False)
dialog_font = pygame.font.SysFont("arial", 15)
ui_font = pygame.font.SysFont("arial", 25)

#Loading Art Assets using OS Module to join path locations of assets
HERO_WARRIOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "hero_warrior.png")), (200,200))
HERO_ROGUE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "hero_rogue.png")), (200,200))
HERO_WIZARD = pygame.transform.scale(pygame.image.load(os.path.join("assets", "hero_wizard.png")), (200,200))
NARRATOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "narrator.png")), (100,100))
MINH = pygame.transform.scale(pygame.image.load(os.path.join("assets", "minh.png")), (200,200))

# Enemy Art Assets
MOB_WARRIOR = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mob_warrior.png")), (200,200))
MOB_ROGUE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mob_rogue.png")), (200,200))
MOB_WIZARD = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mob_wizard.png")), (200,200))
BOSS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mob_boss.png")), (300,300))

# Speech Bubble/Text Class

class Dialog:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self.text = text
        self.text_label = dialog_font.render(f"{self.text}", 1, (255, 255, 255))
        self.rect = self.text_label.get_rect(topleft=(self.x, self.y))
        
        #Background object for Speech bubbles
        self.bg_rect = self.rect.copy()
        self.bg_rect.inflate_ip(10, 10)

        #Frame
        self.frame_rect = self.bg_rect.copy()
        self.frame_rect.inflate_ip(4, 4)

    def draw(self, window):
        pygame.draw.rect(window, (172,159,159), self.frame_rect, border_radius=6)
        pygame.draw.rect(window, (84, 56, 56), self.bg_rect, border_radius=6)
        window.blit(self.text_label, self.rect)

class Storylines(Dialog):
    def __init__(self, text, x, y):
        super().__init__(text, x, y)
        self.rect = self.text_label.get_rect(center=(self.x, self.y))
        self.bg_rect = self.rect.copy()
        self.bg_rect.inflate_ip(10, 10)
        self.frame_rect = self.bg_rect.copy()
        self.frame_rect.inflate_ip(4, 4)
    
    def draw(self, window):
        pygame.draw.rect(window, (172,159,159), self.frame_rect, border_radius=6)
        pygame.draw.rect(window, (59, 95, 101), self.bg_rect, border_radius=6)
        window.blit(self.text_label, self.rect)
    
# Hero Class Declaration and Methods

class Hero:
    def __init__(self, name, x, y):
            self.x = x
            self.y = y
            self.img = None
            self.name = name
            self.status = "normal"
    
    def __repr__(self):
        return self.name

# Class Methods for Drawing Hero and Speech Bubbles

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def speech(self, text):
        speech = Dialog(text, 50 + self.img.get_width() + 10, self.y + 5)
        return speech

# Subclasses

class Warrior(Hero):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.img = HERO_WARRIOR
        self.hitpoints = 200
        self.atk = 7
        self.defense = 15
        self.sp_atk = 1
        self.sp_defense = 12
        self.inventory = {'health potion': 1, 'magical gem': 0, 'sharpening stone': 2, 'potion of weakness': 0}

class Rogue(Hero):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.img = HERO_ROGUE
        self.hitpoints = 175
        self.atk = 10
        self.defense = 13
        self.sp_atk = 2
        self.sp_defense = 14
        self.inventory = {'health potion': 1, 'magical gem': 0, 'sharpening stone': 1, 'potion of weakness': 1}

class Wizard(Hero):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.img = HERO_WIZARD
        self.hitpoints = 150
        self.atk = 2
        self.defense = 11
        self.sp_atk = 10
        self.sp_defense = 17
        self.inventory = {'health potion': 1, 'magical gem': 2, 'sharpening stone': 0, 'potion of weakness': 0}

# NPC class to future implementation of non-active characters

class NPC(Hero):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.img = NARRATOR
        self.hitpoints = 200
        self.atk = 7
        self.defense = 7
        self.sp_atk = 1
        self.sp_defense = 3
        self.inventory = {'health potion': 1, 'magical gem': 0, 'sharpening stone': 2, 'potion of weakness': 0}

# Subclass for fun :)

class Minh(Hero):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.img = MINH
        self.hitpoints = 200
        self.atk = 7
        self.defense = 7
        self.sp_atk = 1
        self.sp_defense = 3
        self.inventory = {'health potion': 1, 'magical gem': 0, 'sharpening stone': 2, 'potion of weakness': 0}

# Mob Class - uses random module to generate different monsters for replayability

class Mob:
    def __init__(self, name, x, y):
        self.suffix = random.choice(("the Brute", "the Cunning", "the Archaic"))
        self.name = f"{name} {self.suffix}"
        self.x = x
        self.y = y
        if self.suffix == "the Brute":
            self.img = MOB_WARRIOR
            self.hitpoints = 50
            self.atk = 11
            self.defense = 11
            self.sp_atk = 6
            self.sp_defense = 6
        if self.suffix == "the Cunning":
            self.img = MOB_ROGUE
            self.hitpoints = 40
            self.atk = 13
            self.defense = 8
            self.sp_atk = 8
            self.sp_defense = 10
        if self.suffix == "the Archaic":
            self.img = MOB_WIZARD
            self.hitpoints = 40
            self.atk = 7
            self.defense = 7
            self.sp_atk = 14
            self.sp_defense = 14

    def __repr__(self):
        return self.name

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def speech(self, text):
        speech = Dialog(text, self.x, self.y-25)
        return speech

# Boss Class separated from Mob class to allow for future implementation of additional features during boss fights

class Boss:
    def __init__(self, name, x, y):
        self.img = BOSS
        self.name = name
        self.hitpoints = 80
        self.atk = 12
        self.defense = 12
        self.sp_atk = 12
        self.sp_defense = 12
        self.x = x
        self.y = y

    def __repr__(self):
        return self.name
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def speech(self, text):
        speech = Dialog(text, self.x, self.y-25)
        return speech