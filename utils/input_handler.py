"""
Input handler for managing user input and validation
"""

import re
from typing import Optional, List, Union

class InputHandler:
    """Handles all user input and validation"""
    
    def __init__(self):
        self.valid_yes_responses = ['y', 'yes', 'yeah', 'yep', 'true', '1']
        self.valid_no_responses = ['n', 'no', 'nope', 'false', '0']
        
        # Import logger here to avoid circular imports
        try:
            from utils.logger import game_logger
            self.logger = game_logger
        except ImportError:
            self.logger = None
    
    def get_input(self, prompt: str = "") -> str:
        """Get basic input from user with improved error handling"""
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                return input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                attempts += 1
                if attempts >= max_attempts:
                    if self.logger:
                        self.logger.warning("Maximum input attempts reached, returning empty string")
                    return ""
                print("\nInput interrupted. Please try again.")
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Unexpected error in get_input: {str(e)}")
                return ""
        
        return ""
    
    def get_menu_choice(self, max_options: int) -> Optional[int]:
        """Get menu choice with validation"""
        if self.logger:
            self.logger.debug("get_menu_choice called", {
                "max_options": max_options
            })
        
        while True:
            try:
                choice = input(f"Choose an option (1-{max_options}): ").strip()
                
                if choice.isdigit():
                    option_number = int(choice)
                    if 1 <= option_number <= max_options:
                        if self.logger:
                            self.logger.debug(f"Valid menu option selected: {option_number}")
                        return option_number  # Return 1-based index
                    else:
                        if self.logger:
                            self.logger.warning(f"Option number {option_number} out of range (1-{max_options})")
                        print(f"Please enter a number between 1 and {max_options}")
                elif choice.lower() in ['quit', 'exit', 'q']:
                    if self.logger:
                        self.logger.debug("User chose to quit/exit")
                    return None
                else:
                    if self.logger:
                        self.logger.warning(f"Invalid menu choice: '{choice}'")
                    print("Please enter a valid option number")
                    
            except (KeyboardInterrupt, EOFError) as e:
                if self.logger:
                    self.logger.warning(f"Input interrupted: {type(e).__name__}")
                return None
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Unexpected error in get_menu_choice: {str(e)}", {
                        "exception_type": type(e).__name__,
                        "choice": choice if 'choice' in locals() else None
                    })
                return None
    
    def get_yes_no(self, prompt: str = "Continue? (y/n): ") -> bool:
        """Get yes/no response from user"""
        while True:
            try:
                response = input(prompt).strip().lower()
                
                if response in self.valid_yes_responses:
                    return True
                elif response in self.valid_no_responses:
                    return False
                else:
                    print("Please enter 'y' for yes or 'n' for no")
                    
            except (KeyboardInterrupt, EOFError):
                return False
    
    def get_integer(self, prompt: str = "Enter number: ", min_val: int = None, max_val: int = None) -> Optional[int]:
        """Get integer input with optional range validation"""
        while True:
            try:
                value = input(prompt).strip()
                
                if not value:
                    continue
                
                number = int(value)
                
                if min_val is not None and number < min_val:
                    print(f"Number must be at least {min_val}")
                    continue
                
                if max_val is not None and number > max_val:
                    print(f"Number must be at most {max_val}")
                    continue
                
                return number
                
            except (KeyboardInterrupt, EOFError):
                return None
            except ValueError:
                print("Please enter a valid number")
    
    def get_string(self, prompt: str = "Enter text: ", min_length: int = 1, max_length: int = 50, 
                   allow_empty: bool = False) -> Optional[str]:
        """Get string input with length validation"""
        while True:
            try:
                text = input(prompt).strip()
                
                if not text and allow_empty:
                    return text
                
                if len(text) < min_length:
                    print(f"Text must be at least {min_length} characters long")
                    continue
                
                if len(text) > max_length:
                    print(f"Text must be no more than {max_length} characters long")
                    continue
                
                return text
                
            except (KeyboardInterrupt, EOFError):
                return None
    
    def get_trainer_name(self) -> str:
        """Get trainer name with validation"""
        while True:
            name = self.get_string("Enter your trainer name: ", min_length=1, max_length=12)
            
            if name is None:
                return "Red"  # Default name
            
            # Check for valid characters (letters, numbers, spaces, some symbols)
            if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name):
                return name
            else:
                print("Name can only contain letters, numbers, spaces, hyphens, underscores, and periods")
    
    def get_pokemon_nickname(self, species: str) -> str:
        """Get Pokemon nickname with validation"""
        prompt = f"Give {species} a nickname (or press Enter to keep '{species}'): "
        nickname = self.get_string(prompt, min_length=1, max_length=12, allow_empty=True)
        
        if not nickname:
            return species
        
        # Check for valid characters
        if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', nickname):
            return nickname
        else:
            print("Nickname can only contain letters, numbers, spaces, hyphens, underscores, and periods")
            return species
    
    def get_direction(self, prompt: str = "Which direction? (north/south/east/west): ") -> Optional[str]:
        """Get movement direction"""
        valid_directions = {
            'n': 'north', 'north': 'north', 'up': 'north',
            's': 'south', 'south': 'south', 'down': 'south',
            'e': 'east', 'east': 'east', 'right': 'east',
            'w': 'west', 'west': 'west', 'left': 'west'
        }
        
        while True:
            try:
                direction = input(prompt).strip().lower()
                
                if direction in valid_directions:
                    return valid_directions[direction]
                elif direction in ['quit', 'exit', 'cancel']:
                    return None
                else:
                    print("Please enter: north, south, east, west (or n/s/e/w)")
                    
            except (KeyboardInterrupt, EOFError):
                return None
    
    def get_battle_choice(self) -> Optional[int]:
        """Get battle menu choice"""
        if self.logger:
            self.logger.debug("get_battle_choice called")
            
        valid_choices = {
            '1': 1, 'attack': 1, 'a': 1,
            '2': 2, 'items': 2, 'i': 2, 'item': 2,
            '3': 3, 'pokemon': 3, 'p': 3, 'switch': 3,
            '4': 4, 'run': 4, 'r': 4, 'flee': 4
        }
        
        while True:
            try:
                choice = input("What will you do? ").strip().lower()
                
                if choice in valid_choices:
                    result = valid_choices[choice]
                    if self.logger:
                        self.logger.debug(f"Valid choice selected: {choice} -> {result}")
                    return result
                elif choice in ['quit', 'exit']:
                    if self.logger:
                        self.logger.debug("User chose to quit/exit, returning 4 (Run)")
                    return 4  # Run
                else:
                    if self.logger:
                        self.logger.warning(f"Invalid choice entered: '{choice}'")
                    print("Please choose: 1-Attack, 2-Items, 3-Pokemon, 4-Run")
                    
            except (KeyboardInterrupt, EOFError) as e:
                if self.logger:
                    self.logger.warning(f"Input interrupted: {type(e).__name__}")
                return 4  # Run
    
    def get_move_choice(self, pokemon) -> Optional[int]:
        """Get move choice for battle"""
        from game.pokemon import Pokemon
        
        if self.logger:
            self.logger.debug("get_move_choice called", {
                "pokemon_species": getattr(pokemon, 'species', 'Unknown'),
                "pokemon_type": type(pokemon).__name__
            })
        
        if not isinstance(pokemon, Pokemon):
            if self.logger:
                self.logger.error("Invalid pokemon object passed to get_move_choice", {
                    "pokemon_type": type(pokemon).__name__,
                    "pokemon_value": str(pokemon)
                })
            return None
        
        max_moves = len(pokemon.moves)
        if self.logger:
            self.logger.debug(f"Pokemon has {max_moves} moves available")
        
        while True:
            try:
                choice = input(f"Choose a move (1-{max_moves}): ").strip()
                
                if choice.isdigit():
                    move_number = int(choice)
                    if 1 <= move_number <= max_moves:
                        # Check if move has PP
                        move = pokemon.moves[move_number - 1]
                        if self.logger:
                            self.logger.debug(f"Checking move: {move.name}, PP: {move.pp}/{move.max_pp}")
                            
                        if move.pp > 0:
                            if self.logger:
                                self.logger.debug(f"Valid move selected: {move.name} (choice {move_number})")
                            return move_number  # Return 1-based index
                        else:
                            if self.logger:
                                self.logger.warning(f"Move {move.name} has no PP left")
                            print(f"{move.name} has no PP left!")
                            continue
                    else:
                        if self.logger:
                            self.logger.warning(f"Move number {move_number} out of range (1-{max_moves})")
                        print(f"Please enter a number between 1 and {max_moves}")
                elif choice.lower() in ['back', 'cancel']:
                    if self.logger:
                        self.logger.debug("User chose to go back/cancel")
                    return None
                else:
                    if self.logger:
                        self.logger.warning(f"Invalid move choice: '{choice}'")
                    print("Please enter a valid move number")
                    
            except (KeyboardInterrupt, EOFError) as e:
                if self.logger:
                    self.logger.warning(f"Input interrupted: {type(e).__name__}")
                return None
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Unexpected error in get_move_choice: {str(e)}", {
                        "exception_type": type(e).__name__,
                        "choice": choice if 'choice' in locals() else None
                    })
                return None
    
    def get_item_choice(self, items: dict) -> Optional[str]:
        """Get item choice from inventory"""
        if not items:
            return None
        
        item_list = list(items.keys())
        max_items = len(item_list)
        
        while True:
            try:
                choice = input(f"Choose an item (1-{max_items}): ").strip()
                
                if choice.isdigit():
                    item_index = int(choice) - 1
                    if 0 <= item_index < max_items:
                        return item_list[item_index]
                    else:
                        print(f"Please enter a number between 1 and {max_items}")
                elif choice.lower() in ['back', 'cancel']:
                    return None
                else:
                    print("Please enter a valid item number")
                    
            except (KeyboardInterrupt, EOFError):
                return None
    
    def get_pokemon_choice(self, pokemon_list) -> Optional[int]:
        """Get Pokemon choice for switching"""
        if self.logger:
            self.logger.debug("get_pokemon_choice called", {
                "pokemon_count": len(pokemon_list) if pokemon_list else 0,
                "pokemon_list_type": type(pokemon_list).__name__
            })
        
        if not pokemon_list:
            if self.logger:
                self.logger.error("Empty pokemon list passed to get_pokemon_choice")
            return None
        
        max_pokemon = len(pokemon_list)
        
        while True:
            try:
                choice = input(f"Choose a Pokemon (1-{max_pokemon}): ").strip()
                
                if choice.isdigit():
                    pokemon_number = int(choice)
                    if 1 <= pokemon_number <= max_pokemon:
                        # Check if Pokemon is alive - use current_hp instead of hp
                        pokemon = pokemon_list[pokemon_number - 1]
                        
                        if pokemon.current_hp > 0:
                            if self.logger:
                                self.logger.debug(f"Valid Pokemon selected: {pokemon.species} (choice {pokemon_number})")
                            return pokemon_number  # Return 1-based index
                        else:
                            if self.logger:
                                self.logger.warning(f"Pokemon {pokemon.species} has no HP left")
                            print(f"{pokemon.species} has no HP left!")
                            continue
                    else:
                        if self.logger:
                            self.logger.warning(f"Pokemon number {pokemon_number} out of range (1-{max_pokemon})")
                        print(f"Please enter a number between 1 and {max_pokemon}")
                elif choice.lower() in ['back', 'cancel']:
                    if self.logger:
                        self.logger.debug("User chose to go back/cancel")
                    return None
                else:
                    if self.logger:
                        self.logger.warning(f"Invalid Pokemon choice: '{choice}'")
                    print("Please enter a valid Pokemon number")
                    
            except (KeyboardInterrupt, EOFError) as e:
                if self.logger:
                    self.logger.warning(f"Input interrupted: {type(e).__name__}")
                return None
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Unexpected error in get_pokemon_choice: {str(e)}", {
                        "exception_type": type(e).__name__,
                        "choice": choice if 'choice' in locals() else None
                    })
                return None
    
    def get_shop_choice(self, shop_items: dict) -> Optional[str]:
        """Get shop item choice"""
        if not shop_items:
            return "quit"
        
        item_list = list(shop_items.keys())
        max_items = len(item_list)
        
        while True:
            try:
                choice = input().strip()
                
                if choice == '0':
                    return "quit"
                elif choice.isdigit():
                    item_index = int(choice) - 1
                    if 0 <= item_index < max_items:
                        return item_list[item_index]
                    else:
                        print(f"Please enter a number between 1 and {max_items} (or 0 to exit)")
                else:
                    print("Please enter a valid item number")
                    
            except (KeyboardInterrupt, EOFError):
                return "quit"
    
    def get_quantity(self, item_name: str, max_quantity: int = 99) -> int:
        """Get quantity for item purchase/use"""
        while True:
            try:
                quantity = input(f"How many {item_name}? (max {max_quantity}): ").strip()
                
                if quantity.isdigit():
                    qty = int(quantity)
                    if 1 <= qty <= max_quantity:
                        return qty
                    else:
                        print(f"Please enter a number between 1 and {max_quantity}")
                else:
                    print("Please enter a valid number")
                    
            except (KeyboardInterrupt, EOFError):
                return 1
    
    def get_starter_choice(self) -> Optional[str]:
        """Get starter Pokemon choice"""
        starters = {
            '1': 'Bulbasaur',
            '2': 'Charmander', 
            '3': 'Squirtle'
        }
        
        while True:
            try:
                print("\nChoose your starter Pokemon:")
                print("1. Bulbasaur (Grass/Poison)")
                print("2. Charmander (Fire)")
                print("3. Squirtle (Water)")
                
                choice = input("Enter your choice (1-3): ").strip()
                
                if choice in starters:
                    return starters[choice]
                else:
                    print("Please enter 1, 2, or 3")
                    
            except (KeyboardInterrupt, EOFError):
                return None
    
    def get_gender_choice(self) -> str:
        """Get trainer gender choice"""
        while True:
            try:
                print("\nChoose your gender:")
                print("1. Male")
                print("2. Female")
                
                choice = input("Enter your choice (1-2): ").strip()
                
                if choice == '1':
                    return "Male"
                elif choice == '2':
                    return "Female"
                else:
                    print("Please enter 1 or 2")
                    
            except (KeyboardInterrupt, EOFError):
                return "Male"  # Default
    
    def wait_for_input(self, prompt: str = "Press Enter to continue..."):
        """Wait for user to press Enter"""
        try:
            input(prompt)
        except (KeyboardInterrupt, EOFError):
            pass
    
    def confirm_action(self, action: str) -> bool:
        """Confirm an action with the user"""
        return self.get_yes_no(f"Are you sure you want to {action}? (y/n): ")
    
    def get_save_name(self) -> str:
        """Get save file name"""
        while True:
            name = self.get_string("Enter save file name: ", min_length=1, max_length=20)
            
            if name is None:
                return "default"
            
            # Check for valid filename characters
            if re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name):
                return name
            else:
                print("Save name can only contain letters, numbers, spaces, hyphens, underscores, and periods")
    
    def get_command(self, prompt: str = "> ") -> List[str]:
        """Get command input and split into words"""
        try:
            command = input(prompt).strip().lower()
            return command.split() if command else []
        except (KeyboardInterrupt, EOFError):
            return []
    
    def parse_command(self, command: str) -> tuple:
        """Parse a command string into action and target"""
        words = command.strip().lower().split()
        
        if not words:
            return None, None
        
        action = words[0]
        target = " ".join(words[1:]) if len(words) > 1 else None
        
        return action, target
    
    def validate_name(self, name: str) -> bool:
        """Validate a name string"""
        if not name or len(name) < 1 or len(name) > 12:
            return False
        
        return re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name) is not None 