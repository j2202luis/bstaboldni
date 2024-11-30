import random
import curses
import time

# Character class to define the player and enemies
class Character:
    def __init__(self, name, health, attack, defense, level=1):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level
    
    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage, stdscr):
        damage_taken = max(damage - self.defense, 0)
        self.health -= damage_taken
        stdscr.addstr(f"{self.name} takes {damage_taken} damage. Health: {self.health}/{self.max_health}\n")
        stdscr.refresh()
        time.sleep(1)

    def attack_enemy(self, enemy, stdscr):
        damage = random.randint(self.attack - 2, self.attack + 2)
        stdscr.addstr(f"{self.name} attacks {enemy.name} for {damage} damage.\n")
        stdscr.refresh()
        time.sleep(1)
        enemy.take_damage(damage, stdscr)
        
    def heal(self, stdscr):
        heal_amount = random.randint(5, 10)
        self.health = min(self.health + heal_amount, self.max_health)
        stdscr.addstr(f"{self.name} heals for {heal_amount} points. Health: {self.health}/{self.max_health}\n")
        stdscr.refresh()
        time.sleep(1)

# Player class (inherits from Character)
class Player(Character):
    def __init__(self, name):
        super().__init__(name, health=50, attack=10, defense=3)
        self.max_health = 50
    
    def level_up(self, stdscr):
        self.level += 1
        self.attack += 3
        self.defense += 2
        self.max_health += 10
        self.health = self.max_health
        stdscr.addstr(f"{self.name} has leveled up! Now at level {self.level}.\n")
        stdscr.refresh()
        time.sleep(1)

# Enemy class (inherits from Character)
class Enemy(Character):
    def __init__(self, name, level):
        super().__init__(name, health=30 + (level * 5), attack=8 + level, defense=2 + level, level=level)
        self.max_health = self.health

    def take_damage(self, damage, stdscr):
        super().take_damage(damage, stdscr)
        if not self.is_alive():
            stdscr.addstr(f"{self.name} has been defeated!\n")
            stdscr.refresh()
            time.sleep(1)

# Game logic
def battle(player, enemy, stdscr):
    stdscr.addstr(f"A wild {enemy.name} appears!\n")
    stdscr.refresh()
    time.sleep(1)
    
    while player.is_alive() and enemy.is_alive():
        stdscr.clear()
        stdscr.addstr(f"{player.name}'s Health: {player.health}/{player.max_health}\n")
        stdscr.addstr(f"{enemy.name}'s Health: {enemy.health}/{enemy.max_health}\n")
        stdscr.addstr("\nChoose your action:\n")
        stdscr.addstr("1: Attack\n")
        stdscr.addstr("2: Heal\n")
        stdscr.refresh()
        choice = stdscr.getch()

        if choice == ord('1'):
            player.attack_enemy(enemy, stdscr)
        elif choice == ord('2'):
            player.heal(stdscr)
        else:
            stdscr.addstr("Invalid choice, try again.\n")
            stdscr.refresh()
            time.sleep(1)
            continue

        if enemy.is_alive():
            enemy.attack_enemy(player, stdscr)
        else:
            break

        if player.is_alive():
            stdscr.addstr(f"{player.name}'s Health: {player.health}/{player.max_health}\n")
        else:
            stdscr.addstr(f"{player.name} has been defeated!\n")
            break

# Main game loop
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.clear()

    stdscr.addstr("Welcome to the RPG Game!\n")
    stdscr.refresh()
    time.sleep(1)

    # Create player
    stdscr.addstr("Enter your character's name: ")
    stdscr.refresh()
    player_name = ""
    while True:
        char = stdscr.getch()
        if char == 10:  # Enter key
            break
        player_name += chr(char)
        stdscr.addstr(chr(char))
        stdscr.refresh()

    player = Player(player_name)
    
    # Game loop
    while player.is_alive():
        enemy_level = random.randint(1, player.level + 1)
        enemy = Enemy("Goblin", enemy_level)
        battle(player, enemy, stdscr)
        
        if player.is_alive():
            player.level_up(stdscr)
            stdscr.addstr("Do you want to continue adventuring? (y/n): ")
            stdscr.refresh()
            choice = stdscr.getch()
            if choice == ord('n'):
                break
        else:
            stdscr.addstr("Game over!\n")
            break

    stdscr.addstr("Thank you for playing!\n")
    stdscr.refresh()
    time.sleep(2)

if __name__ == "__main__":
    curses.wrapper(main)
