# An interactive RPG adventure made in Pygame by Minh Tran.

import roles
import os
import random
import pygame

# Initializing Fonts/Music modules
pygame.font.init()
pygame.mixer.init()

# Outlining the Pygame Display Window

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rylen's Descent - minhtran.app")

# Defining and Loading Sound Files provided by Zapsplat.com
cave_entry_sound = pygame.mixer.Sound(os.path.join("assets", "cave_entry_sound.mp3"))
crystal_sound = pygame.mixer.Sound(os.path.join("assets", "crystal_sound.mp3"))
dark_sound = pygame.mixer.Sound(os.path.join("assets", "dark.mp3"))
first_lava_sound = pygame.mixer.Sound(os.path.join("assets", "first_lava.mp3"))
lava_bridge_sound = pygame.mixer.Sound(os.path.join("assets", "lava_bridge.mp3"))
take_left_sound = pygame.mixer.Sound(os.path.join("assets", "take_left.mp3"))
taking_dmg_sound = pygame.mixer.Sound(os.path.join("assets", "taking_dmg.mp3"))
tunnels_sound = pygame.mixer.Sound(os.path.join("assets", "tunnels.mp3"))
selection_sound = pygame.mixer.Sound(os.path.join("assets", "selection_sound.mp3"))
player_death_sound = pygame.mixer.Sound(os.path.join("assets", "player_death.mp3"))
player_attack_sound = pygame.mixer.Sound(os.path.join("assets", "player_attack.mp3"))
player_spell_sound = pygame.mixer.Sound(os.path.join("assets", "player_spell.mp3"))
enemy_miss_sound = pygame.mixer.Sound(os.path.join("assets", "enemy_miss.mp3"))
enemy_casting_sound = pygame.mixer.Sound(os.path.join("assets", "enemy_casting.mp3"))
enemy_attack_sound = pygame.mixer.Sound(os.path.join("assets", "enemy_attack.mp3"))
arrow_sound = pygame.mixer.Sound(os.path.join("assets", "arrow_sound.mp3"))
earthquake_sound = pygame.mixer.Sound(os.path.join("assets", "earthquake.mp3"))
crystal_pickup_sound = pygame.mixer.Sound(os.path.join("assets", "crystal.mp3"))
rylen_growl_sound = pygame.mixer.Sound(os.path.join("assets", "rylen_growl.mp3"))

# Background Image to Start

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "startingforest.png")), (WIDTH, HEIGHT))

# Initializing flow variables

run = True

