import streamlit as st
import random
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

    def take_damage(self, damage):
        damage_taken = max(damage - self.defense, 0)
        self.health -= damage_taken
        return damage_taken

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 2, self.attack + 2)
        damage_taken = enemy.take_damage(damage)
        return damage, damage_taken

    def heal(self):
        heal_amount = random.randint(5, 10)
        self.health = min(self.health + heal_amount, self.max_health)
        return heal_amount

# Player class (inherits from Character)
class Player(Character):
    def __init__(self, name):
        super().__init__(name, health=50, attack=10, defense=3)
        self.max_health = 50
    
    def level_up(self):
        self.level += 1
        self.attack += 3
        self.defense += 2
        self.max_health += 10
        self.health = self.max_health

# Enemy class (inherits from Character)
class Enemy(Character):
    def __init__(self, name, level):
        super().__init__(name, health=30 + (level * 5), attack=8 + level, defense=2 + level, level=level)
        self.max_health = self.health

# Game logic
def battle(player, enemy):
    battle_messages = []
    while player.is_alive() and enemy.is_alive():
        action = st.radio("Choose your action:", ['Attack', 'Heal'])

        if action == 'Attack':
            damage_dealt, damage_taken = player.attack_enemy(enemy)
            battle_messages.append(f"{player.name} attacks {enemy.name} for {damage_dealt} damage.")
            battle_messages.append(f"{enemy.name} takes {damage_taken} damage. Health: {enemy.health}/{enemy.max_health}")
        
        elif action == 'Heal':
            heal_amount = player.heal()
            battle_messages.append(f"{player.name} heals for {heal_amount} health. Health: {player.health}/{player.max_health}")
        
        if enemy.is_alive():
            damage_dealt, damage_taken = enemy.attack_enemy(player)
            battle_messages.append(f"{enemy.name} attacks {player.name} for {damage_dealt} damage.")
            battle_messages.append(f"{player.name} takes {damage_taken} damage. Health: {player.health}/{player.max_health}")
        
        if not enemy.is_alive():
            battle_messages.append(f"{enemy.name} has been defeated!")
            player.level_up()
            battle_messages.append(f"{player.name} levels up! Now at level {player.level}.")
            break

        if not player.is_alive():
            battle_messages.append(f"{player.name} has been defeated!")
            break

    return battle_messages

# Main game loop
def main():
    st.title("RPG Game")

    # Player setup
    player_name = st.text_input("Enter your character's name:", "Hero")
    if st.button("Start Game"):
        player = Player(player_name)
        st.session_state.player = player
        st.session_state.messages = []

    # Game loop
    if 'player' in st.session_state:
        player = st.session_state.player
        enemy_level = random.randint(1, player.level + 1)
        enemy = Enemy("Goblin", enemy_level)

        # Show messages
        for message in st.session_state.messages:
            st.text(message)

        if player.is_alive() and enemy.is_alive():
            battle_messages = battle(player, enemy)
            st.session_state.messages.extend(battle_messages)

        if player.is_alive():
            st.text(f"{player.name}'s Health: {player.health}/{player.max_health}")
            st.text(f"{enemy.name}'s Health: {enemy.health}/{enemy.max_health}")

        if player.is_alive() and not enemy.is_alive():
            st.text(f"{enemy.name} has been defeated!")
            st.text(f"{player.name}'s Health: {player.health}/{player.max_health}")

            if st.button("Continue Adventuring"):
                enemy_level = random.randint(1, player.level + 1)
                enemy = Enemy("Goblin", enemy_level)
                battle_messages = battle(player, enemy)
                st.session_state.messages.extend(battle_messages)

        elif not player.is_alive():
            st.text(f"{player.name} has been defeated! Game Over!")
            if st.button("Restart Game"):
                del st.session_state.player
                del st.session_state.messages
                st.experimental_rerun()

if __name__ == "__main__":
    main()
