"""
Pokemon class and related functionality
"""

import random
import json
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

class PokemonType(Enum):
    """Pokemon types with their strengths and weaknesses"""
    NORMAL = "Normal"
    FIRE = "Fire"
    WATER = "Water"
    ELECTRIC = "Electric"
    GRASS = "Grass"
    ICE = "Ice"
    FIGHTING = "Fighting"
    POISON = "Poison"
    GROUND = "Ground"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    BUG = "Bug"
    ROCK = "Rock"
    GHOST = "Ghost"
    DRAGON = "Dragon"
    DARK = "Dark"
    STEEL = "Steel"
    FAIRY = "Fairy"

@dataclass
class Move:
    """Represents a Pokemon move"""
    name: str
    type: PokemonType
    power: int
    accuracy: int
    pp: int
    max_pp: int
    description: str
    effect: Optional[str] = None
    
    def use_move(self) -> bool:
        """Use the move, reducing PP"""
        if self.pp > 0:
            self.pp -= 1
            return True
        return False
    
    def restore_pp(self, amount: int = None):
        """Restore PP to the move"""
        if amount is None:
            self.pp = self.max_pp
        else:
            self.pp = min(self.max_pp, self.pp + amount)

@dataclass
class Stats:
    """Pokemon base stats"""
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int
    
    def calculate_stat(self, base_stat: int, level: int, iv: int = 15) -> int:
        """Calculate actual stat value based on level and IV"""
        return int(((2 * base_stat + iv) * level) / 100) + 5