def main():
    global BG
    global run
    FPS = 10
    in_combat = False

    # This will determine what dynamic elements will be on screen. This should be a list of objects

    active_surfaces = []
    menu_font = pygame.font.SysFont("arial", 20)
    dialog_font = pygame.font.SysFont("arial", 15)
    clock = pygame.time.Clock()

    # Defining Drawing Surfaces ontop of Display Surface, including Texts and other Art Assets

    def redraw_window():
        WIN.blit(BG, (0,0))

        #Add Assets to Draw on surface here

        if "HERO" in locals():
            player_name_label = menu_font.render(f"Hero: {player_name}", 1, (255, 255, 255))
            WIN.blit(player_name_label, (10,10))

            player_hitpoints_label = menu_font.render(f"Hitpoints: {HERO.hitpoints}", 1, (255, 255, 255))
            WIN.blit(player_hitpoints_label, (10, 10+player_hitpoints_label.get_height()+5))

            player_atk_label = menu_font.render(f"Attack Power: {HERO.atk}", 1, (255, 255, 255))
            WIN.blit(player_atk_label, (10, 10+player_hitpoints_label.get_height()*2+5))

            player_defense_label = menu_font.render(f"Defense: {HERO.defense}", 1, (255, 255, 255))
            WIN.blit(player_defense_label, (10, 10+player_hitpoints_label.get_height()*3+5))

            player_sp_atk_label = menu_font.render(f"Spell Power: {HERO.sp_atk}", 1, (255, 255, 255))
            WIN.blit(player_sp_atk_label, (10, 10+player_hitpoints_label.get_height()*4+5))

            player_sp_defense_label = menu_font.render(f"Spell Defense: {HERO.sp_defense}", 1, (255, 255, 255))
            WIN.blit(player_sp_defense_label, (10, 10+player_hitpoints_label.get_height()*5+5))
        
        # Adding Conditional to only display when in combat

        if "HERO" in locals() and in_combat == True:
            health_potion_label = dialog_font.render(f"Health Potion: {HERO.inventory['health potion']}", 1, (255, 255, 255))
            WIN.blit(health_potion_label, (10, HEIGHT/2 - health_potion_label.get_height()*3 - 100))
            
            potion_of_weakness_label = dialog_font.render(f"Potion of Weakness: {HERO.inventory['potion of weakness']}", 1, (255,255,255))
            WIN.blit(potion_of_weakness_label, (10, HEIGHT/2 - health_potion_label.get_height()*2 - 100))

            magical_gem_label = dialog_font.render(f"Magical Gem: {HERO.inventory['magical gem']}", 1, (255,255,255))
            WIN.blit(magical_gem_label, (10, HEIGHT/2 - health_potion_label.get_height() - 100))

            sharpening_stone_label = dialog_font.render(f"Sharpening Stone: {HERO.inventory['sharpening stone']}", 1, (255,255,255))
            WIN.blit(sharpening_stone_label, (10, HEIGHT/2 - 100))
      
        # Handling Enemy Stats Display using in_combat variable

        if "active_enemy" in locals() and in_combat == True:
            enemy_name_label = menu_font.render(f"Enemy Name: {active_enemy.name}", 1, (255, 255, 255))
            WIN.blit(enemy_name_label, (WIDTH - enemy_name_label.get_width() - 10,10))
            enemy_hitpoints_label = menu_font.render(f"Hitpoints: {active_enemy.hitpoints}", 1, (255, 255, 255))
            WIN.blit(enemy_hitpoints_label, (WIDTH - enemy_name_label.get_width() - 10, 10+enemy_hitpoints_label.get_height()+5))

            enemy_atk_label = menu_font.render(f"Attack Power: {active_enemy.atk}", 1, (255, 255, 255))
            WIN.blit(enemy_atk_label, (WIDTH - enemy_name_label.get_width() - 10, 10+enemy_hitpoints_label.get_height()*2+5))

            enemy_defense_label = menu_font.render(f"Defense: {active_enemy.defense}", 1, (255, 255, 255))
            WIN.blit(enemy_defense_label, (WIDTH - enemy_name_label.get_width() - 10, 10+enemy_hitpoints_label.get_height()*3+5))

            enemy_sp_atk_label = menu_font.render(f"Spell Power: {active_enemy.sp_atk}", 1, (255, 255, 255))
            WIN.blit(enemy_sp_atk_label, (WIDTH - enemy_name_label.get_width() - 10, 10+enemy_hitpoints_label.get_height()*4+5))

            enemy_sp_defense_label = menu_font.render(f"Spell Defense: {active_enemy.sp_defense}", 1, (255, 255, 255))
            WIN.blit(enemy_sp_defense_label, (WIDTH - enemy_name_label.get_width() - 10, 10+enemy_hitpoints_label.get_height()*5+5))
       
        # Drawing the Dynamic surfaces from the Active Surfaces list

        for surface in active_surfaces:
            surface.draw(WIN)

        # Final Refresh of Display
        pygame.display.update()
    
    # Creating Add Dialog function based on who's speaking

    def add_dialog(speaker, text):
        dialog = speaker.speech(text)
        active_surfaces.append(dialog)
        clock.tick(FPS)
        redraw_window()
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                        active_surfaces.remove(dialog)
                        return
    
    # Creating a Multi-Line function to draw multiple lines of text since Pygame doesn't handle that built-in
    
    def multiline_dialog(text1, text2, text3=None, text4=None):
        dialog1 = roles.Storylines(text1, WIDTH/2, HEIGHT/2)
        active_surfaces.append(dialog1)
        dialog2 = roles.Storylines(text2, dialog1.x, dialog1.y + dialog1.text_label.get_height()*2+2)
        active_surfaces.append(dialog2)
        if text3 != None:
            dialog3 = roles.Storylines(text3, dialog1.x, dialog1.y + dialog1.text_label.get_height()*4+2)
            active_surfaces.append(dialog3)
        if text4 != None:
            dialog4 = roles.Storylines(text4, dialog1.x ,dialog1.y + dialog1.text_label.get_height()*6+2)
            active_surfaces.append(dialog4)
        while True:
            clock.tick(FPS)
            redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        active_surfaces.remove(dialog1)
                        active_surfaces.remove(dialog2)
                        if "dialog3" in locals():
                            active_surfaces.remove(dialog3)
                        if "dialog4" in locals():
                            active_surfaces.remove(dialog4)
                        return None

    # Menu dialog function to handle user input/selection

    def menu_dialog(text1, text2, text3=None, text4=None):
        dialog1 = roles.Dialog(text1, 225, 300)
        active_surfaces.append(dialog1)
        dialog2 = roles.Dialog(text2, dialog1.x, dialog1.y + dialog1.text_label.get_height()*2)
        active_surfaces.append(dialog2)
        if text3 != None:
            dialog3 = roles.Dialog(text3, dialog1.x, dialog1.y + dialog1.text_label.get_height()*4)
            active_surfaces.append(dialog3)
        if text4 != None:
            dialog4 = roles.Dialog(text4, dialog1.x ,dialog1.y + dialog1.text_label.get_height()*6)
            active_surfaces.append(dialog4)
        while True:
            clock.tick(FPS)
            redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        active_surfaces.remove(dialog1)
                        active_surfaces.remove(dialog2)
                        if "dialog3" in locals():
                            active_surfaces.remove(dialog3)
                        if "dialog4" in locals():
                            active_surfaces.remove(dialog4)
                        return 1
                    elif event.key == pygame.K_2:  
                        active_surfaces.remove(dialog1)
                        active_surfaces.remove(dialog2)
                        if "dialog3" in locals():
                            active_surfaces.remove(dialog3)
                        if "dialog4" in locals():
                            active_surfaces.remove(dialog4)
                        return 2
                    elif event.key == pygame.K_3:
                        if "dialog3" in locals():  
                            active_surfaces.remove(dialog1)
                            active_surfaces.remove(dialog2)
                            active_surfaces.remove(dialog3)
                            if "dialog4" in locals():
                                active_surfaces.remove(dialog4)
                            return 3
                    elif event.key == pygame.K_4:
                        if "dialog4" in locals():
                            active_surfaces.remove(dialog1)
                            active_surfaces.remove(dialog2)
                            active_surfaces.remove(dialog3)
                            active_surfaces.remove(dialog4)
                            return 4

    # Input Box function to allow for user input of strings

    def add_inputbox(text=""):
        input_dialog = roles.Dialog(text, 200, HEIGHT - 150)
        active_surfaces.append(input_dialog)
        while True:
            input_dialog.text = text
            input_dialog.text_label = dialog_font.render(f"{text}", 1, (255, 255, 255))
            input_dialog.rect = input_dialog.text_label.get_rect(topleft=(input_dialog.x, input_dialog.y))
            input_dialog.bg_rect = input_dialog.rect.copy()
            input_dialog.bg_rect.inflate_ip(10, 10)
            input_dialog.frame_rect = input_dialog.bg_rect.copy()
            input_dialog.frame_rect.inflate_ip(4, 4)
            clock.tick(FPS)
            redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(text) > 0:
                            active_surfaces.remove(input_dialog)
                            return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

    # Combat function to handle combat arounds

    def start_combat(player, enemy):
        nonlocal in_combat
        in_combat = True
        round = 0
        start_sound = pygame.mixer.Sound(os.path.join("assets", "combat_start.mp3"))
        end_sound = pygame.mixer.Sound(os.path.join("assets", "combat_Complete.mp3"))

        #Player Attack Phase

        start_sound.play()
        multiline_dialog(f"========= COMBAT START =========",f"{player_name} engages the enemy: {enemy.name}!")
        while player.hitpoints > 0 and enemy.hitpoints > 0:
            round += 1
            multiline_dialog(f"========= Round: {round} =========", "You prepare for your attack! What will you do?")
            while True:
                result = menu_dialog("1. Attack the enemy with your weapon.", "2. Channel mystical energies to assault the enemy.", "3. Use an item.")
                if result == 1:
                    selection_sound.play()
                    bonus = random.randint(0, 10) 
                    roll = player.atk + bonus
                    if roll > enemy.defense:
                        enemy.hitpoints -= roll

                        # Adding Flavor texts to display critical hits and dialogue based on rolls

                        if bonus >= 7:
                            multiline_dialog("****ATTACK CRITICAL****", "A surge of adrenaline fills your body!")
                        elif bonus < 7 and bonus > 3:
                            multiline_dialog("You dash forward and slash down at your enemy.", "A solid strike!")
                        else:
                            multiline_dialog("You lunge forward to attack.", "A glancing blow!")
                        player_attack_sound.play()
                        multiline_dialog(f"Your attack roll of {roll} is GREATER than the enemy's defenses ({enemy.defense}).", f"Your attack on {enemy.name} is successful. You inflict {roll} damage!")
                    elif roll <= enemy.defense:
                        if bonus >= 5:
                            multiline_dialog("You swing your sword wildly at the enemy.", f"{enemy.name} parries all your attacks.")
                        else:
                            multiline_dialog("You step forward to launch your attack, but trip and fall.", "How embarassing!")
                        multiline_dialog(f"Your attack roll of {roll} is LOWER than the enemy's defenses ({enemy.defense}).", f"Your attack on {enemy.name} misses!")
                    break
                elif result == 2:
                    selection_sound.play()
                    bonus = random.randint(0, 10)
                    roll =  player.sp_atk + bonus
                    if roll > enemy.sp_defense:
                        if bonus >= 7:
                            multiline_dialog("****SPELL CRITICAL****", "The sky darkens as the winds of magic empower your spell!")
                        elif bonus < 7 and bonus > 3:
                            multiline_dialog("Your eyes flash as you channel energy through your hands.", "You unleash a fireball towards the enemy.")
                        else:
                            multiline_dialog("You quickly mutter a simple spell under your breath.", "Streams of ice flow from your hands.")
                        player_spell_sound.play()
                        multiline_dialog(f"Your spellcast roll of {roll} is GREATER than the enemy's magical defenses ({enemy.sp_defense}).", f"Your spell hits {enemy.name} for {roll} damage.")
                        enemy.hitpoints -= roll
                    elif roll <= enemy.sp_defense:
                        if bonus >= 5:
                            multiline_dialog("As you coalesce energy around your hands, the wind howls slightly.", "Your hands begin to falter as you lose control of the energy.")
                        else:
                            multiline_dialog("As you finish channeling your spell, you trip on your long robe.", "Your hands flail wildly as you fall.")
                        multiline_dialog(f"Your spellcast roll of {roll} is LOWER than the enemy's magical defenses ({enemy.sp_defense}).", f"Your spell was resisted!")
                    break
                
                # Inventory Handling
                
                elif result == 3:
                    selection_sound.play()
                    while True:
                        item_used = False
                        multiline_dialog("Which item do you want to use?", "Choose an option.")
                        result = menu_dialog("1. Health Potion (restores 20 hitpoints)", "2. Potion of Weakness (-2 to enemy defenses)", "3. Magical Gem (+5 spell power)", "4. Sharpening Stone (+5 attack power)")
                        if result == 1:
                            selection_sound.play()
                            if player.inventory['health potion'] > 0:
                                player.hitpoints += 20
                                player.inventory['health potion'] -= 1
                                multiline_dialog("Health Potion used!", "You drink the potion and restore 20 hitpoints!")
                                item_used = True
                                break
                            else:
                                selection_sound.play()
                                multiline_dialog("You do not have any health potions left.", "Please select another option.")
                                break
                        elif result == 2:
                            selection_sound.play()
                            if player.inventory['potion of weakness'] > 0:
                                enemy.defense -= 2
                                enemy.sp_defense -= 2
                                player.inventory['potion of weakness'] -= 1
                                multiline_dialog("Potion of Weakness used!", "You lob the potion on the enemy. It splashes and strips away {enemy}\'s defenses!")
                                item_used = True
                                break
                            else:
                                selection_sound.play()
                                multiline_dialog("You do not have any Potions of Weakness left.", "Please select another option.")
                                break
                        elif result == 3:
                            selection_sound.play()
                            if player.inventory['magical gem'] > 0:
                                player.sp_atk += 5
                                player.inventory['magical gem'] -= 1
                                multiline_dialog("Magical Gem used!", "The magical gem glows as it empowers your magical reserves!")
                                item_used = True
                                break
                            else:
                                selection_sound.play()
                                multiline_dialog("You do not have any Magical Gems left.", "Please select another option.")    
                                break
                        elif result == 4:
                            selection_sound.play()
                            if player.inventory['sharpening stone'] > 0:
                                player.atk += 5
                                player.inventory['sharpening stone'] -= 1
                                multiline_dialog("Sharpening Stone used!", "You sharpen your blade with the stone. It\'s edge is razor sharp.")
                                item_used = True
                                break
                            else:
                                selection_sound.play()
                                multiline_dialog("You do not have any Sharpening Stones left.", "Please select another option.")
                                break
                    if item_used == True:
                        break            
                    else:
                        continue

            # Checking if Enemy is dead
            
            if enemy.hitpoints <= 0:
                end_sound.play()
                multiline_dialog(f"***** COMBAT ENDED AFTER {round} ROUNDS ****", f"{enemy.name} has been defeated!")
                in_combat = False
                return "alive"
            
            ### Enemy Attack Phase
            
            multiline_dialog(f"{enemy.name} prepares to attack!", "You ready your defenses.")
            mob_attack_choice = random.randint(1, 3)
            if mob_attack_choice == 1 or mob_attack_choice == 2:
                bonus = random.randint(0, 10) 
                roll = enemy.atk + bonus                             
                if roll > player.defense:
                    player.hitpoints -= roll
                    if bonus >= 7:
                        multiline_dialog("****ATTACK CRITICAL****", "The enemy bursts forward with lightning speed.")
                    elif bonus < 7 and bonus > 3:
                        multiline_dialog("The enemy swipes at you.", "You attempt to dodge, but fail!")
                    else:
                        multiline_dialog("The enemy lashes out with its claws.", "You jump back, but its claws graze your arm.")
                    enemy_attack_sound.play()    
                    multiline_dialog(f"Enemy attack roll of {roll} is GREATER than your defenses ({player.defense}).", f"It's attack on you lands. You take {roll} damage!")
                elif roll <= player.defense:
                    enemy_miss_sound.play()
                    if bonus >= 5:
                        multiline_dialog("The enemy flys forward with its fangs bared.", f"You deftly step left.")
                    else:
                        multiline_dialog("The enemy leaps forward to strike, but trips the landing.", "What an idiot!")
                    multiline_dialog(f"Enemy attack roll of {roll} is LOWER than your defenses ({player.defense}).", f"You dodge the attack.")                          
            elif mob_attack_choice == 3:
                bonus = random.randint(0, 10)
                roll =  enemy.sp_atk + bonus
                if roll > player.sp_defense:
                    if bonus >= 7:
                        multiline_dialog("****SPELL CRITICAL****", "Swirls of chaotic energy surge forward from the creature!")
                    elif bonus < 7 and bonus > 3:
                        multiline_dialog("The creature utters a dark incantation.", "The ground shakes as the dark energy erupts everywhere.")
                    else:
                        multiline_dialog("The creature mutters a quick spell.", "Dark rays pulse towards you.")
                    enemy_casting_sound.play()
                    multiline_dialog(f"The enemy spellcast roll of {roll} is GREATER than your magical defenses ({player.sp_defense}).", f"The spell hits you for {roll} damage!")
                    player.hitpoints -= roll
                elif roll <= player.sp_defense:
                    if bonus >= 5:
                        multiline_dialog("The creature conjures a ghastly spectre towards you.", "Fortunately, you ain't afraid of no ghosts.")
                    else:
                        multiline_dialog("The creature begins conjuring a spell, but mispronounces some of the key words.", "The spell fizzles out lazily.")
                    enemy_miss_sound.play()
                    multiline_dialog(f"The enemy spellcast roll of {roll} is LOWER than your magical defenses ({player.sp_defense}).", f"You deflect the spell with ease.")
            # Checking if Player is Dead

            if player.hitpoints <= 0:
                player_death_sound.play()
                multiline_dialog("You crumble to the ground as your lifeforce leaves your body.", "You have been slain.")
                in_combat = False
                return "dead"

