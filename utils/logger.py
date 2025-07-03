"""
Logger utility for debugging Pokemon game issues
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

class GameLogger:
    """Centralized logging for the Pokemon game"""
    
    def __init__(self, log_file: str = "pokemon_game_debug.log"):
        self.log_file = log_file
        self.logger = None
        self.setup_logger()
    
    def setup_logger(self):
        """Setup the logger with proper formatting"""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", self.log_file)
        
        # Create a unique logger name to avoid conflicts
        logger_name = f"pokemon_game_{id(self)}"
        self.logger = logging.getLogger(logger_name)
        
        # Only set up if not already configured
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            
            # Create file handler - ONLY log to file, not console
            file_handler = logging.FileHandler(log_path, mode='a')
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(file_handler)
            
            # Prevent propagation to root logger (which might have console handlers)
            self.logger.propagate = False
            
            # Log session start
            self.logger.info("="*60)
            self.logger.info(f"NEW GAME SESSION STARTED - {datetime.now()}")
            self.logger.info("="*60)
    
    def debug(self, message: str, context: Dict[str, Any] = None):
        """Log debug message with optional context"""
        if self.logger:
            if context:
                self.logger.debug(f"{message} | Context: {context}")
            else:
                self.logger.debug(message)
    
    def info(self, message: str, context: Dict[str, Any] = None):
        """Log info message with optional context"""
        if self.logger:
            if context:
                self.logger.info(f"{message} | Context: {context}")
            else:
                self.logger.info(message)
    
    def warning(self, message: str, context: Dict[str, Any] = None):
        """Log warning message with optional context"""
        if self.logger:
            if context:
                self.logger.warning(f"{message} | Context: {context}")
            else:
                self.logger.warning(message)
    
    def error(self, message: str, context: Dict[str, Any] = None, exception: Exception = None):
        """Log error message with optional context and exception"""
        if self.logger:
            if context and exception:
                self.logger.error(f"{message} | Context: {context} | Exception: {str(exception)}")
            elif context:
                self.logger.error(f"{message} | Context: {context}")
            elif exception:
                self.logger.error(f"{message} | Exception: {str(exception)}")
            else:
                self.logger.error(message)
    
    def battle_start(self, player_pokemon: Any, opponent_pokemon: Any, is_wild: bool):
        """Log battle start details"""
        if self.logger:
            context = {
                "player_pokemon": {
                    "species": getattr(player_pokemon, 'species', 'Unknown'),
                    "level": getattr(player_pokemon, 'level', 'Unknown'),
                    "hp": f"{getattr(player_pokemon, 'current_hp', 'Unknown')}/{getattr(player_pokemon, 'max_hp', 'Unknown')}",
                    "moves": [move.name for move in getattr(player_pokemon, 'moves', [])]
                },
                "opponent_pokemon": {
                    "species": getattr(opponent_pokemon, 'species', 'Unknown'),
                    "level": getattr(opponent_pokemon, 'level', 'Unknown'),
                    "hp": f"{getattr(opponent_pokemon, 'current_hp', 'Unknown')}/{getattr(opponent_pokemon, 'max_hp', 'Unknown')}",
                    "moves": [move.name for move in getattr(opponent_pokemon, 'moves', [])]
                },
                "is_wild": is_wild
            }
            self.info("BATTLE STARTED", context)
    
    def battle_choice(self, choice: Any, choice_type: str = "battle_menu"):
        """Log battle choice details"""
        if self.logger:
            context = {
                "choice": choice,
                "choice_type": choice_type,
                "choice_value": str(choice),
                "choice_class": type(choice).__name__
            }
            self.debug(f"BATTLE CHOICE - {choice_type.upper()}", context)
    
    def move_selection(self, pokemon: Any, move_choice: Any, move_selected: Any = None):
        """Log move selection details"""
        if self.logger:
            context = {
                "pokemon_species": getattr(pokemon, 'species', 'Unknown'),
                "available_moves": [move.name for move in getattr(pokemon, 'moves', [])],
                "move_choice": move_choice,
                "move_choice_type": type(move_choice).__name__,
                "move_selected": getattr(move_selected, 'name', 'None') if move_selected else None
            }
            self.debug("MOVE SELECTION", context)
    
    def damage_calculation(self, attacker: Any, defender: Any, move: Any, damage: int):
        """Log damage calculation details"""
        if self.logger:
            context = {
                "attacker": getattr(attacker, 'species', 'Unknown'),
                "defender": getattr(defender, 'species', 'Unknown'),
                "move": getattr(move, 'name', 'Unknown'),
                "move_power": getattr(move, 'power', 'Unknown'),
                "move_type": str(getattr(move, 'type', 'Unknown')),
                "damage": damage,
                "defender_hp_before": getattr(defender, 'current_hp', 'Unknown'),
                "defender_hp_after": max(0, getattr(defender, 'current_hp', 0) - damage)
            }
            self.debug("DAMAGE CALCULATION", context)
    
    def input_handler_call(self, method_name: str, args: tuple = None, result: Any = None):
        """Log input handler method calls"""
        if self.logger:
            context = {
                "method": method_name,
                "args": str(args) if args else None,
                "result": result,
                "result_type": type(result).__name__
            }
            self.debug(f"INPUT HANDLER - {method_name}", context)
    
    def battle_loop_iteration(self, iteration: int, player_hp: int, opponent_hp: int):
        """Log battle loop iteration"""
        if self.logger:
            context = {
                "iteration": iteration,
                "player_hp": player_hp,
                "opponent_hp": opponent_hp
            }
            self.debug("BATTLE LOOP ITERATION", context)
    
    def exception_caught(self, exception: Exception, location: str, context: Dict[str, Any] = None):
        """Log caught exceptions with full context"""
        if self.logger:
            error_context = {
                "location": location,
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "additional_context": context
            }
            self.error("EXCEPTION CAUGHT", error_context, exception)

# Global logger instance
game_logger = GameLogger() 