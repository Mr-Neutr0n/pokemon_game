"""
Display utility for game output and formatting
"""

import os
import time
from typing import List, Dict, Optional

class Display:
    """Handles all game display and formatting"""
    
    def __init__(self):
        self.width = 80
        self.animation_speed = 0.03
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_title(self):
        """Display the game title"""
        title = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗           ║
║  ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗ ████║██╔═══██╗████╗  ██║           ║
║  ██████╔╝██║   ██║█████╔╝ █████╗  ██╔████╔██║██║   ██║██╔██╗ ██║           ║
║  ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║           ║
║  ██║     ╚██████╔╝██║  ██╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║           ║
║  ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝           ║
║                                                                              ║
║                    ╔═══════════════════════════════════╗                    ║
║                    ║     OPEN WORLD ADVENTURE GAME     ║                    ║
║                    ╚═══════════════════════════════════╝                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(title)
    
    def show_menu(self, title: str, options: List[str]):
        """Display a menu with options"""
        print(f"\n{'='*self.width}")
        print(f"{title:^{self.width}}")
        print('='*self.width)
        
        for option in options:
            print(f"  {option}")
        
        print('='*self.width)
        print("Enter your choice: ", end="")
    
    def show_message(self, message: str, delay: bool = False):
        """Display a message"""
        if delay:
            self.animate_text(message)
        else:
            print(message)
    
    def animate_text(self, text: str):
        """Animate text character by character"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(self.animation_speed)
        print()
    
    def show_pokemon_info(self, pokemon, detailed: bool = False):
        """Display Pokemon information"""
        from game.pokemon import Pokemon
        
        if not isinstance(pokemon, Pokemon):
            return
        
        print(f"\n┌─ {pokemon.species} ({'★' if pokemon.is_shiny else '●'}) ─┐")
        print(f"│ Level: {pokemon.level}")
        print(f"│ HP: {pokemon.current_hp}/{pokemon.max_hp}")
        print(f"│ Type: {'/'.join([t.value for t in pokemon.types])}")
        print(f"│ Nature: {pokemon.nature}")
        
        if detailed:
            print(f"│ Stats:")
            print(f"│   Attack: {pokemon.attack}")
            print(f"│   Defense: {pokemon.defense}")
            print(f"│   Sp. Atk: {pokemon.special_attack}")
            print(f"│   Sp. Def: {pokemon.special_defense}")
            print(f"│   Speed: {pokemon.speed}")
            print(f"│ Moves:")
            for move in pokemon.moves:
                print(f"│   {move.name} ({move.pp}/{move.max_pp} PP)")
            print(f"│ Ability: {pokemon.ability}")
            print(f"│ Friendship: {pokemon.friendship}")
            if pokemon.status_condition:
                print(f"│ Status: {pokemon.status_condition}")
        
        print("└─────────────────────┘")
    
    def show_battle_scene(self, player_pokemon, opponent_pokemon, is_wild: bool = True):
        """Display battle scene"""
        opponent_type = "Wild" if is_wild else "Enemy"
        
        print(f"\n{'='*self.width}")
        print(f"BATTLE! {opponent_type} {opponent_pokemon.species} appeared!")
        print('='*self.width)
        
        # Show Pokemon status
        print(f"\n{opponent_pokemon.species} (Lv.{opponent_pokemon.level})")
        print(f"HP: {self.get_hp_bar(opponent_pokemon)}")
        
        print(f"\n{player_pokemon.species} (Lv.{player_pokemon.level})")
        print(f"HP: {self.get_hp_bar(player_pokemon)}")
        
        if player_pokemon.status_condition:
            print(f"Status: {player_pokemon.status_condition}")
        
        print()
    
    def get_hp_bar(self, pokemon, width: int = 20) -> str:
        """Generate HP bar visualization"""
        from game.pokemon import Pokemon
        
        if not isinstance(pokemon, Pokemon):
            return ""
        
        hp_ratio = pokemon.current_hp / pokemon.max_hp
        filled_bars = int(hp_ratio * width)
        empty_bars = width - filled_bars
        
        # Color coding based on HP percentage
        if hp_ratio > 0.5:
            bar_color = "█"  # Green (full)
        elif hp_ratio > 0.2:
            bar_color = "█"  # Yellow (medium)
        else:
            bar_color = "█"  # Red (low)
        
        bar = f"[{bar_color * filled_bars}{'░' * empty_bars}] {pokemon.current_hp}/{pokemon.max_hp}"
        return bar
    
    def show_battle_menu(self):
        """Display battle menu options"""
        options = [
            "1. Attack",
            "2. Items",
            "3. Pokemon",
            "4. Run"
        ]
        
        print("\nWhat will you do?")
        for option in options:
            print(f"  {option}")
        print()
    
    def show_move_selection(self, pokemon):
        """Display move selection menu"""
        from game.pokemon import Pokemon
        
        if not isinstance(pokemon, Pokemon):
            return
        
        print(f"\n{pokemon.species}'s moves:")
        for i, move in enumerate(pokemon.moves, 1):
            pp_info = f"({move.pp}/{move.max_pp} PP)"
            type_info = f"[{move.type.value}]"
            print(f"  {i}. {move.name} {type_info} {pp_info}")
        print()
    
    def show_inventory(self, inventory, item_type: str = None):
        """Display inventory items"""
        from game.trainer import Inventory
        
        if not isinstance(inventory, Inventory):
            return
        
        if item_type:
            items = inventory.get_items_by_type(item_type)
            print(f"\n{item_type.title()} Items:")
        else:
            items = inventory.items
            print("\nInventory:")
        
        if not items:
            print("  No items found.")
            return
        
        for i, (item_name, quantity) in enumerate(items.items(), 1):
            item_db = inventory.get_item_database()
            description = item_db.get(item_name, {}).get("description", "Unknown item")
            print(f"  {i}. {item_name} x{quantity} - {description}")
        print()
    
    def show_pokemon_team(self, pokemon_team):
        """Display Pokemon team"""
        print("\nYour Pokemon Team:")
        
        if not pokemon_team:
            print("  No Pokemon in your team!")
            return
        
        for i, pokemon in enumerate(pokemon_team, 1):
            status = ""
            if pokemon.is_fainted():
                status = " (Fainted)"
            elif pokemon.status_condition:
                status = f" ({pokemon.status_condition})"
            
            print(f"  {i}. {pokemon.species} (Lv.{pokemon.level}) - {pokemon.current_hp}/{pokemon.max_hp} HP{status}")
        print()
    
    def show_location_info(self, location_name: str, description: str, available_actions: List[str]):
        """Display location information"""
        print(f"\n{'='*self.width}")
        print(f"{location_name:^{self.width}}")
        print('='*self.width)
        print(f"\n{description}")
        
        if available_actions:
            print("\nAvailable actions:")
            for i, action in enumerate(available_actions, 1):
                print(f"  {i}. {action}")
        print()
    
    def show_shop_menu(self, shop_items: Dict[str, int]):
        """Display shop items"""
        print("\nShop Items:")
        print("-" * 40)
        
        for i, (item_name, price) in enumerate(shop_items.items(), 1):
            print(f"  {i}. {item_name} - ${price}")
        
        print("-" * 40)
        print("Enter item number to buy (0 to exit): ", end="")
    
    def show_shop_items(self, shop_items: Dict[str, Dict], trainer_money: int):
        """Display shop items with money check"""
        print(f"\n{'='*50}")
        print(f"{'SHOP':^50}")
        print(f"{'='*50}")
        print(f"Your Money: ${trainer_money}")
        print("-" * 50)
        
        if not shop_items:
            print("  No items available.")
            return
        
        for i, (item_key, item_data) in enumerate(shop_items.items(), 1):
            name = item_data.get("name", item_key)
            price = item_data.get("price", 0)
            description = item_data.get("description", "No description")
            
            affordable = "✓" if trainer_money >= price else "✗"
            print(f"  {i}. {name} - ${price} {affordable}")
            print(f"     {description}")
        
        print("-" * 50)
        print("Enter item number to buy (0 to exit): ", end="")
    
    def show_pokedex_entry(self, pokemon_species: str, is_caught: bool = False):
        """Display Pokedex entry"""
        # This would normally load from a database
        pokedex_data = {
            "Bulbasaur": {
                "number": "001",
                "category": "Seed Pokemon",
                "height": "0.7 m",
                "weight": "6.9 kg",
                "description": "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokemon."
            },
            "Charmander": {
                "number": "004",
                "category": "Lizard Pokemon", 
                "height": "0.6 m",
                "weight": "8.5 kg",
                "description": "Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail."
            },
            "Squirtle": {
                "number": "007",
                "category": "Tiny Turtle Pokemon",
                "height": "0.5 m", 
                "weight": "9.0 kg",
                "description": "After birth, its back swells and hardens into a shell. Powerfully sprays foam from its mouth."
            }
        }
        
        data = pokedex_data.get(pokemon_species, {
            "number": "???",
            "category": "Unknown Pokemon",
            "height": "??? m",
            "weight": "??? kg", 
            "description": "No data available."
        })
        
        print(f"\n┌─ Pokedex Entry #{data['number']} ─┐")
        print(f"│ {pokemon_species}")
        print(f"│ {data['category']}")
        print(f"│ Height: {data['height']}")
        print(f"│ Weight: {data['weight']}")
        print(f"│")
        
        # Word wrap description
        desc_lines = self.wrap_text(data['description'], 35)
        for line in desc_lines:
            print(f"│ {line}")
        
        if is_caught:
            print(f"│ Status: CAUGHT")
        else:
            print(f"│ Status: SEEN")
        
        print("└─────────────────────────┘")
    
    def show_pokedex_summary(self, seen_count: int, caught_count: int):
        """Display Pokedex summary"""
        total_pokemon = 151  # Original 151 Pokemon
        seen_percentage = (seen_count / total_pokemon) * 100
        caught_percentage = (caught_count / total_pokemon) * 100
        
        print(f"\n┌─ Pokedex Summary ─┐")
        print(f"│ Pokemon Seen: {seen_count}/{total_pokemon} ({seen_percentage:.1f}%)")
        print(f"│ Pokemon Caught: {caught_count}/{total_pokemon} ({caught_percentage:.1f}%)")
        print(f"│ Completion: {caught_percentage:.1f}%")
        print("└───────────────────┘")
    
    def wrap_text(self, text: str, width: int) -> List[str]:
        """Wrap text to specified width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= width:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def show_trainer_info(self, trainer):
        """Display trainer information"""
        from game.trainer import Trainer
        
        if not isinstance(trainer, Trainer):
            return
        
        print(f"\n┌─ Trainer Info ─┐")
        print(f"│ Name: {trainer.name}")
        print(f"│ Level: {trainer.level}")
        print(f"│ Money: ${trainer.money}")
        print(f"│ Location: {trainer.current_location}")
        print(f"│ Pokemon: {len(trainer.pokemon_team)}/{trainer.max_team_size}")
        print(f"│ Badges: {trainer.get_badge_count()}")
        print(f"│ Pokedex: {len(trainer.pokedex_caught)}/151")
        print(f"│ ID: {trainer.trainer_id}")
        print("└─────────────────┘")
    
    def show_evolution_scene(self, pokemon, old_species: str):
        """Display evolution animation"""
        print(f"\n{'='*self.width}")
        print(f"What? {old_species} is evolving!")
        print('='*self.width)
        
        # Simple evolution animation
        for i in range(3):
            print(".", end="", flush=True)
            time.sleep(0.5)
        
        print(f"\n\nCongratulations! {old_species} evolved into {pokemon.species}!")
        print('='*self.width)
    
    def show_catch_attempt(self, pokemon_species: str, pokeball_type: str, trainer_name: str = "You"):
        """Display catch attempt animation"""
        print(f"\n{trainer_name} used {pokeball_type}!")
        
        # Simple catch animation
        for i in range(3):
            print("*", end="", flush=True)
            time.sleep(0.3)
        print()
    
    def show_catch_success(self, pokemon_species: str):
        """Display successful catch message"""
        print(f"\nGotcha! {pokemon_species} was caught!")
        print(f"{pokemon_species} was added to your team!")
    
    def show_catch_failure(self):
        """Display failed catch message"""
        print("\nOh no! The Pokemon broke free!")
    
    def show_level_up(self, pokemon):
        """Display level up message"""
        print(f"\n{pokemon.species} grew to level {pokemon.level}!")
        
    def show_stats_summary(self, trainer):
        """Display trainer statistics"""
        from game.trainer import Trainer
        
        if not isinstance(trainer, Trainer):
            return
        
        print(f"\n┌─ Statistics ─┐")
        print(f"│ Pokemon Caught: {trainer.stats['pokemon_caught']}")
        print(f"│ Battles Won: {trainer.stats['battles_won']}")
        print(f"│ Battles Lost: {trainer.stats['battles_lost']}")
        print(f"│ Steps Taken: {trainer.stats['steps_taken']}")
        print(f"│ Play Time: {trainer.stats['play_time']} minutes")
        print(f"│ Gyms Defeated: {trainer.stats['gyms_defeated']}")
        print(f"│ Pokemon Evolved: {trainer.stats['pokemon_evolved']}")
        print(f"│ Items Used: {trainer.stats['items_used']}")
        print("└───────────────┘")
    
    def show_error(self, message: str):
        """Display error message"""
        print(f"\n❌ Error: {message}")
    
    def show_success(self, message: str):
        """Display success message"""
        print(f"\n✅ {message}")
    
    def show_warning(self, message: str):
        """Display warning message"""
        print(f"\n⚠️  Warning: {message}")
    
    def show_separator(self):
        """Display a separator line"""
        print("-" * self.width) 