# Function to check if player is dead from non-combat related damage

    def check_if_player_dead(combat_result):
        if combat_result == "dead":
            death_sound = pygame.mixer.Sound(os.path.join("assets", "player_death.mp3"))
            death_sound.play()
            multiline_dialog("You have been slain.", "Rylen claims another soul.", "Please try again.")
            return False
        else:
            return True

# Function to change background music as the story progresses

    def change_bg_music(file_name):
        pygame.mixer.music.load(os.path.join("assets", file_name))
        pygame.mixer.music.set_volume(.2)
        pygame.mixer.music.play(-1)

# Main Loop to control Storyline and Flow

    while run:
        global BG
        global BGM
        redraw_window()

# Story Starts here
        change_bg_music("starting_music.mp3")
        narrator = roles.NPC("Narrator", 50, HEIGHT - 150)
        active_surfaces.append(narrator)
        add_dialog(narrator, "Welcome to Rylen's Descent!")
        add_dialog(narrator, "Enter at your own risk and proceed with caution, as this is your last and only warning...")
        add_dialog(narrator, "What is your name adventurer?")
        player_name = add_inputbox()
        add_dialog(narrator, f"I remember you {player_name}! I know what you did last summer!")
        add_dialog(narrator, "Err - wrong story. What do you do for a living?")
        
        # Hero Creation

        result = menu_dialog("1. [Warrior] Me hit big things with heavy rock - me SMASH!!!", "2. [Rogue] I'm a member of the Theive's guild.", "3. [Wizard] I study the arcane arts. ")
        if result == 1:
            selection_sound.play()
            HERO = roles.Warrior(player_name, 50, HEIGHT - 165)
            add_dialog(narrator, "I knew I recognized you at my last CrossFit session! Welcome and good luck!")
            active_surfaces.append(HERO)
            redraw_window()
        elif result == 2:
            selection_sound.play()
            HERO = roles.Rogue(player_name, 50, HEIGHT - 165)
            add_dialog(narrator, "Oh dear! I'll have to keep a close watch on you. Welcome and good luck!")
            active_surfaces.append(HERO)
            redraw_window()
        elif result == 3:
            selection_sound.play()
            HERO = roles.Wizard(player_name, 50, HEIGHT - 165)
            add_dialog(narrator, "A fellow scholar! Welcome and good luck!")
            active_surfaces.append(HERO)
            redraw_window()
        active_surfaces.remove(narrator)
        redraw_window()
        multiline_dialog("You start your journey in an open clearing. In the distance, a cave stands ominously before you", "Without warning, something jumps out from the trees!")
        active_enemy = roles.Mob("Scrix", WIDTH - 250, HEIGHT - 200)
        active_surfaces.append(active_enemy)
        add_dialog(active_enemy, "RAWRRRRR! Time to die!!")
        combat_result = start_combat(HERO, active_enemy)
        run = check_if_player_dead(combat_result)
        if run == False:
            break
        active_surfaces.remove(active_enemy)
        multiline_dialog("As the dust from the battle settles, you collect your things and move forward.", "You reach the entrance of the dark cave. Ominous signs are staked all around.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cavemouth.png")), (WIDTH, HEIGHT))
        change_bg_music("cave_entry.mp3")
        cave_entry_sound.play()
        multiline_dialog("TURN BACK - DO NOT ENTER - IT'S NOT WORTH IT - HIRE MINH NOW", "\"Strange\", you think to yourself. Reluctantly, you press forward.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "darkcave.png")), (WIDTH, HEIGHT))
        multiline_dialog("The mine floor becomes more jagged and uneven as you dive deeper into the tunnel.", "You trip and fall, cutting your hand open on a jagged rock. Blood oozes out of the open wound.")
        
        # Using Random module to determine outcomes - also giving player option to consume inventory items to during story actions
        
        result = menu_dialog("1. Use a health potion to fully heal and close the wound.", "2. Attempt to find herbs in the darkness to create a salve for the wound.","3. Ignore the pain and continue down the path.")
        if result == 1:
            selection_sound.play()
            if HERO.inventory['health potion'] <= 0:
                multiline_dialog("You rumble around your bag, but do not find any health potions.", "You decide to ignore the pain. (Your status changes to \"Weakened\")")
                HERO.status = "weakened"
            else:
                multiline_dialog("You take out the small vial of restorative liquids and pour it over the open wound.", "The pain subsides as thhe skin regrows and completely closes.")
            HERO.inventory['health potion'] -= 1
        elif result == 2:
            selection_sound.play()
            wound_roll = random.randint(1,3)
            if wound_roll == 1 or wound_roll == 2:
                taking_dmg_sound.play()
                multiline_dialog("You attempt fails and you end up opening the wound further.", "You take 10 hitpoint damage. (Your status changes to \"Weakened\")")
                HERO.hitpoints -= 10
                HERO.status = "weakened"
                run = check_if_player_dead(combat_result)
                if run == False:
                    break
            if wound_roll == 3:
                multiline_dialog("Miraculously, you forage enough herbs to make a salve.", "You crush them into a paste and apply it to the wound. The pain subsides.")
        elif result == 3:
            selection_sound.play()
            taking_dmg_sound.play()
            multiline_dialog("You decide to ignore the pain.", "You feel weaker as you move. (Your status changes to \"Weakened\")")
            HERO.status = "weakened"
        multiline_dialog("You continue on. In the distance a small torch outlines two paths.", "You follow the light until you arrive at the fork.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_twopath.png")), (WIDTH, HEIGHT))
        tunnels_sound.play()
        multiline_dialog("Something shiny glitters in the distance on the left path.", "The path on the right is littered with bones.")
        result = menu_dialog("1. Take the path on the left.", "2. Take the path on the right.")
        if result == 1:
            selection_sound.play()
            BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_left.png")), (WIDTH, HEIGHT))
            take_left_sound.play()
            multiline_dialog("You follow the path down towards a dead end.", "In front of you lay a white bag on a stone pedastal.")
            arrow_sound.play()
            multiline_dialog("As you pick up the white satchel, you hear a faint click.", "An arrow whistles through the air, striking you in the knee.")
            taking_dmg_sound.play()
            multiline_dialog("You take 20 damage from the arrow.", "You gain a Health Potion and a Potion of Weakness from the satchel.")
            HERO.inventory["health potion"] += 1
            HERO.inventory["potion of weakness"] += 1
            multiline_dialog("You can't you just took an arrow to the knee.", "Flustered, you go back the way you came and take the path on the right.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_right.png")), (WIDTH, HEIGHT))
        multiline_dialog("Tip-toeing over the string of bones, you continue down the mine tunnels.", "There's something in the distance...")
        active_enemy = roles.Mob("Ludgar", WIDTH - 250, HEIGHT - 200)
        multiline_dialog("Your eyes strain in the darkness...", "The dark mass turns around and lunges towards you!")
        active_surfaces.append(active_enemy)
        add_dialog(active_enemy, "Who dares disturb my slumber?")
        combat_result = start_combat(HERO, active_enemy)
        run = check_if_player_dead(combat_result)
        if run == False:
            break
        active_surfaces.remove(active_enemy)
        multiline_dialog("As the creatures body slumps to the ground, the ground begins to shake.", "You hastily stride past the lifeless corpse and into a large cavern.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_lava.png")), (WIDTH, HEIGHT))
        change_bg_music("cave_lava.mp3")
        first_lava_sound.play()
        multiline_dialog("Before you stretches a large underground chasm. Lava flows through a deep channel in the middle.", "There doesn't appear to be a way across the lava.")
        multiline_dialog("Searching for a way forward, you find a ledge following the trench of lava.", "You decide to place your back against the wall and shimmy along.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_ledge.png")), (WIDTH, HEIGHT))
        multiline_dialog("You slink along the cave edge, following the lava flow below.", "You place your back against the wall as you try to keep your balance.")
        multiline_dialog("You notice a few bats perched overhead. As you slide through, one of them dives at you!", "Startled, you lose your balance and slip off the cliff edge, towards the lava below.")
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_hang.png")), (WIDTH, HEIGHT))
        multiline_dialog("Grabbing wildly, you manage to get hold of some cliff vegetation and hold on.", "Hanging precariously over the edge, you realize you need to make a decision fast!")
        result = menu_dialog("1. Attempt to kick off the cliff wall and land on the ledge below.", "2. Take your chances and let go.")
        if result == 1:
            selection_sound.play()
            result = random.randint(1, 2)

            # Using player status of weakened from previous choices to determine outcome

            if result == 1 and HERO.status != "normal":
                multiline_dialog("You push off the cliff wall with all your strength and propel yourself forward.", "You land safely on the ledge below.")
            elif result == 2:
                multiline_dialog("You push off the cliff wall with all your strength.", "Unfortunately, you are still weakened from the open wound on your hand.")
                taking_dmg_sound.play()
                multiline_dialog("Blood gushes wildly from the wound as you fall to the ledge below.", "You take 20 hitpoints of damage from the fall.")
                HERO.hitpoints -= 20
                run = check_if_player_dead(combat_result)
                if run == False:
                    break
        elif result == 2:
            selection_sound.play()
            multiline_dialog("You close your eyes and let go.", "You slide along the cliff wall and land on the ledge safely below.")
        multiline_dialog("You brush yourself off and continue along the ledge, following the lava below.", "In the distance, you see a way across the chasm.")
        multiline_dialog("The ground shakes again. Something is stirring in the cave.", "You continue on your way forward.")       
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_bridge.png")), (WIDTH, HEIGHT))
        lava_bridge_sound.play()
        multiline_dialog("In front of you is a stone bridge spanning the length of the lava.", "The ground shakes and rumbles from the lava eruptions, and perhaps something else?")
        multiline_dialog("You carefully place one foot in front of the other, hoping to avoid a very painful, and hot, death below.", "You cross slowly, just a few more steps to the other side.")
        multiline_dialog("Before you can make it across, something grabs your feet.", "A creature crawls out from underneath the stone bridge and strikes!")
        active_enemy = roles.Mob("Thrax", WIDTH - 250, HEIGHT - 200)
        active_surfaces.append(active_enemy)
        add_dialog(active_enemy, "ME LOVE ANKLES! YUMMY!!!!")
        combat_result = start_combat(HERO, active_enemy)
        run = check_if_player_dead(combat_result)
        if run == False:
            break
        multiline_dialog("With the battle subsiding, you pick up your weapon.", "As you go to deal the finishing blow on the creature, it whispers one last time.",)
        add_dialog(active_enemy, "Your...")
        add_dialog(active_enemy, "ankles...")
        add_dialog(active_enemy, "are...")
        add_dialog(active_enemy, "ugly...")
        earthquake_sound.play()
        multiline_dialog("The creature lets out its last dying breath.", "It falls into the lava below.")
        active_surfaces.remove(active_enemy)
        multiline_dialog("The ground begins to shake and rumble again...", "...")
        multiline_dialog("This time, it doesn't stop...", "...")
        multiline_dialog("Rocks fall from the ceiling...", "Lava erupts in vast plumes all around you...")
        multiline_dialog("The bridge crumbles, as it gives way to the rising lava below.", "You lose your footing...")
        multiline_dialog("You turn to run, but you don't notice the large boulders crashing towards you.", "The barrage of rocks slam into your face...", "Everything goes dark...")
        active_surfaces.remove(HERO)
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_sleep.png")), (WIDTH, HEIGHT))
        dark_sound.play()
        minh = roles.Minh("Minh", WIDTH - 300, HEIGHT - 200)
        add_dialog(minh, "...")
        add_dialog(minh, "...")
        add_dialog(minh, "Hey!")
        add_dialog(minh, "Excuse me...")
        add_dialog(minh, "HEY! WAKE UP!")
        multiline_dialog("Everything is dark, and your head feels groggy.", "You faintly hear the sound of what appears to be a very reliable, and skilled software engineer.")
        active_surfaces.append(minh)
        add_dialog(minh, "WE'RE NOT DONE WITH THE CODE DEMO")
        active_surfaces.remove(minh)
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_before_boss.png")), (WIDTH, HEIGHT))
        crystal_sound.play()
        active_surfaces.append(HERO)
        multiline_dialog("Weird - whoever that was he sure did help us.", "You should probably hire him - er I mean, where was I...(ahem)...")
        multiline_dialog("Slowly, you brush the debris off and get to your feet.", "You're not sure how long you were out, but the shaking has stopped.", "Looks like you were lucky and your hard head broke your fall.")
        multiline_dialog("A flourescent, blue crystal lay before you, floating atop a pillar of lava.", "The crystal calls out to you...")
        crystal_pickup_sound.play()
        multiline_dialog("You grab the crystal.", "As you gaze into it's crystalline depths, visions of vast treasure troves fill your head.", "Entranced by the visions, you do not notice the dark shadow looming above.")
        
        # Boss fight and story climax
        
        active_enemy = roles.Boss("Rylen the Darkener", WIDTH - 320, HEIGHT - 330)
        active_surfaces.append(active_enemy)
        rylen_growl_sound.play()
        add_dialog(active_enemy, "Tiny mouse...")
        add_dialog(active_enemy, "Return my crystal...")
        add_dialog(active_enemy, "And you may yet live...")
        
        # Using variable has_crystal to control story flow and outcomes
        
        result = menu_dialog("1. Never! What do you need with the crystal? I will be rich beyond compare!", "2. What's in it for me?", "3. Here, take it. (give the crystal back)", "4. (make a run for the opening behind the dragon)")
        if result == 1:
            selection_sound.play()
            has_crystal = True
            add_dialog(active_enemy, "Insolence! Prepare to die!")
            combat_result = start_combat(HERO, active_enemy)
            run = check_if_player_dead(combat_result)
            if run == False:
                break
            multiline_dialog("You strike the dragon down with one last blow.", "The dragon hisses and roars in anger.")
            add_dialog(active_enemy, "This is impossible!")
            add_dialog(active_enemy, "You...")
            add_dialog(active_enemy, "will...")
            add_dialog(active_enemy, "pay...")
            multiline_dialog("The dragon lets out its last breath, and collapses into the lava.", "With the crystal in hand, you head toward the opening.")
        elif result == 2:
            selection_sound.play()
            add_dialog(active_enemy, "You may leave with your life.")
            result = menu_dialog("1. Give the crystal to Rylen.", "2. Keep the crystal.")
            if result == 1:
                selection_sound.play()
                has_crystal = False
                multiline_dialog("You give the crystal back to the dragon.", "Honoring his word, Rylen allows you to leave, empty-handed.")
            elif result == 2:
                selection_sound.play()
                has_crystal = True
                add_dialog(active_enemy, "Then you choose death.")
                combat_result = start_combat(HERO, active_enemy)
                run = check_if_player_dead(combat_result)
                if run == False:
                    break
                multiline_dialog("You strike the dragon down with one last blow.", "The dragon hisses and roars in anger.")
                add_dialog(active_enemy, "This is impossible!")
                add_dialog(active_enemy, "You...")
                add_dialog(active_enemy, "will...")
                add_dialog(active_enemy, "pay...")
                multiline_dialog("The dragon lets out its last breath, and collapses into the lava.", "With the crystal in hand, you head toward the opening.")
        elif result == 3:
            selection_sound.play()
            has_crystal = False
            multiline_dialog("You give the crystal back to the dragon.", "Honoring his word, Rylen allows you to leave, empty-handed.")
        elif result == 4:
            selection_sound.play()
            has_crystal = True
            multiline_dialog("You make a run for the opening, with the crystal in hand.", "Rylen roars with anger and leaps after you.")
            add_dialog(active_enemy, "Fool!! You will not get away!")
            multiline_dialog("Rylen slams in front of you, blocking the opening.", "You see an opening between the dragon's outstretched legs.", "What should you do?")
            result = menu_dialog("1. Attempt to run under the dragon and through his legs, into the opening.", "2. Throw the crystal towards the lava, and try to run past the dragon.")
            if result == 1:
                selection_sound.play()
                result = random.randint(1,4)
                if result == 1:
                    selection_sound.play()
                    multiline_dialog("You push off on your feet as fast as you can.", "You run towards the dragon, dodging his swinging claws and snapping jaws.","Against all odds, you slip past the dragon and into the opening behind.")
                else:
                    selection_sound.play()
                    multiline_dialog("You push off on your feet as fast as you can.", "You run towards the dragon, dodging his swinging claws and snapping jaws.","Just as you are sliding past the dragon, his tail swipes you and throws you back into the cave.")
                    add_dialog(active_enemy, "No one escapes me.")
                    combat_result = start_combat(HERO, active_enemy)
                    run = check_if_player_dead(combat_result)
                    if run == False:
                        break
                    multiline_dialog("You strike the dragon down with one last blow.", "The dragon hisses and roars in anger.")
                    add_dialog(active_enemy, "This is impossible!")
                    add_dialog(active_enemy, "You...")
                    add_dialog(active_enemy, "will...")
                    add_dialog(active_enemy, "pay...")
                    multiline_dialog("The dragon lets out its last breath, and collapses into the lava.", "With the crystal in hand, you head toward the opening.")
            elif result == 2:
                selection_sound.play()
                has_crystal = False
                multiline_dialog("You toss the crystal into the lava hoping to distract the dragon.", "As the crystal fades into the lava, an explosion ripples through the cave.")
                taking_dmg_sound.play()
                multiline_dialog("You take cover behind the massive dragon.","Both you and Rylen get caught in the explosion.", "You take 50 points of damage the explosion")
                HERO.hitpoints -= 50
                run = check_if_player_dead(combat_result)
                if run == False:
                    break
                multiline_dialog("As the smoke clears, you see the lifeless form of the dragon.", "The crystal's explosion violently severed the dragon's head.", "You walk towards the opening.")
        active_surfaces.remove(active_enemy)
        active_surfaces.remove(HERO)
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "cave_exit.png")), (WIDTH, HEIGHT))    
        change_bg_music("end_music.mp3")
        
        # Ending storyline based on has_crystal variable
        
        if has_crystal == True:
            multiline_dialog("Sunlight bathes your face as you crawl out of the opening into the light.", "The crystal pulses and hums in your hand.") 
            multiline_dialog("You smile knowing all the riches that await you.", "Perhaps you will find those treasures in a far away land...")
            multiline_dialog("...or perhaps in another exciting game from Minh Tran", "(you know, that very reliable and skilled software engineer that saved your life) :)")
            multiline_dialog("...The End...", "...or is it???...")
            multiline_dialog("Thank you guys for sticking it out to the end!", "I hope you enjoyed playing it as much as I did creating it!")
            multiline_dialog("Thanks again!", "(Push Enter to Exit)")
            run = False
        else:
            multiline_dialog("Sunlight bathes your face as you crawl out of the opening into the light.", "A strange sense of emptiness surrounds you.")
            multiline_dialog("Thankful to be alive, you smile knowing you survived Rylen's Descent.", "Still, you can't help but wonder what riches would have awaited you.")
            multiline_dialog("...or perhaps you don't have to wonder after all...","...maybe that very reliable, and skilled software engineer will make another game...", "...what was his name again? Oh yeah! Minh - the guy that saved us back there")
            multiline_dialog("...The End...", "...or is it???...")
            multiline_dialog("Thank you guys for sticking it out to the end!", "I hope you enjoyed playing it as much as I did creating it!")
            multiline_dialog("Thanks again!", "(Push Enter to Exit)")
            run = False