class Pokemon:
    """Main Pokemon class"""
    
    # Type effectiveness chart
    TYPE_EFFECTIVENESS = {
        PokemonType.FIRE: {
            PokemonType.GRASS: 2.0, PokemonType.ICE: 2.0, PokemonType.BUG: 2.0, PokemonType.STEEL: 2.0,
            PokemonType.FIRE: 0.5, PokemonType.WATER: 0.5, PokemonType.ROCK: 0.5, PokemonType.DRAGON: 0.5
        },
        PokemonType.WATER: {
            PokemonType.FIRE: 2.0, PokemonType.GROUND: 2.0, PokemonType.ROCK: 2.0,
            PokemonType.WATER: 0.5, PokemonType.GRASS: 0.5, PokemonType.DRAGON: 0.5
        },
        PokemonType.ELECTRIC: {
            PokemonType.WATER: 2.0, PokemonType.FLYING: 2.0,
            PokemonType.ELECTRIC: 0.5, PokemonType.GRASS: 0.5, PokemonType.DRAGON: 0.5,
            PokemonType.GROUND: 0.0
        },
        PokemonType.GRASS: {
            PokemonType.WATER: 2.0, PokemonType.GROUND: 2.0, PokemonType.ROCK: 2.0,
            PokemonType.FIRE: 0.5, PokemonType.GRASS: 0.5, PokemonType.POISON: 0.5, 
            PokemonType.FLYING: 0.5, PokemonType.BUG: 0.5, PokemonType.DRAGON: 0.5, PokemonType.STEEL: 0.5
        },
        # Add more type effectiveness as needed
    }
    
    def __init__(self, species: str, level: int = 1, is_shiny: bool = False):
        self.species = species
        self.level = level
        self.is_shiny = is_shiny
        self.nickname = species
        self.experience = 0
        self.experience_to_next_level = self.calculate_exp_to_next_level()
        
        # Get species data
        self.species_data = self.get_species_data(species)
        self.types = self.species_data["types"]
        self.base_stats = Stats(**self.species_data["base_stats"])
        
        # Calculate actual stats
        self.max_hp = self.base_stats.calculate_stat(self.base_stats.hp, level)
        self.current_hp = self.max_hp
        self.attack = self.base_stats.calculate_stat(self.base_stats.attack, level)
        self.defense = self.base_stats.calculate_stat(self.base_stats.defense, level)
        self.special_attack = self.base_stats.calculate_stat(self.base_stats.special_attack, level)
        self.special_defense = self.base_stats.calculate_stat(self.base_stats.special_defense, level)
        self.speed = self.base_stats.calculate_stat(self.base_stats.speed, level)
        
        # Status conditions
        self.status_condition = None
        self.status_turns = 0
        
        # Moves
        self.moves = self.get_initial_moves()
        
        # Battle stats (temporary modifiers)
        self.attack_modifier = 0
        self.defense_modifier = 0
        self.speed_modifier = 0
        
        # Friendship and other attributes
        self.friendship = 70
        self.nature = self.get_random_nature()
        self.ability = self.species_data.get("abilities", ["None"])[0]
        
        # Catch information
        self.original_trainer = None
        self.catch_location = None
        self.catch_level = level
        
    def get_species_data(self, species: str) -> Dict:
        """Get species data from Pokemon database"""
        # This would normally load from a JSON file
        pokemon_data = {
            "Bulbasaur": {
                "types": [PokemonType.GRASS, PokemonType.POISON],
                "base_stats": {"hp": 45, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45},
                "abilities": ["Overgrow"],
                "evolution": {"level": 16, "evolves_to": "Ivysaur"}
            },
            "Charmander": {
                "types": [PokemonType.FIRE],
                "base_stats": {"hp": 39, "attack": 52, "defense": 43, "special_attack": 60, "special_defense": 50, "speed": 65},
                "abilities": ["Blaze"],
                "evolution": {"level": 16, "evolves_to": "Charmeleon"}
            },
            "Squirtle": {
                "types": [PokemonType.WATER],
                "base_stats": {"hp": 44, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43},
                "abilities": ["Torrent"],
                "evolution": {"level": 16, "evolves_to": "Wartortle"}
            },
            "Pikachu": {
                "types": [PokemonType.ELECTRIC],
                "base_stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                "abilities": ["Static"],
                "evolution": {"item": "Thunder Stone", "evolves_to": "Raichu"}
            },
            "Rattata": {
                "types": [PokemonType.NORMAL],
                "base_stats": {"hp": 30, "attack": 56, "defense": 35, "special_attack": 25, "special_defense": 35, "speed": 72},
                "abilities": ["Run Away", "Guts"],
                "evolution": {"level": 20, "evolves_to": "Raticate"}
            },
            "Caterpie": {
                "types": [PokemonType.BUG],
                "base_stats": {"hp": 45, "attack": 30, "defense": 35, "special_attack": 20, "special_defense": 20, "speed": 45},
                "abilities": ["Shield Dust"],
                "evolution": {"level": 7, "evolves_to": "Metapod"}
            },
            "Pidgey": {
                "types": [PokemonType.NORMAL, PokemonType.FLYING],
                "base_stats": {"hp": 40, "attack": 45, "defense": 40, "special_attack": 35, "special_defense": 35, "speed": 56},
                "abilities": ["Keen Eye", "Tangled Feet"],
                "evolution": {"level": 18, "evolves_to": "Pidgeotto"}
            }
        }
        
        return pokemon_data.get(species, {
            "types": [PokemonType.NORMAL],
            "base_stats": {"hp": 50, "attack": 50, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 50},
            "abilities": ["Unknown"]
        })
    
    def get_initial_moves(self) -> List[Move]:
        """Get initial moves for the Pokemon"""
        move_database = {
            "Tackle": Move("Tackle", PokemonType.NORMAL, 40, 100, 35, 35, "A physical attack in which the user charges and slams into the target."),
            "Growl": Move("Growl", PokemonType.NORMAL, 0, 100, 40, 40, "The user growls in an endearing way, making opposing Pokemon less wary."),
            "Vine Whip": Move("Vine Whip", PokemonType.GRASS, 45, 100, 25, 25, "The target is struck with slender, whiplike vines."),
            "Ember": Move("Ember", PokemonType.FIRE, 40, 100, 25, 25, "The target is attacked with small flames."),
            "Water Gun": Move("Water Gun", PokemonType.WATER, 40, 100, 25, 25, "The target is blasted with a forceful shot of water."),
            "Thunder Shock": Move("Thunder Shock", PokemonType.ELECTRIC, 40, 100, 30, 30, "A jolt of electricity crashes down on the target."),
            "Quick Attack": Move("Quick Attack", PokemonType.NORMAL, 40, 100, 30, 30, "The user lunges at the target at a speed that makes it almost invisible."),
            "String Shot": Move("String Shot", PokemonType.BUG, 0, 95, 40, 40, "The opposing Pokemon are bound with silk blown from the user's mouth."),
            "Gust": Move("Gust", PokemonType.FLYING, 40, 100, 35, 35, "A gust of wind is whipped up by wings and launched at the target.")
        }
        
        # Assign moves based on species
        species_moves = {
            "Bulbasaur": ["Tackle", "Growl", "Vine Whip"],
            "Charmander": ["Tackle", "Growl", "Ember"],
            "Squirtle": ["Tackle", "Water Gun"],
            "Pikachu": ["Thunder Shock", "Quick Attack"],
            "Rattata": ["Tackle", "Quick Attack"],
            "Caterpie": ["Tackle", "String Shot"],
            "Pidgey": ["Tackle", "Gust"]
        }
        
        move_names = species_moves.get(self.species, ["Tackle"])
        return [move_database[name] for name in move_names if name in move_database]
    
    def get_random_nature(self) -> str:
        """Get a random nature for the Pokemon"""
        natures = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax",
                  "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash",
                  "Calm", "Gentle", "Sassy", "Careful", "Quirky"]
        return random.choice(natures)
    
    def calculate_exp_to_next_level(self) -> int:
        """Calculate experience needed to reach next level"""
        return int(1.2 * (self.level ** 2))
    
    def gain_experience(self, amount: int) -> bool:
        """Gain experience and check for level up"""
        self.experience += amount
        
        if self.experience >= self.experience_to_next_level:
            return self.level_up()
        return False
    
    def level_up(self) -> bool:
        """Level up the Pokemon"""
        if self.level >= 100:
            return False
            
        self.level += 1
        self.experience = 0
        self.experience_to_next_level = self.calculate_exp_to_next_level()
        
        # Recalculate stats
        old_max_hp = self.max_hp
        self.max_hp = self.base_stats.calculate_stat(self.base_stats.hp, self.level)
        self.current_hp += (self.max_hp - old_max_hp)  # Heal proportionally
        
        self.attack = self.base_stats.calculate_stat(self.base_stats.attack, self.level)
        self.defense = self.base_stats.calculate_stat(self.base_stats.defense, self.level)
        self.special_attack = self.base_stats.calculate_stat(self.base_stats.special_attack, self.level)
        self.special_defense = self.base_stats.calculate_stat(self.base_stats.special_defense, self.level)
        self.speed = self.base_stats.calculate_stat(self.base_stats.speed, self.level)
        
        # Check for evolution
        evolution_data = self.species_data.get("evolution")
        if evolution_data and "level" in evolution_data and self.level >= evolution_data["level"]:
            return True
        
        return False
    
    def can_evolve(self) -> bool:
        """Check if Pokemon can evolve"""
        evolution_data = self.species_data.get("evolution")
        if not evolution_data:
            return False
            
        if "level" in evolution_data:
            return self.level >= evolution_data["level"]
        
        return False
    
    def evolve(self) -> str:
        """Evolve the Pokemon"""
        evolution_data = self.species_data.get("evolution")
        if not evolution_data:
            return None
            
        old_species = self.species
        self.species = evolution_data["evolves_to"]
        self.species_data = self.get_species_data(self.species)
        
        # Update types and abilities
        self.types = self.species_data["types"]
        self.ability = self.species_data.get("abilities", [self.ability])[0]
        
        # Recalculate stats with new base stats
        self.base_stats = Stats(**self.species_data["base_stats"])
        old_max_hp = self.max_hp
        self.max_hp = self.base_stats.calculate_stat(self.base_stats.hp, self.level)
        self.current_hp += (self.max_hp - old_max_hp)
        
        self.attack = self.base_stats.calculate_stat(self.base_stats.attack, self.level)
        self.defense = self.base_stats.calculate_stat(self.base_stats.defense, self.level)
        self.special_attack = self.base_stats.calculate_stat(self.base_stats.special_attack, self.level)
        self.special_defense = self.base_stats.calculate_stat(self.base_stats.special_defense, self.level)
        self.speed = self.base_stats.calculate_stat(self.base_stats.speed, self.level)
        
        return old_species
    
    def heal(self, amount: int = None):
        """Heal the Pokemon"""
        if amount is None:
            self.current_hp = self.max_hp
        else:
            self.current_hp = min(self.max_hp, self.current_hp + amount)
        
        # Clear status conditions when fully healed
        if self.current_hp == self.max_hp:
            self.status_condition = None
            self.status_turns = 0
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if fainted"""
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp == 0
    
    def is_fainted(self) -> bool:
        """Check if Pokemon is fainted"""
        return self.current_hp <= 0
    
    def calculate_damage(self, move: Move, target: 'Pokemon') -> int:
        """Calculate damage dealt by a move"""
        if move.power == 0:
            return 0
        
        # Base damage calculation
        level_factor = (2 * self.level / 5) + 2
        attack_stat = self.attack if move.type in [PokemonType.NORMAL, PokemonType.FIGHTING] else self.special_attack
        defense_stat = target.defense if move.type in [PokemonType.NORMAL, PokemonType.FIGHTING] else target.special_defense
        
        damage = ((level_factor * move.power * attack_stat / defense_stat) / 50) + 2
        
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(move.type, target.types)
        damage *= effectiveness
        
        # STAB (Same Type Attack Bonus)
        if move.type in self.types:
            damage *= 1.5
        
        # Random factor
        damage *= random.uniform(0.85, 1.0)
        
        return int(damage)
    
    @classmethod
    def get_type_effectiveness_static(cls, attack_type: PokemonType, target_type: PokemonType) -> float:
        """Calculate type effectiveness multiplier (class method)"""
        if attack_type in cls.TYPE_EFFECTIVENESS:
            return cls.TYPE_EFFECTIVENESS[attack_type].get(target_type, 1.0)
        return 1.0

    def get_type_effectiveness(self, attack_type: PokemonType, target_types: List[PokemonType]) -> float:
        """Calculate type effectiveness multiplier for multiple target types"""
        effectiveness = 1.0
        
        for target_type in target_types:
            if attack_type in self.TYPE_EFFECTIVENESS:
                type_multiplier = self.TYPE_EFFECTIVENESS[attack_type].get(target_type, 1.0)
                effectiveness *= type_multiplier
        
        return effectiveness
    
    def get_catch_rate(self) -> int:
        """Get base catch rate for this Pokemon"""
        # Base catch rates (higher = easier to catch)
        catch_rates = {
            "Bulbasaur": 45, "Charmander": 45, "Squirtle": 45,
            "Pikachu": 190, "Rattata": 255, "Caterpie": 255, "Pidgey": 255
        }
        return catch_rates.get(self.species, 100)
    
    def get_info(self) -> Dict:
        """Get comprehensive Pokemon information"""
        return {
            "species": self.species,
            "nickname": self.nickname,
            "level": self.level,
            "types": [t.value for t in self.types],
            "hp": f"{self.current_hp}/{self.max_hp}",
            "stats": {
                "attack": self.attack,
                "defense": self.defense,
                "special_attack": self.special_attack,
                "special_defense": self.special_defense,
                "speed": self.speed
            },
            "moves": [move.name for move in self.moves],
            "nature": self.nature,
            "ability": self.ability,
            "experience": f"{self.experience}/{self.experience_to_next_level}",
            "friendship": self.friendship,
            "is_shiny": self.is_shiny,
            "status": self.status_condition
        }
    
    def __str__(self) -> str:
        return f"{self.nickname} (Lv.{self.level}) - {self.current_hp}/{self.max_hp} HP" 