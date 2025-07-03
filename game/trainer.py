"""
Trainer class and related functionality
"""

import random
from typing import List, Dict, Optional
from datetime import datetime
from .pokemon import Pokemon, PokemonType

class Item:
    """Represents an item in the game"""
    def __init__(self, name: str, description: str, item_type: str, effect: str = None):
        self.name = name
        self.description = description
        self.item_type = item_type  # pokeball, healing, evolution, key, misc
        self.effect = effect

class Inventory:
    """Manages trainer's inventory"""
    def __init__(self):
        self.items: Dict[str, int] = {}
        self.key_items: List[str] = []
        
        # Start with basic items
        self.add_item("Pokeball", 10)
        self.add_item("Potion", 5)
        
    def add_item(self, item_name: str, quantity: int = 1):
        """Add items to inventory"""
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove items from inventory"""
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
            return True
        return False
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """Check if inventory has specific item"""
        return self.items.get(item_name, 0) >= quantity
    
    def get_items_by_type(self, item_type: str) -> Dict[str, int]:
        """Get items of specific type"""
        item_database = self.get_item_database()
        return {name: qty for name, qty in self.items.items() 
                if item_database.get(name, {}).get('type') == item_type}
    
    def get_all_items(self) -> Dict[str, int]:
        """Get all items in inventory"""
        return self.items.copy()
    
    def get_item_database(self) -> Dict[str, Dict]:
        """Get item database"""
        return {
            "Pokeball": {"type": "pokeball", "description": "A device for catching wild Pokemon", "catch_rate": 1.0},
            "Great Ball": {"type": "pokeball", "description": "A good, high-performance Ball", "catch_rate": 1.5},
            "Ultra Ball": {"type": "pokeball", "description": "An ultra-high performance Ball", "catch_rate": 2.0},
            "Master Ball": {"type": "pokeball", "description": "The best Ball with the ultimate level of performance", "catch_rate": 255.0},
            "Potion": {"type": "healing", "description": "Restores 20 HP", "heal_amount": 20},
            "Super Potion": {"type": "healing", "description": "Restores 50 HP", "heal_amount": 50},
            "Hyper Potion": {"type": "healing", "description": "Restores 200 HP", "heal_amount": 200},
            "Max Potion": {"type": "healing", "description": "Fully restores HP", "heal_amount": 999},
            "Revive": {"type": "healing", "description": "Revives a fainted Pokemon with half HP", "revive": True},
            "Thunder Stone": {"type": "evolution", "description": "Makes certain Pokemon evolve"},
            "Fire Stone": {"type": "evolution", "description": "Makes certain Pokemon evolve"},
            "Water Stone": {"type": "evolution", "description": "Makes certain Pokemon evolve"},
            "Leaf Stone": {"type": "evolution", "description": "Makes certain Pokemon evolve"},
            "Rare Candy": {"type": "misc", "description": "Raises a Pokemon's level by 1"},
            "Bicycle": {"type": "key", "description": "Allows faster travel"},
            "Pokedex": {"type": "key", "description": "Records data on Pokemon"}
        }

class Badge:
    """Represents a gym badge"""
    def __init__(self, name: str, gym_leader: str, location: str, date_earned: datetime = None):
        self.name = name
        self.gym_leader = gym_leader
        self.location = location
        self.date_earned = date_earned or datetime.now()

class Trainer:
    """Main trainer class"""
    def __init__(self, name: str = "Red"):
        self.name = name
        self.level = 1
        self.experience = 0
        self.money = 3000  # Starting money
        self.current_location = "pallet_town"  # Use location key, not display name
        self.home_location = "pallet_town"
        
        # Pokemon team and storage
        self.pokemon_team: List[Pokemon] = []
        self.pokemon_box: List[Pokemon] = []  # PC storage
        self.max_team_size = 6
        
        # Inventory and items
        self.inventory = Inventory()
        self.badges: List[Badge] = []
        
        # Pokedex
        self.pokedex_seen: set = set()
        self.pokedex_caught: set = set()
        
        # Game progress
        self.story_flags: Dict[str, bool] = {}
        self.visited_locations: set = {self.current_location}
        
        # Statistics
        self.stats = {
            "pokemon_caught": 0,
            "battles_won": 0,
            "battles_lost": 0,
            "steps_taken": 0,
            "play_time": 0,  # in minutes
            "gyms_defeated": 0,
            "pokemon_evolved": 0,
            "items_used": 0
        }
        
        # Trainer customization
        self.gender = "Male"
        self.appearance = "A young Pokemon trainer"
        self.trainer_id = random.randint(10000, 99999)
        
        # Game settings
        self.settings = {
            "battle_animations": True,
            "auto_save": True,
            "text_speed": "Normal"
        }
    
    def add_pokemon(self, pokemon: Pokemon, caught: bool = False) -> bool:
        """Add Pokemon to team or box"""
        if caught:
            pokemon.original_trainer = self.name
            pokemon.catch_location = self.current_location
            self.stats["pokemon_caught"] += 1
            self.pokedex_caught.add(pokemon.species)
        
        self.pokedex_seen.add(pokemon.species)
        
        if len(self.pokemon_team) < self.max_team_size:
            self.pokemon_team.append(pokemon)
            return True
        else:
            self.pokemon_box.append(pokemon)
            return False  # Sent to box
    
    def remove_pokemon(self, pokemon: Pokemon) -> bool:
        """Remove Pokemon from team"""
        if pokemon in self.pokemon_team:
            self.pokemon_team.remove(pokemon)
            return True
        return False
    
    def get_active_pokemon(self) -> Optional[Pokemon]:
        """Get first non-fainted Pokemon"""
        for pokemon in self.pokemon_team:
            if not pokemon.is_fainted():
                return pokemon
        return None
    
    def has_usable_pokemon(self) -> bool:
        """Check if trainer has any non-fainted Pokemon"""
        return any(not pokemon.is_fainted() for pokemon in self.pokemon_team)
    
    def heal_all_pokemon(self):
        """Heal all Pokemon in team"""
        for pokemon in self.pokemon_team:
            pokemon.heal()
    
    def add_money(self, amount: int):
        """Add money to trainer"""
        self.money += amount
    
    def spend_money(self, amount: int) -> bool:
        """Spend money if trainer has enough"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def earn_badge(self, badge_name: str, gym_leader: str, location: str):
        """Earn a gym badge"""
        badge = Badge(badge_name, gym_leader, location)
        self.badges.append(badge)
        self.stats["gyms_defeated"] += 1
    
    def has_badge(self, badge_name: str) -> bool:
        """Check if trainer has specific badge"""
        return any(badge.name == badge_name for badge in self.badges)
    
    def get_badge_count(self) -> int:
        """Get number of badges earned"""
        return len(self.badges)
    
    def gain_experience(self, amount: int):
        """Gain trainer experience"""
        self.experience += amount
        
        # Check for level up
        exp_needed = self.level * 100
        if self.experience >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """Level up the trainer"""
        self.level += 1
        self.experience = 0
        
        # Unlock features based on level
        if self.level == 5:
            self.story_flags["can_use_pc"] = True
        elif self.level == 10:
            self.story_flags["can_trade"] = True
    
    def move_to_location(self, location: str):
        """Move trainer to new location"""
        self.current_location = location
        self.visited_locations.add(location)
        self.stats["steps_taken"] += 1
    
    def use_item(self, item_name: str, target_pokemon: Pokemon = None) -> bool:
        """Use an item"""
        if not self.inventory.has_item(item_name):
            return False
        
        item_database = self.inventory.get_item_database()
        item_data = item_database.get(item_name)
        
        if not item_data:
            return False
        
        # Handle different item types
        if item_data["type"] == "healing" and target_pokemon:
            if "heal_amount" in item_data:
                if item_data["heal_amount"] == 999:
                    target_pokemon.heal()
                else:
                    target_pokemon.heal(item_data["heal_amount"])
            elif item_data.get("revive") and target_pokemon.is_fainted():
                target_pokemon.current_hp = target_pokemon.max_hp // 2
            
            self.inventory.remove_item(item_name)
            self.stats["items_used"] += 1
            return True
        
        elif item_data["type"] == "misc" and item_name == "Rare Candy" and target_pokemon:
            target_pokemon.gain_experience(target_pokemon.experience_to_next_level)
            self.inventory.remove_item(item_name)
            self.stats["items_used"] += 1
            return True
        
        return False
    
    def catch_pokemon(self, wild_pokemon: Pokemon, pokeball_type: str = "Pokeball") -> bool:
        """Attempt to catch a wild Pokemon"""
        if not self.inventory.has_item(pokeball_type):
            return False
        
        # Calculate catch probability
        item_database = self.inventory.get_item_database()
        ball_modifier = item_database.get(pokeball_type, {}).get("catch_rate", 1.0)
        
        # Base catch rate calculation
        catch_rate = wild_pokemon.get_catch_rate()
        hp_modifier = (3 * wild_pokemon.max_hp - 2 * wild_pokemon.current_hp) / (3 * wild_pokemon.max_hp)
        
        # Status condition bonus
        status_modifier = 1.0
        if wild_pokemon.status_condition in ["sleep", "freeze"]:
            status_modifier = 2.0
        elif wild_pokemon.status_condition in ["paralyze", "burn", "poison"]:
            status_modifier = 1.5
        
        # Final catch probability
        catch_probability = (catch_rate * ball_modifier * hp_modifier * status_modifier) / 255
        catch_probability = min(1.0, catch_probability)
        
        # Use the pokeball
        self.inventory.remove_item(pokeball_type)
        
        # Determine if catch is successful
        if random.random() < catch_probability:
            # Successful catch
            wild_pokemon.heal()  # Heal the caught Pokemon
            in_team = self.add_pokemon(wild_pokemon, caught=True)
            return True
        
        return False
    
    def get_pokedex_completion(self) -> float:
        """Get Pokedex completion percentage"""
        total_pokemon = 151  # Original 151 Pokemon
        return (len(self.pokedex_caught) / total_pokemon) * 100
    
    def get_team_info(self) -> List[Dict]:
        """Get information about Pokemon team"""
        return [pokemon.get_info() for pokemon in self.pokemon_team]
    
    def get_save_data(self) -> Dict:
        """Get data for saving the game"""
        return {
            "trainer_name": self.name,
            "trainer_level": self.level,
            "experience": self.experience,
            "money": self.money,
            "current_location": self.current_location,
            "home_location": self.home_location,
            "pokemon_team": [self.pokemon_to_dict(p) for p in self.pokemon_team],
            "pokemon_box": [self.pokemon_to_dict(p) for p in self.pokemon_box],
            "inventory": self.inventory.items,
            "badges": [{"name": b.name, "gym_leader": b.gym_leader, "location": b.location} for b in self.badges],
            "pokedex_seen": list(self.pokedex_seen),
            "pokedex_caught": list(self.pokedex_caught),
            "story_flags": self.story_flags,
            "visited_locations": list(self.visited_locations),
            "stats": self.stats,
            "gender": self.gender,
            "appearance": self.appearance,
            "trainer_id": self.trainer_id,
            "settings": self.settings
        }
    
    def pokemon_to_dict(self, pokemon: Pokemon) -> Dict:
        """Convert Pokemon to dictionary for saving"""
        return {
            "species": pokemon.species,
            "nickname": pokemon.nickname,
            "level": pokemon.level,
            "experience": pokemon.experience,
            "current_hp": pokemon.current_hp,
            "max_hp": pokemon.max_hp,
            "is_shiny": pokemon.is_shiny,
            "nature": pokemon.nature,
            "friendship": pokemon.friendship,
            "moves": [{"name": m.name, "pp": m.pp} for m in pokemon.moves],
            "status_condition": pokemon.status_condition,
            "original_trainer": pokemon.original_trainer,
            "catch_location": pokemon.catch_location,
            "catch_level": pokemon.catch_level
        }
    
    def load_from_save_data(self, save_data: Dict):
        """Load trainer from save data"""
        self.name = save_data.get("trainer_name", "Red")
        self.level = save_data.get("trainer_level", 1)
        self.experience = save_data.get("experience", 0)
        self.money = save_data.get("money", 3000)
        self.current_location = save_data.get("current_location", "pallet_town")
        self.home_location = save_data.get("home_location", "pallet_town")
        
        # Load Pokemon team
        self.pokemon_team = []
        for pokemon_data in save_data.get("pokemon_team", []):
            pokemon = self.dict_to_pokemon(pokemon_data)
            self.pokemon_team.append(pokemon)
        
        # Load Pokemon box
        self.pokemon_box = []
        for pokemon_data in save_data.get("pokemon_box", []):
            pokemon = self.dict_to_pokemon(pokemon_data)
            self.pokemon_box.append(pokemon)
        
        # Load inventory
        self.inventory.items = save_data.get("inventory", {})
        
        # Load badges
        self.badges = []
        for badge_data in save_data.get("badges", []):
            badge = Badge(badge_data["name"], badge_data["gym_leader"], badge_data["location"])
            self.badges.append(badge)
        
        # Load other data
        self.pokedex_seen = set(save_data.get("pokedex_seen", []))
        self.pokedex_caught = set(save_data.get("pokedex_caught", []))
        self.story_flags = save_data.get("story_flags", {})
        self.visited_locations = set(save_data.get("visited_locations", [self.current_location]))
        self.stats = save_data.get("stats", self.stats)
        self.gender = save_data.get("gender", "Male")
        self.appearance = save_data.get("appearance", "A young Pokemon trainer")
        self.trainer_id = save_data.get("trainer_id", random.randint(10000, 99999))
        self.settings = save_data.get("settings", self.settings)
    
    def dict_to_pokemon(self, pokemon_data: Dict) -> Pokemon:
        """Convert dictionary to Pokemon object"""
        pokemon = Pokemon(pokemon_data["species"], pokemon_data["level"], pokemon_data.get("is_shiny", False))
        pokemon.nickname = pokemon_data.get("nickname", pokemon.species)
        pokemon.experience = pokemon_data.get("experience", 0)
        pokemon.current_hp = pokemon_data.get("current_hp", pokemon.max_hp)
        pokemon.nature = pokemon_data.get("nature", pokemon.nature)
        pokemon.friendship = pokemon_data.get("friendship", 70)
        pokemon.status_condition = pokemon_data.get("status_condition")
        pokemon.original_trainer = pokemon_data.get("original_trainer")
        pokemon.catch_location = pokemon_data.get("catch_location")
        pokemon.catch_level = pokemon_data.get("catch_level", pokemon.level)
        
        # Restore move PP
        move_data = pokemon_data.get("moves", [])
        for i, move in enumerate(pokemon.moves):
            if i < len(move_data):
                move.pp = move_data[i].get("pp", move.max_pp)
        
        return pokemon
    
    def __str__(self) -> str:
        return f"Trainer {self.name} (Lv.{self.level}) - {len(self.pokemon_team)} Pokemon - {self.get_badge_count()} Badges" 