# Main Menu function to allow for replaying of game            

def main_menu():
    global BG
    global run
    title_font = pygame.font.SysFont("arial", 70)
    sub_title_font = pygame.font.SysFont("arial", 30)
    while True:
        if run == True:
            BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "startingforest.png")), (WIDTH, HEIGHT))
            WIN.blit(BG, (0,0))
            title_label = title_font.render("Rylen's Descent", 1, (249, 231, 231))
            WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 100))
            sub_title_label = sub_title_font.render("Push Enter to begin...", 1, (249, 231, 231))
            WIN.blit(sub_title_label, (WIDTH/2 - sub_title_label.get_width()/2, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()
        else:
            BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "startingforest.png")), (WIDTH, HEIGHT))
            WIN.blit(BG, (0,0))
            game_over_label = title_font.render("Thank's for playing!", 1, (249, 231, 231))
            WIN.blit(game_over_label, (WIDTH/2 - game_over_label.get_width()/2, 100))
            play_again_label = sub_title_font.render("Push Enter to play again...", 1, (249, 231, 231))
            WIN.blit(play_again_label, (WIDTH/2 - play_again_label.get_width()/2, 400))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = True
                        main()
            

main_menu()

### *** Things to implement in the future ***
### Animations
### Movement-based outcomes
### Implement collision between assets
### High Score functionality

