#!/usr/bin/env python3
"""
Pokemon Adventure Game - Main Entry Point

A comprehensive text-based Pokemon adventure game featuring:
- Pokemon battles and collection
- Gym challenges and badges
- World exploration
- Save/load functionality
- Comprehensive statistics tracking
"""

import os
import sys
import json
from typing import Optional

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_engine import GameEngine
from game.save_manager import SaveManager
from utils.display import Display
from utils.input_handler import InputHandler

class PokemonGame:
    def __init__(self):
        self.game_engine: Optional[GameEngine] = None
        self.save_manager = SaveManager()
        self.display = Display()
        self.input_handler = InputHandler()
        
    def show_main_menu(self) -> str:
        """Display the main menu and get user choice"""
        self.display.clear_screen()
        self.display.show_title()
        
        menu_options = [
            "1. New Game",
            "2. Load Game", 
            "3. Game Statistics",
            "4. Settings",
            "5. About",
            "6. Exit"
        ]
        
        self.display.show_menu("Main Menu", menu_options)
        return self.input_handler.get_menu_choice(len(menu_options))
    
    def start_new_game(self):
        """Initialize a new game"""
        self.display.clear_screen()
        self.display.show_message("Starting a new Pokemon adventure!")
        
        # Create new game engine
        self.game_engine = GameEngine()
        
        # Start the new game (this handles trainer creation)
        self.game_engine.start_new_game()
    
    def load_game(self):
        """Load an existing game"""
        save_files = self.save_manager.get_save_files()
        
        if not save_files:
            self.display.show_message("No save files found!")
            self.input_handler.wait_for_input()
            return
        
        self.display.clear_screen()
        self.display.show_message("Select a save file to load:")
        
        for i, save_file in enumerate(save_files, 1):
            save_info = self.save_manager.get_save_info(save_file)
            self.display.show_message(f"{i}. {save_info['trainer_name']} - Level {save_info['trainer_level']} - {save_info['play_time']}")
        
        choice = self.input_handler.get_menu_choice(len(save_files))
        
        if choice:
            selected_save = save_files[choice - 1]  # choice is already an integer
            self.game_engine = GameEngine()
            success = self.game_engine.load_game(selected_save)
            
            if not success:
                self.display.show_message("Failed to load game!")
                self.input_handler.wait_for_input()
    
    def show_statistics(self):
        """Show game statistics"""
        self.display.clear_screen()
        stats = self.save_manager.get_global_statistics()
        
        self.display.show_message("=== GAME STATISTICS ===")
        self.display.show_message(f"Total Games Played: {stats.get('total_games', 0)}")
        self.display.show_message(f"Total Play Time: {stats.get('total_play_time', '0h 0m')}")
        self.display.show_message(f"Pokemon Caught: {stats.get('total_pokemon_caught', 0)}")
        self.display.show_message(f"Battles Won: {stats.get('total_battles_won', 0)}")
        self.display.show_message(f"Gyms Defeated: {stats.get('total_gyms_defeated', 0)}")
        
        self.input_handler.wait_for_input()
    
    def show_settings(self):
        """Show and modify game settings"""
        self.display.clear_screen()
        settings_options = [
            "1. Animation Speed",
            "2. Auto-Save",
            "3. Battle Difficulty",
            "4. Sound Effects (Text)",
            "5. Back to Main Menu"
        ]
        
        self.display.show_menu("Settings", settings_options)
        choice = self.input_handler.get_menu_choice(len(settings_options))
        
        # Settings logic would go here
        if choice and choice != 5:
            self.display.show_message("Settings feature coming soon!")
            self.input_handler.wait_for_input()
    
    def show_about(self):
        """Show about information"""
        self.display.clear_screen()
        self.display.show_message("=== ABOUT ===")
        self.display.show_message("Pokemon Open World Game v1.0")
        self.display.show_message("A text-based Pokemon adventure inspired by Pokemon Go")
        self.display.show_message("")
        self.display.show_message("Created by: Mr-Neutr0n")
        self.display.show_message("GitHub: https://github.com/Mr-Neutr0n/pokemon_game")
        self.display.show_message("")
        self.display.show_message("This game is a tribute to the Pokemon franchise.")
        self.display.show_message("All Pokemon names and concepts are property of Nintendo/Game Freak.")
        
        self.input_handler.wait_for_input()
    
    def run(self):
        """Main game loop"""
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == 1:
                    self.start_new_game()
                elif choice == 2:
                    self.load_game()
                elif choice == 3:
                    self.show_statistics()
                elif choice == 4:
                    self.show_settings()
                elif choice == 5:
                    self.show_about()
                elif choice == 6:
                    self.display.show_message("Thanks for playing! Gotta catch 'em all!")
                    break
                else:
                    self.display.show_message("Invalid choice. Please try again.")
                    self.input_handler.wait_for_input()
                    
            except KeyboardInterrupt:
                self.display.show_message("\nGame interrupted. Saving progress...")
                if self.game_engine:
                    self.game_engine.save_game()
                break
            except Exception as e:
                self.display.show_message(f"An error occurred: {str(e)}")
                self.input_handler.wait_for_input()

def main():
    """Entry point of the application"""
    # Ensure required directories exist
    os.makedirs("saves", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Start the game
    game = PokemonGame()
    game.run()

if __name__ == "__main__":
    main() 