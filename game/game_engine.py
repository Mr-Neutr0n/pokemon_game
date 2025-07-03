"""
Game engine for handling all game logic, battles, and world interactions
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .pokemon import Pokemon, PokemonType, Move
from .trainer import Trainer, Badge
from .save_manager import SaveManager

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.display import Display
from utils.input_handler import InputHandler
from utils.logger import game_logger

class GameEngine:
    """Main game engine that handles all game logic"""
    
    def __init__(self):
        self.display = Display()
        self.input_handler = InputHandler()
        self.save_manager = SaveManager()
        self.trainer = None
        self.current_battle = None
        self.game_running = False
        self.game_start_time = None
        
        # Game world data
        self.locations = self.initialize_locations()
        self.wild_pokemon = self.initialize_wild_pokemon()
        self.gym_leaders = self.initialize_gym_leaders()
        self.shops = self.initialize_shops()
        self.starter_pokemon = self.initialize_starter_pokemon()
    
    def start_new_game(self):
        """Start a new game"""
        self.display.clear_screen()
        self.display.show_title()
        
        # Create new trainer
        trainer_name = self.input_handler.get_trainer_name()
        self.trainer = Trainer(trainer_name)
        
        # Choose starter Pokemon
        self.display.show_message("Welcome to the world of Pokemon!")
        self.display.show_message("Choose your starter Pokemon:")
        
        starter_choice = self.input_handler.get_starter_choice()
        starter_pokemon = self.get_starter_pokemon(starter_choice)
        
        # Give nickname to starter
        nickname = self.input_handler.get_pokemon_nickname(starter_pokemon.species)
        if nickname:
            starter_pokemon.nickname = nickname
        
        self.trainer.add_pokemon(starter_pokemon)
        
        self.display.show_message(f"Congratulations! You received {starter_pokemon.nickname}!")
        self.display.show_pokemon_info(starter_pokemon)
        
        # Start the game
        self.game_running = True
        self.game_start_time = time.time()
        self.main_game_loop()
    
    def load_game(self, save_name: str):
        """Load an existing game"""
        save_data = self.save_manager.load_game(save_name)
        
        if save_data is None:
            self.display.show_error("Failed to load game!")
            return False
        
        # Create trainer from save data
        self.trainer = Trainer()
        self.trainer.load_from_save_data(save_data)
        
        self.display.show_message(f"Welcome back, {self.trainer.name}!")
        
        # Start the game
        self.game_running = True
        self.game_start_time = time.time()
        self.main_game_loop()
        
        return True
    
    def main_game_loop(self):
        """Main game loop"""
        while self.game_running:
            try:
                # Auto-save periodically
                self.save_manager.auto_save(self.trainer)
                
                # Update play time
                if self.game_start_time:
                    play_time = int((time.time() - self.game_start_time) / 60)
                    self.trainer.stats["play_time"] = self.trainer.stats.get("play_time", 0) + play_time
                    self.game_start_time = time.time()
                
                # Show current location and options
                self.display.clear_screen()
                self.show_location_info()
                
                # Get player action
                action = self.get_player_action()
                
                # Process action
                self.process_action(action)
                
            except KeyboardInterrupt:
                self.display.show_message("\nGame interrupted. Saving...")
                self.save_game()
                break
            except Exception as e:
                self.display.show_error(f"An error occurred: {e}")
                self.display.show_message("The game will continue...")
    
    def show_location_info(self):
        """Show current location information"""
        location = self.locations.get(self.trainer.current_location, {})
        
        # Safety check: if current location is invalid, reset to pallet_town
        if not location:
            self.display.show_warning(f"Invalid location detected: {self.trainer.current_location}")
            self.display.show_message("Resetting to Pallet Town...")
            self.trainer.current_location = "pallet_town"
            location = self.locations.get(self.trainer.current_location, {})
        
        self.display.show_message(f"Current Location: {location.get('name', 'Unknown')}")
        self.display.show_message(f"Description: {location.get('description', 'No description available')}")
        
        # Show available actions with consistent numbering
        actions = []
        actions.append("1. Explore (Find wild Pokemon)" if location.get('wild_pokemon') else "1. Explore (No wild Pokemon here)")
        actions.append("2. Challenge Gym" if location.get('gym') else "2. Challenge Gym (No gym here)")
        actions.append("3. Visit Shop" if location.get('shop') else "3. Visit Shop (No shop here)")
        actions.append("4. Visit Pokemon Center" if location.get('pokemon_center') else "4. Visit Pokemon Center (No center here)")
        actions.extend([
            "5. View Team",
            "6. View Bag",
            "7. View Pokedex",
            "8. View Trainer Info",
            "9. Travel",
            "10. Save Game",
            "11. Settings",
            "12. Quit Game"
        ])
        
        self.display.show_menu("What would you like to do?", actions)
    
    def get_player_action(self) -> str:
        """Get player's action choice"""
        choice = self.input_handler.get_menu_choice(12)
        
        if choice is None:
            return "invalid"
        
        action_map = {
            1: "explore",
            2: "gym",
            3: "shop",
            4: "pokemon_center",
            5: "team",
            6: "bag",
            7: "pokedex",
            8: "trainer_info",
            9: "travel",
            10: "save",
            11: "settings",
            12: "quit"
        }
        
        return action_map.get(choice, "invalid")
    
    def process_action(self, action: str):
        """Process the player's action"""
        location = self.locations.get(self.trainer.current_location, {})
        
        if action == "explore":
            if location.get('wild_pokemon'):
                self.explore_area()
            else:
                self.display.show_message("There are no wild Pokemon in this area.")
                self.input_handler.wait_for_input("Press Enter to continue...")
        elif action == "gym":
            if location.get('gym'):
                self.challenge_gym()
            else:
                self.display.show_message("There's no gym in this location.")
                self.input_handler.wait_for_input("Press Enter to continue...")
        elif action == "shop":
            if location.get('shop'):
                self.visit_shop()
            else:
                self.display.show_message("There's no shop in this location.")
                self.input_handler.wait_for_input("Press Enter to continue...")
        elif action == "pokemon_center":
            if location.get('pokemon_center'):
                self.visit_pokemon_center()
            else:
                self.display.show_message("There's no Pokemon Center in this location.")
                self.input_handler.wait_for_input("Press Enter to continue...")
        elif action == "team":
            self.view_team()
        elif action == "bag":
            self.view_bag()
        elif action == "pokedex":
            self.view_pokedex()
        elif action == "trainer_info":
            self.view_trainer_info()
        elif action == "travel":
            self.travel()
        elif action == "save":
            self.save_game()
        elif action == "settings":
            self.show_settings()
        elif action == "quit":
            self.quit_game()
        else:
            self.display.show_error("Invalid action!")
            self.input_handler.wait_for_input("Press Enter to continue...")
    
    def explore_area(self):
        """Explore the current area for wild Pokemon"""
        location = self.locations.get(self.trainer.current_location, {})
        wild_pokemon_list = location.get('wild_pokemon', [])
        
        if not wild_pokemon_list:
            self.display.show_message("There are no wild Pokemon in this area.")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        self.display.show_message("You start exploring the area...")
        self.display.animate_text("Searching for Pokemon...")
        
        # Random encounter
        if random.random() < 0.7:  # 70% chance of encounter
            wild_species = random.choice(wild_pokemon_list)
            wild_pokemon = self.create_wild_pokemon(wild_species)
            
            self.display.show_message(f"A wild {wild_pokemon.species} appeared!")
            self.start_battle(wild_pokemon, is_wild=True)
        else:
            self.display.show_message("No Pokemon found this time.")
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def start_battle(self, opponent_pokemon: Pokemon, is_wild: bool = True, trainer_name: str = None):
        """Start a battle with a Pokemon"""
        if not self.trainer.get_active_pokemon():
            self.display.show_error("You have no Pokemon that can battle!")
            return "no_pokemon"
        
        player_pokemon = self.trainer.get_active_pokemon()
        
        self.display.show_battle_scene(player_pokemon, opponent_pokemon, is_wild)
        
        battle_result = self.battle_loop(player_pokemon, opponent_pokemon, is_wild, trainer_name)
        
        if battle_result == "victory":
            self.trainer.stats["battles_won"] = self.trainer.stats.get("battles_won", 0) + 1
            
            # Gain experience
            exp_gained = self.calculate_exp_gain(player_pokemon, opponent_pokemon)
            old_level = player_pokemon.level
            player_pokemon.gain_experience(exp_gained)
            
            self.display.show_message(f"{player_pokemon.nickname} gained {exp_gained} experience!")
            
            # Check for level up
            if player_pokemon.level > old_level:
                self.display.show_level_up(player_pokemon)
            
            # Attempt to catch if wild
            if is_wild:
                self.attempt_catch(opponent_pokemon)
        elif battle_result == "defeat":
            self.display.show_message("You were defeated!")
            self.trainer.stats["battles_lost"] = self.trainer.stats.get("battles_lost", 0) + 1
        
        return battle_result
    
    def battle_loop(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon, is_wild: bool, trainer_name: str = None) -> str:
        """Main battle loop"""
        game_logger.battle_start(player_pokemon, opponent_pokemon, is_wild)
        
        battle_turn = 0
        max_turns = 100  # Prevent infinite battles
        
        while not player_pokemon.is_fainted() and not opponent_pokemon.is_fainted() and battle_turn < max_turns:
            battle_turn += 1
            game_logger.battle_loop_iteration(battle_turn, player_pokemon.current_hp, opponent_pokemon.current_hp)
            
            try:
                # Show battle scene
                self.display.show_battle_scene(player_pokemon, opponent_pokemon, is_wild)
                
                # Show battle menu
                self.display.show_battle_menu()
                
                # Get player's choice
                battle_choice = self.input_handler.get_battle_choice()
                game_logger.battle_choice(battle_choice, "battle_menu")
                
                if battle_choice is None:
                    game_logger.info("Battle choice was None, treating as Run")
                    battle_choice = 4  # Run
                
                if battle_choice == 1:  # Fight
                    game_logger.debug("Player chose FIGHT")
                    
                    # Show move selection
                    self.display.show_move_selection(player_pokemon)
                    move_choice = self.input_handler.get_move_choice(player_pokemon)
                    game_logger.move_selection(player_pokemon, move_choice)
                    
                    if move_choice and move_choice <= len(player_pokemon.moves):
                        move = player_pokemon.moves[move_choice - 1]
                        game_logger.debug(f"Selected move: {move.name}")
                        
                        # Use the move (reduce PP)
                        if not move.use_move():
                            self.display.show_message(f"{move.name} has no PP left!")
                            continue
                        
                        damage = player_pokemon.calculate_damage(move, opponent_pokemon)
                        game_logger.damage_calculation(player_pokemon, opponent_pokemon, move, damage)
                        
                        opponent_pokemon.take_damage(damage)
                        
                        self.display.show_message(f"{player_pokemon.nickname} used {move.name}!")
                        
                        if damage > 0:
                            effectiveness = self.get_effectiveness_message(move.type, opponent_pokemon.types)
                            if effectiveness:
                                self.display.show_message(f"It dealt {damage} damage! {effectiveness}")
                            else:
                                self.display.show_message(f"It dealt {damage} damage!")
                        else:
                            self.display.show_message("The attack missed!")
                    else:
                        game_logger.warning("Invalid move choice, skipping turn")
                        continue
                        
                elif battle_choice == 2:  # Items
                    game_logger.debug("Player chose ITEMS")
                    healing_items = self.trainer.inventory.get_items_by_type("healing")
                    if healing_items:
                        self.display.show_inventory(self.trainer.inventory, "healing")
                        item_choice = self.input_handler.get_item_choice(healing_items)
                        if item_choice:
                            # Use healing item
                            if self.trainer.use_item(item_choice, player_pokemon):
                                self.display.show_message(f"Used {item_choice} on {player_pokemon.nickname}!")
                            else:
                                self.display.show_message("Cannot use that item right now.")
                                continue
                        else:
                            continue
                    else:
                        self.display.show_message("No usable items!")
                        continue
                        
                elif battle_choice == 3:  # Pokemon
                    game_logger.debug("Player chose POKEMON")
                    if len(self.trainer.pokemon_team) > 1:
                        self.display.show_pokemon_team(self.trainer.pokemon_team)
                        pokemon_choice = self.input_handler.get_pokemon_choice(self.trainer.pokemon_team)
                        if pokemon_choice and pokemon_choice <= len(self.trainer.pokemon_team):
                            new_pokemon = self.trainer.pokemon_team[pokemon_choice - 1]
                            if new_pokemon != player_pokemon and not new_pokemon.is_fainted():
                                self.display.show_message(f"Come back, {player_pokemon.nickname}!")
                                self.display.show_message(f"Go, {new_pokemon.nickname}!")
                                player_pokemon = new_pokemon
                            else:
                                self.display.show_message("Cannot switch to that Pokemon!")
                                continue
                        else:
                            continue
                    else:
                        self.display.show_message("No other Pokemon available!")
                        continue
                        
                elif battle_choice == 4:  # Run
                    game_logger.debug("Player chose RUN")
                    if is_wild:
                        if random.random() < 0.8:  # 80% chance to run from wild Pokemon
                            game_logger.info("Successfully ran from wild Pokemon")
                            return "run"
                        else:
                            self.display.show_message("Can't escape!")
                    else:
                        self.display.show_message("Can't run from a trainer battle!")
                        continue
                
                # Check if opponent fainted
                if opponent_pokemon.is_fainted():
                    game_logger.info("Opponent Pokemon fainted - Player victory")
                    self.display.show_message(f"{opponent_pokemon.species} fainted!")
                    
                    # Award experience
                    exp_gained = self.calculate_exp_gain(player_pokemon, opponent_pokemon)
                    player_pokemon.gain_experience(exp_gained)
                    self.display.show_message(f"{player_pokemon.nickname} gained {exp_gained} experience!")
                    
                    # Check for level up
                    if player_pokemon.level_up():
                        self.display.show_level_up(player_pokemon)
                    
                    return "victory"
                
                # Opponent's turn (if not fainted)
                if not opponent_pokemon.is_fainted():
                    self.opponent_turn(opponent_pokemon, player_pokemon)
                    
                    # Check if player Pokemon fainted
                    if player_pokemon.is_fainted():
                        game_logger.info("Player Pokemon fainted")
                        self.display.show_message(f"{player_pokemon.nickname} fainted!")
                        
                        # Check if player has other Pokemon
                        if self.trainer.has_usable_pokemon():
                            self.display.show_message("Choose another Pokemon!")
                            self.display.show_pokemon_team(self.trainer.pokemon_team)
                            pokemon_choice = self.input_handler.get_pokemon_choice(self.trainer.pokemon_team)
                            if pokemon_choice and pokemon_choice <= len(self.trainer.pokemon_team):
                                new_pokemon = self.trainer.pokemon_team[pokemon_choice - 1]
                                if not new_pokemon.is_fainted():
                                    self.display.show_message(f"Go, {new_pokemon.nickname}!")
                                    player_pokemon = new_pokemon
                                else:
                                    game_logger.info("Battle ended - Player defeat (no usable Pokemon)")
                                    return "defeat"
                            else:
                                game_logger.info("Battle ended - Player defeat (no Pokemon selected)")
                                return "defeat"
                        else:
                            game_logger.info("Battle ended - Player defeat (no usable Pokemon)")
                            return "defeat"
                
                time.sleep(1)  # Brief pause between turns
                
            except Exception as e:
                game_logger.exception_caught(e, "battle_loop", {
                    "battle_turn": battle_turn,
                    "player_hp": player_pokemon.current_hp,
                    "opponent_hp": opponent_pokemon.current_hp,
                    "battle_choice": battle_choice if 'battle_choice' in locals() else None
                })
                # Continue the battle instead of crashing
                self.display.show_message("An error occurred during battle. Continuing...")
                continue
        
        # If we reach max turns, it's a draw
        if battle_turn >= max_turns:
            game_logger.info("Battle ended - Maximum turns reached")
            self.display.show_message("The battle has gone on too long! It's a draw!")
            return "draw"
        
        game_logger.info("Battle loop ended - Player defeat")
        return "defeat"
    
    def opponent_turn(self, opponent_pokemon: Pokemon, player_pokemon: Pokemon):
        """Handle opponent's turn in battle"""
        if opponent_pokemon.moves:
            move = random.choice(opponent_pokemon.moves)
            damage = opponent_pokemon.calculate_damage(move, player_pokemon)
            player_pokemon.take_damage(damage)
            
            self.display.show_message(f"{opponent_pokemon.species} used {move.name}!")
            
            if damage > 0:
                # Use the first type for effectiveness calculation
                primary_type = player_pokemon.types[0] if player_pokemon.types else None
                if primary_type:
                    effectiveness = self.get_effectiveness_message(move.type, player_pokemon.types)
                    self.display.show_message(f"It dealt {damage} damage! {effectiveness}")
                else:
                    self.display.show_message(f"It dealt {damage} damage!")
            else:
                self.display.show_message("The attack missed!")
    
    def get_effectiveness_message(self, attack_type: PokemonType, target_types: List[PokemonType]) -> str:
        """Get effectiveness message for type matchups"""
        effectiveness = 1.0
        
        # Calculate effectiveness against all target types
        for target_type in target_types:
            effectiveness *= Pokemon.get_type_effectiveness_static(attack_type, target_type)
        
        if effectiveness > 1.0:
            return "It's super effective!"
        elif effectiveness < 1.0:
            return "It's not very effective..."
        else:
            return ""
    
    def calculate_exp_gain(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon) -> int:
        """Calculate experience gained from battle"""
        base_exp = opponent_pokemon.level * 10
        level_diff = max(1, opponent_pokemon.level - player_pokemon.level + 5)
        return int(base_exp * level_diff / 10)
    
    def attempt_catch(self, wild_pokemon: Pokemon):
        """Attempt to catch a wild Pokemon"""
        if self.input_handler.get_yes_no("Would you like to try to catch this Pokemon?"):
            # Check if trainer has Pokeballs
            pokeballs = self.trainer.inventory.get_items_by_type("pokeball")
            
            if not pokeballs:
                self.display.show_error("You don't have any Pokeballs!")
                return
            
            # Use the first available pokeball
            pokeball_name = list(pokeballs.keys())[0]
            
            # Calculate catch rate
            catch_rate = self.calculate_catch_rate(wild_pokemon)
            
            self.display.show_catch_attempt(wild_pokemon.species, pokeball_name)
            
            if random.random() < catch_rate:
                # Successful catch
                success = self.trainer.catch_pokemon(wild_pokemon, pokeball_name)
                if success:
                    self.display.show_message(f"Gotcha! {wild_pokemon.species} was caught!")
                    
                    # Ask for nickname
                    nickname = self.input_handler.get_pokemon_nickname(wild_pokemon.species)
                    if nickname:
                        wild_pokemon.nickname = nickname
                    
                    self.trainer.stats["pokemon_caught"] = self.trainer.stats.get("pokemon_caught", 0) + 1
                else:
                    self.display.show_message(f"{wild_pokemon.species} was sent to the PC!")
            else:
                self.display.show_message(f"{wild_pokemon.species} broke free!")
                self.trainer.inventory.remove_item(pokeball_name, 1)  # Still use the pokeball
    
    def calculate_catch_rate(self, pokemon: Pokemon) -> float:
        """Calculate the catch rate for a Pokemon"""
        base_rate = 0.3  # Base 30% catch rate
        
        # Adjust for Pokemon's remaining HP
        hp_factor = 1.0 - (pokemon.current_hp / pokemon.max_hp)
        
        # Adjust for Pokemon's level
        level_factor = max(0.1, 1.0 - (pokemon.level / 100))
        
        return min(0.9, base_rate + (hp_factor * 0.4) + (level_factor * 0.2))
    
    def use_item_in_battle(self, pokemon):
        """Use an item during battle"""
        battle_items = {
            'Potion': self.trainer.inventory.get_item_count('Potion'),
            'Super Potion': self.trainer.inventory.get_item_count('Super Potion'),
            'Hyper Potion': self.trainer.inventory.get_item_count('Hyper Potion'),
            'Full Heal': self.trainer.inventory.get_item_count('Full Heal'),
            'Revive': self.trainer.inventory.get_item_count('Revive')
        }
        
        # Filter out items with 0 count
        available_items = {k: v for k, v in battle_items.items() if v > 0}
        
        if not available_items:
            self.display.show_message("You don't have any items to use!")
            return False
        
        self.display.show_inventory(available_items)
        choice = self.input_handler.get_item_choice(available_items)
        
        if choice is None:
            return False
        
        item_name = list(available_items.keys())[choice - 1]
        
        # Use the item
        success = self.trainer.inventory.remove_item(item_name, 1)
        if not success:
            self.display.show_message("You don't have that item!")
            return False
        
        # Apply item effect
        if item_name == 'Potion':
            pokemon.heal(20)
            self.display.show_message(f"{pokemon.nickname} recovered 20 HP!")
        elif item_name == 'Super Potion':
            pokemon.heal(50)
            self.display.show_message(f"{pokemon.nickname} recovered 50 HP!")
        elif item_name == 'Hyper Potion':
            pokemon.heal(200)
            self.display.show_message(f"{pokemon.nickname} recovered 200 HP!")
        elif item_name == 'Full Heal':
            pokemon.status = None
            self.display.show_message(f"{pokemon.nickname} was cured of all status conditions!")
        elif item_name == 'Revive':
            if pokemon.is_fainted():
                pokemon.heal(pokemon.max_hp // 2)
                self.display.show_message(f"{pokemon.nickname} was revived!")
            else:
                self.display.show_message(f"{pokemon.nickname} is already healthy!")
        
        return True
    
    def switch_pokemon_in_battle(self):
        """Switch Pokemon during battle"""
        available_pokemon = [p for p in self.trainer.pokemon_team if not p.is_fainted()]
        
        if len(available_pokemon) <= 1:
            self.display.show_message("You don't have any other Pokemon!")
            return None
        
        self.display.show_pokemon_team(available_pokemon)
        choice = self.input_handler.get_pokemon_choice(available_pokemon)
        
        if choice and choice <= len(available_pokemon):
            new_pokemon = available_pokemon[choice - 1]  # Convert to 0-based index
            self.display.show_message(f"Come back! Go, {new_pokemon.nickname}!")
            return new_pokemon
        
        return None
    
    def challenge_gym(self):
        """Challenge the gym at current location"""
        location = self.locations.get(self.trainer.current_location, {})
        gym_info = location.get('gym')
        
        if not gym_info:
            self.display.show_message("There's no gym in this location.")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        gym_leader = self.gym_leaders.get(gym_info['leader'])
        
        if not gym_leader:
            self.display.show_message("The gym leader is not available.")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        # Check if already defeated
        if gym_info['badge'] in [badge.name for badge in self.trainer.badges]:
            self.display.show_message("You have already defeated this gym!")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        self.display.show_message(f"You challenge {gym_leader['name']}, the {gym_info['type']} type gym leader!")
        
        if self.input_handler.get_yes_no("Are you ready to battle?"):
            self.gym_battle()
    
    def gym_battle(self):
        """Battle the gym leader"""
        if not self.trainer.current_location:
            self.display.show_error("You're not in a valid location!")
            return
        
        location = self.locations.get(self.trainer.current_location, {})
        gym_info = location.get("gym")
        
        if not gym_info:
            self.display.show_error("There's no gym here!")
            return
        
        gym_leader_name = gym_info["leader"]
        gym_leader_data = self.gym_leaders.get(gym_leader_name)
        
        if not gym_leader_data:
            self.display.show_error("The gym leader isn't here right now!")
            return
        
        # Check if player already has this badge
        badge_name = gym_info["badge"]
        if any(badge.name == badge_name for badge in self.trainer.badges):
            self.display.show_message(f"You've already defeated {gym_leader_data['name']}!")
            return
        
        self.display.show_message(f"Gym Leader {gym_leader_data['name']} wants to battle!")
        self.display.show_message(gym_leader_data["intro"])
        
        # Battle each of the gym leader's Pokemon
        victories = 0
        for pokemon_data in gym_leader_data["pokemon"]:
            gym_pokemon = self.create_trainer_pokemon(pokemon_data)
            
            self.display.show_message(f"{gym_leader_data['name']} sends out {gym_pokemon.species}!")
            
            battle_result = self.start_battle(gym_pokemon, is_wild=False, trainer_name=gym_leader_data['name'])
            
            if battle_result == "victory":
                victories += 1
                self.display.show_message(f"You defeated {gym_pokemon.species}!")
            elif battle_result == "defeat":
                break
            elif battle_result == "no_pokemon":
                self.display.show_error("You need Pokemon to battle!")
                return
        
        # Check if player won all battles
        if victories == len(gym_leader_data["pokemon"]):
            # Award badge
            badge = Badge(
                name=badge_name,
                gym_leader=gym_leader_data['name'],
                location=self.trainer.current_location,
                date_earned=datetime.now()
            )
            self.trainer.badges.append(badge)
            
            # Award prize money
            prize_money = gym_info["prize_money"]
            self.trainer.add_money(prize_money)
            
            self.display.show_message(f"Congratulations! You defeated {gym_leader_data['name']}!")
            self.display.show_message(f"You earned the {badge_name}!")
            self.display.show_message(f"You received ${prize_money}!")
            
            # Update stats
            self.trainer.stats["gyms_defeated"] = self.trainer.stats.get("gyms_defeated", 0) + 1
        else:
            self.display.show_message(f"You were defeated by {gym_leader_data['name']}!")
            self.display.show_message("Come back when you're stronger!")
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def visit_shop(self):
        """Visit the shop at current location"""
        location = self.locations.get(self.trainer.current_location, {})
        shop_info = location.get('shop')
        
        if not shop_info:
            self.display.show_message("There's no shop in this location.")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        shop_items = self.shops.get(shop_info['type'], {})
        
        while True:
            self.display.show_shop_items(shop_items, self.trainer.money)
            
            choice = self.input_handler.get_shop_choice(shop_items)
            
            if choice == "quit":
                break
            elif choice in shop_items:
                item = shop_items[choice]
                quantity = self.input_handler.get_quantity(item['name'], 99)
                
                total_cost = item['price'] * quantity
                
                if self.trainer.money >= total_cost:
                    if self.input_handler.confirm_action(f"Buy {quantity} {item['name']} for ${total_cost}?"):
                        self.trainer.spend_money(total_cost)
                        self.trainer.inventory.add_item(item['name'], quantity)
                        self.display.show_success(f"Bought {quantity} {item['name']}!")
                else:
                    self.display.show_error("You don't have enough money!")
    
    def visit_pokemon_center(self):
        """Visit the Pokemon Center"""
        self.display.show_message("Welcome to the Pokemon Center!")
        self.display.show_message("We'll heal your Pokemon to full health!")
        
        # Heal all Pokemon
        for pokemon in self.trainer.pokemon_team:
            pokemon.heal()
        
        self.display.show_success("Your Pokemon have been healed!")
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def view_team(self):
        """View Pokemon team"""
        if not self.trainer.pokemon_team:
            self.display.show_message("You don't have any Pokemon!")
        else:
            self.display.show_pokemon_team(self.trainer.pokemon_team)
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def view_bag(self):
        """View trainer's bag"""
        items = self.trainer.inventory.get_all_items()
        
        if not items:
            self.display.show_message("Your bag is empty!")
        else:
            self.display.show_message("Your Bag:")
            self.display.show_message("-" * 30)
            
            for item_name, quantity in items.items():
                item_db = self.trainer.inventory.get_item_database()
                description = item_db.get(item_name, {}).get("description", "Unknown item")
                self.display.show_message(f"  {item_name} x{quantity} - {description}")
            
            self.display.show_message("-" * 30)
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def view_pokedex(self):
        """View Pokedex"""
        seen_count = len(self.trainer.pokedex_seen)
        caught_count = len(self.trainer.pokedex_caught)
        
        self.display.show_pokedex_summary(seen_count, caught_count)
        
        if self.trainer.pokedex_caught:
            self.display.show_message("\nPokemon You've Caught:")
            self.display.show_message("-" * 30)
            for species in sorted(self.trainer.pokedex_caught):
                self.display.show_message(f"  {species}")
            self.display.show_message("-" * 30)
        else:
            self.display.show_message("\nYou haven't caught any Pokemon yet!")
        
        if self.trainer.pokedex_seen:
            self.display.show_message("\nPokemon You've Seen:")
            self.display.show_message("-" * 30)
            for species in sorted(self.trainer.pokedex_seen):
                if species not in self.trainer.pokedex_caught:
                    self.display.show_message(f"  {species} (Seen only)")
            self.display.show_message("-" * 30)
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def view_trainer_info(self):
        """View trainer information"""
        self.display.show_trainer_info(self.trainer)
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def travel(self):
        """Travel to a different location"""
        current_location = self.locations.get(self.trainer.current_location, {})
        connections = current_location.get('connections', [])
        
        if not connections:
            self.display.show_message("You can't travel from here!")
            self.input_handler.wait_for_input("Press Enter to continue...")
            return
        
        self.display.show_message("Where would you like to go?")
        
        for i, location_id in enumerate(connections, 1):
            location = self.locations.get(location_id, {})
            self.display.show_message(f"{i}. {location.get('name', 'Unknown')}")
        
        choice = self.input_handler.get_menu_choice(len(connections))
        
        if choice is not None:
            if 1 <= choice <= len(connections):
                new_location = connections[choice - 1]
                
                # Validate that the new location exists
                if new_location in self.locations:
                    self.trainer.move_to_location(new_location)
                    
                    location_name = self.locations.get(new_location, {}).get('name', 'Unknown')
                    self.display.show_message(f"You traveled to {location_name}!")
                else:
                    self.display.show_error(f"Invalid destination: {new_location}")
                    self.display.show_message("Travel cancelled.")
            else:
                self.display.show_error("Invalid choice!")
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def save_game(self):
        """Save the current game"""
        save_name = self.input_handler.get_save_name()
        
        if self.save_manager.save_game(self.trainer, save_name):
            self.display.show_success("Game saved successfully!")
        else:
            self.display.show_error("Failed to save game!")
        
        self.input_handler.wait_for_input("Press Enter to continue...")
    
    def show_settings(self):
        """Show game settings"""
        self.display.show_message("Game Settings:")
        self.display.show_message("1. Animation Speed")
        self.display.show_message("2. Auto-save Interval")
        self.display.show_message("3. Display Width")
        self.display.show_message("4. Back")
        
        choice = self.input_handler.get_menu_choice(4)
        
        if choice == 1:
            speed = self.input_handler.get_integer("Enter animation speed (1-10): ", 1, 10)
            self.display.animation_speed = speed / 10.0
            self.display.show_success("Animation speed updated!")
        elif choice == 2:
            interval = self.input_handler.get_integer("Enter auto-save interval (minutes): ", 1, 60)
            self.trainer.settings["auto_save_interval"] = interval
            self.display.show_success("Auto-save interval updated!")
        elif choice == 3:
            width = self.input_handler.get_integer("Enter display width (40-120): ", 40, 120)
            self.display.width = width
            self.display.show_success("Display width updated!")
        
        if choice != 4:
            self.input_handler.wait_for_input("Press Enter to continue...")
    
    def quit_game(self):
        """Quit the game"""
        if self.input_handler.get_yes_no("Do you want to save before quitting?"):
            self.save_game()
        
        self.display.show_message("Thanks for playing!")
        self.game_running = False
    
    # Helper methods for game initialization
    
    def initialize_locations(self) -> Dict:
        """Initialize game locations"""
        return {
            "pallet_town": {
                "name": "Pallet Town",
                "description": "A quiet town with a Pokemon research lab.",
                "wild_pokemon": ["Pidgey", "Rattata"],
                "level_range": [2, 4],
                "pokemon_center": True,
                "shop": {"type": "basic"},
                "connections": ["route_1", "oak_lab"]
            },
            "oak_lab": {
                "name": "Professor Oak's Lab",
                "description": "A research laboratory filled with Pokemon research equipment.",
                "pokemon_center": False,
                "shop": False,
                "connections": ["pallet_town"]
            },
            "route_1": {
                "name": "Route 1",
                "description": "A peaceful route connecting Pallet Town to Viridian City.",
                "wild_pokemon": ["Pidgey", "Rattata", "Caterpie", "Weedle"],
                "level_range": [2, 5],
                "connections": ["pallet_town", "viridian_city"]
            },
            "viridian_city": {
                "name": "Viridian City",
                "description": "A city with a Pokemon Gym and a forest nearby.",
                "wild_pokemon": ["Pidgey", "Rattata"],
                "level_range": [3, 5],
                "pokemon_center": True,
                "shop": {"type": "basic"},
                "gym": {"leader": "giovanni", "type": "Ground", "badge": "Earth Badge", "prize_money": 5000},
                "connections": ["route_1", "viridian_forest"]
            },
            "viridian_forest": {
                "name": "Viridian Forest",
                "description": "A dense forest full of Bug-type Pokemon.",
                "wild_pokemon": ["Caterpie", "Weedle", "Pikachu"],
                "level_range": [3, 6],
                "connections": ["viridian_city", "pewter_city"]
            },
            "pewter_city": {
                "name": "Pewter City",
                "description": "A city known for its Rock-type Pokemon Gym.",
                "wild_pokemon": ["Spearow", "Sandshrew"],
                "level_range": [4, 7],
                "pokemon_center": True,
                "shop": {"type": "basic"},
                "gym": {"leader": "brock", "type": "Rock", "badge": "Boulder Badge", "prize_money": 1000},
                "connections": ["viridian_forest", "route_3"]
            },
            "route_3": {
                "name": "Route 3",
                "description": "A route leading to Mt. Moon.",
                "wild_pokemon": ["Spearow", "Sandshrew", "Jigglypuff"],
                "connections": ["pewter_city", "mt_moon"]
            },
            "mt_moon": {
                "name": "Mt. Moon",
                "description": "A mysterious mountain cave.",
                "wild_pokemon": ["Zubat", "Geodude", "Clefairy"],
                "connections": ["route_3", "cerulean_city"]
            },
            "cerulean_city": {
                "name": "Cerulean City",
                "description": "A city with a Water-type Pokemon Gym.",
                "wild_pokemon": ["Oddish", "Bellsprout"],
                "pokemon_center": True,
                "shop": {"type": "advanced"},
                "gym": {"leader": "misty", "type": "Water", "badge": "Cascade Badge", "prize_money": 2000},
                "connections": ["mt_moon", "route_5"]
            },
            "route_5": {
                "name": "Route 5",
                "description": "A route south of Cerulean City.",
                "wild_pokemon": ["Oddish", "Bellsprout", "Meowth"],
                "level_range": [10, 16],
                "connections": ["cerulean_city"]
            }
        }
    
    def initialize_wild_pokemon(self) -> Dict:
        """Initialize wild Pokemon data"""
        return {
            "pallet_town": ["Pidgey", "Rattata"],
            "route_1": ["Pidgey", "Rattata", "Caterpie"],
            "viridian_city": ["Pidgey", "Rattata"],
            "viridian_forest": ["Caterpie", "Pikachu"],
            "pewter_city": ["Spearow", "Sandshrew"]
        }
    
    def initialize_gym_leaders(self) -> Dict:
        """Initialize gym leaders"""
        return {
            "brock": {
                "name": "Brock",
                "intro": "I'm Brock! I'm Pewter's Gym Leader! My rock-hard willpower is evident even in my Pokemon!",
                "pokemon": [
                    {"species": "Geodude", "level": 12, "moves": ["Tackle", "Defense Curl"]},
                    {"species": "Onix", "level": 14, "moves": ["Tackle", "Screech", "Bind"]}
                ]
            },
            "misty": {
                "name": "Misty",
                "intro": "Hi, I'm Misty! I'm Cerulean's Gym Leader! I'm an expert on Water-type Pokemon!",
                "pokemon": [
                    {"species": "Staryu", "level": 18, "moves": ["Tackle", "Water Gun"]},
                    {"species": "Starmie", "level": 21, "moves": ["Tackle", "Water Gun", "Harden"]}
                ]
            },
            "giovanni": {
                "name": "Giovanni",
                "intro": "I am Giovanni! For your insolence, you will feel a world of pain!",
                "pokemon": [
                    {"species": "Rhyhorn", "level": 45, "moves": ["Tackle", "Horn Attack", "Fury Attack"]},
                    {"species": "Dugtrio", "level": 42, "moves": ["Dig", "Slash", "Sand Attack"]},
                    {"species": "Nidoqueen", "level": 44, "moves": ["Tackle", "Poison Sting", "Body Slam"]},
                    {"species": "Nidoking", "level": 45, "moves": ["Tackle", "Poison Sting", "Thrash"]},
                    {"species": "Rhydon", "level": 50, "moves": ["Tackle", "Horn Attack", "Fury Attack", "Take Down"]}
                ]
            }
        }
    
    def initialize_shops(self) -> Dict:
        """Initialize shop inventories"""
        return {
            "basic": {
                "pokeball": {"name": "Pokeball", "price": 200, "description": "A basic ball for catching Pokemon"},
                "potion": {"name": "Potion", "price": 300, "description": "Restores 20 HP"},
                "antidote": {"name": "Antidote", "price": 100, "description": "Cures poison"},
                "paralyze_heal": {"name": "Paralyze Heal", "price": 200, "description": "Cures paralysis"}
            },
            "advanced": {
                "pokeball": {"name": "Pokeball", "price": 200, "description": "A basic ball for catching Pokemon"},
                "great_ball": {"name": "Great Ball", "price": 600, "description": "A better ball for catching Pokemon"},
                "potion": {"name": "Potion", "price": 300, "description": "Restores 20 HP"},
                "super_potion": {"name": "Super Potion", "price": 700, "description": "Restores 50 HP"},
                "antidote": {"name": "Antidote", "price": 100, "description": "Cures poison"},
                "paralyze_heal": {"name": "Paralyze Heal", "price": 200, "description": "Cures paralysis"},
                "awakening": {"name": "Awakening", "price": 250, "description": "Cures sleep"}
            }
        }
    
    def initialize_starter_pokemon(self) -> Dict:
        """Initialize starter Pokemon"""
        return {
            1: {"species": "Bulbasaur", "level": 5, "moves": ["Tackle", "Growl"]},
            2: {"species": "Charmander", "level": 5, "moves": ["Scratch", "Growl"]},
            3: {"species": "Squirtle", "level": 5, "moves": ["Tackle", "Tail Whip"]}
        }
    
    def get_starter_pokemon(self, choice: str) -> Pokemon:
        """Get starter Pokemon based on choice"""
        # Map string choices to numbers
        choice_map = {
            "Bulbasaur": 1,
            "Charmander": 2,
            "Squirtle": 3
        }
        
        choice_num = choice_map.get(choice, 1)
        starter_data = self.starter_pokemon.get(choice_num)
        
        if starter_data:
            return self.create_trainer_pokemon(starter_data)
        
        # Default to Bulbasaur if invalid choice
        return self.create_trainer_pokemon(self.starter_pokemon[1])
    
    def create_wild_pokemon(self, species: str) -> Pokemon:
        """Create a wild Pokemon for battle"""
        # Wild Pokemon level range based on location
        location = self.locations.get(self.trainer.current_location, {})
        level_range = location.get("level_range", [2, 5])
        
        level = random.randint(level_range[0], level_range[1])
        
        # Small chance for shiny Pokemon
        is_shiny = random.random() < 0.001  # 1 in 1000 chance
        
        wild_pokemon = Pokemon(species, level, is_shiny)
        
        # Wild Pokemon are at full health
        wild_pokemon.heal()
        
        return wild_pokemon
    
    def create_trainer_pokemon(self, pokemon_data: Dict) -> Pokemon:
        """Create a trainer's Pokemon from data"""
        pokemon = Pokemon(pokemon_data["species"], pokemon_data["level"])
        
        # Set custom moves if specified
        if "moves" in pokemon_data:
            from .pokemon import Move, PokemonType
            
            # Move database for proper move creation
            move_database = {
                "Tackle": Move("Tackle", PokemonType.NORMAL, 40, 100, 35, 35, "A physical attack."),
                "Growl": Move("Growl", PokemonType.NORMAL, 0, 100, 40, 40, "Lowers opponent's Attack."),
                "Scratch": Move("Scratch", PokemonType.NORMAL, 40, 100, 35, 35, "Scratches with sharp claws."),
                "Tail Whip": Move("Tail Whip", PokemonType.NORMAL, 0, 100, 30, 30, "Lowers opponent's Defense."),
                "Defense Curl": Move("Defense Curl", PokemonType.NORMAL, 0, 100, 40, 40, "Raises user's Defense."),
                "Screech": Move("Screech", PokemonType.NORMAL, 0, 85, 40, 40, "Harshly lowers opponent's Defense."),
                "Bind": Move("Bind", PokemonType.NORMAL, 15, 85, 20, 20, "Binds the target for 4-5 turns."),
                "Water Gun": Move("Water Gun", PokemonType.WATER, 40, 100, 25, 25, "Blasts water at the target."),
                "Harden": Move("Harden", PokemonType.NORMAL, 0, 100, 30, 30, "Raises user's Defense."),
                "Horn Attack": Move("Horn Attack", PokemonType.NORMAL, 65, 100, 25, 25, "Attacks with a horn."),
                "Fury Attack": Move("Fury Attack", PokemonType.NORMAL, 15, 85, 20, 20, "Attacks 2-5 times in a row."),
                "Dig": Move("Dig", PokemonType.GROUND, 80, 100, 10, 10, "Digs underground then attacks."),
                "Slash": Move("Slash", PokemonType.NORMAL, 70, 100, 20, 20, "High critical hit ratio."),
                "Sand Attack": Move("Sand Attack", PokemonType.GROUND, 0, 100, 15, 15, "Lowers opponent's accuracy."),
                "Poison Sting": Move("Poison Sting", PokemonType.POISON, 15, 100, 35, 35, "May poison the target."),
                "Body Slam": Move("Body Slam", PokemonType.NORMAL, 85, 100, 15, 15, "May paralyze the target."),
                "Thrash": Move("Thrash", PokemonType.NORMAL, 120, 100, 10, 10, "Attacks for 2-3 turns then confuses user."),
                "Take Down": Move("Take Down", PokemonType.NORMAL, 90, 85, 20, 20, "User takes recoil damage.")
            }
            
            pokemon.moves = []
            for move_name in pokemon_data["moves"]:
                if move_name in move_database:
                    pokemon.moves.append(move_database[move_name])
                else:
                    # Default move if not found
                    pokemon.moves.append(Move(move_name, PokemonType.NORMAL, 40, 100, 25, 25, "A basic move"))
        
        return pokemon
    
    def create_badge(self, gym_info: Dict):
        """Create a badge from gym info"""
        from .trainer import Badge
        
        return Badge(
            name=gym_info["badge"],
            gym_leader=gym_info["leader"],
            location=self.trainer.current_location,
            date_earned=datetime.now()
        ) 