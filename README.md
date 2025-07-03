# Pokemon Adventure Game

A comprehensive text-based Pokemon adventure game built with Python, featuring sophisticated gameplay mechanics, multiple modules, and an engaging storyline.

## Features

### Core Gameplay
- **Pokemon Battles**: Turn-based combat system with type effectiveness
- **Pokemon Collection**: Catch, train, and evolve Pokemon
- **Gym Battles**: Challenge gym leaders to earn badges
- **World Exploration**: Travel through multiple locations
- **Shopping System**: Buy items and equipment
- **Pokemon Centers**: Heal your Pokemon team

### Advanced Features
- **Save System**: Save and load game progress
- **Auto-save**: Automatic game saving
- **Statistics Tracking**: Comprehensive gameplay statistics
- **Pokedex**: Track discovered and caught Pokemon
- **Inventory Management**: Organize items and equipment
- **Level System**: Pokemon and trainer progression
- **Type System**: 18 Pokemon types with effectiveness chart

### Technical Architecture
- **Object-Oriented Design**: Clean, modular code structure
- **Multiple Modules**: Organized into logical components
- **Error Handling**: Robust error management
- **Input Validation**: Comprehensive user input validation
- **Display System**: Formatted text output with animations
- **Save Management**: JSON-based save system with backup

## Installation

1. **Prerequisites**: Python 3.7 or higher
2. **Clone/Download**: Get the game files
3. **No Dependencies**: Uses only Python standard library

```bash
# Navigate to the game directory
cd pokemon_game

# Run the game
python main.py
```

## Game Structure

```
pokemon_game/
├── main.py                 # Main entry point
├── game/                   # Core game logic
│   ├── __init__.py
│   ├── pokemon.py         # Pokemon classes and mechanics
│   ├── trainer.py         # Trainer and inventory system
│   ├── game_engine.py     # Main game engine
│   └── save_manager.py    # Save/load functionality
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── display.py         # Display and formatting
│   └── input_handler.py   # Input validation
├── saves/                  # Save files (auto-created)
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## How to Play

### Starting the Game
1. Run `python main.py`
2. Choose "New Game" or "Load Game"
3. Create your trainer and choose a starter Pokemon
4. Begin your adventure!

### Basic Controls
- **Menu Navigation**: Use numbers to select options
- **Battle System**: Choose Fight, Bag, Pokemon, or Run
- **Movement**: Select destinations from available connections
- **Inventory**: View and use items from your bag

### Game Progression
1. **Start**: Choose your starter Pokemon (Bulbasaur, Charmander, or Squirtle)
2. **Explore**: Visit different locations to find wild Pokemon
3. **Battle**: Fight wild Pokemon and trainers to gain experience
4. **Catch**: Use Pokeballs to catch wild Pokemon
5. **Train**: Level up your Pokemon through battles
6. **Gym Challenge**: Defeat gym leaders to earn badges
7. **Shop**: Buy items and equipment to aid your journey

### Locations
- **Pallet Town**: Starting location with Pokemon Lab
- **Route 1**: Peaceful route with common Pokemon
- **Viridian City**: City with gym and forest access
- **Viridian Forest**: Dense forest with Bug-type Pokemon
- **Pewter City**: Home of Brock, the Rock-type gym leader
- **Mt. Moon**: Mysterious cave with rare Pokemon
- **Cerulean City**: Home of Misty, the Water-type gym leader

### Pokemon Types
The game features a comprehensive type system:
- Normal, Fire, Water, Electric, Grass, Ice
- Fighting, Poison, Ground, Flying, Psychic, Bug
- Rock, Ghost, Dragon, Dark, Steel, Fairy

Each type has strengths and weaknesses against other types, affecting battle damage.

## Game Mechanics

### Battle System
- **Turn-based Combat**: Take turns choosing actions
- **Type Effectiveness**: Super effective, not very effective, or normal damage
- **Move System**: Each Pokemon has up to 4 moves
- **HP System**: Pokemon faint when HP reaches 0
- **Experience**: Gain EXP from battles to level up

### Pokemon Stats
- **HP**: Hit Points - determines how much damage Pokemon can take
- **Attack**: Physical attack power
- **Defense**: Physical defense
- **Sp. Attack**: Special attack power
- **Sp. Defense**: Special defense
- **Speed**: Determines turn order in battle

### Items
- **Pokeballs**: Catch wild Pokemon
- **Potions**: Restore Pokemon HP
- **Status Healers**: Cure poison, paralysis, sleep
- **Berries**: Various beneficial effects

### Save System
- **Manual Save**: Save at any time through the menu
- **Auto-save**: Automatic saving every 5 minutes
- **Multiple Saves**: Create multiple save files
- **Save Info**: View save file details before loading

## Advanced Features

### Statistics Tracking
- Battles won/lost
- Pokemon caught
- Gyms defeated
- Play time
- Money earned
- Pokedex completion

### Customization
- Pokemon nicknames
- Trainer customization
- Game settings (animation speed, display width)
- Auto-save intervals

### Error Handling
- Input validation
- Save file corruption protection
- Graceful error recovery
- User-friendly error messages

## Development Notes

### Code Architecture
- **Modular Design**: Separated concerns into logical modules
- **Object-Oriented**: Uses classes for Pokemon, Trainer, Items, etc.
- **Type Hints**: Full type annotation for better code quality
- **Documentation**: Comprehensive docstrings and comments

### Design Patterns
- **Factory Pattern**: Pokemon and item creation
- **Strategy Pattern**: Battle mechanics and AI
- **Observer Pattern**: Game state management
- **Command Pattern**: Input handling and validation

### Performance
- **Efficient Data Structures**: Optimized for gameplay
- **Memory Management**: Proper resource cleanup
- **Fast Save/Load**: JSON-based serialization
- **Responsive UI**: Minimal delay in user interactions

## Future Enhancements

### Planned Features
- More Pokemon species and moves
- Additional locations and gym leaders
- Trading system
- Breeding mechanics
- Online multiplayer battles
- Graphical user interface

### Technical Improvements
- Database integration for Pokemon data
- Network multiplayer support
- Advanced AI for computer opponents
- Plugin system for custom content

## Contributing

This game is designed as a showcase of programming skills and game development concepts. The code is well-structured and documented for educational purposes.

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write comprehensive docstrings
- Include unit tests for new features

## License

This project is for educational and demonstration purposes. It showcases various programming concepts including:
- Object-oriented programming
- Game development patterns
- File I/O and data persistence
- User interface design
- Error handling and validation

## Support

For questions or issues:
1. Check the code documentation
2. Review the README file
3. Examine the game structure and comments
4. Test the game functionality

---

**Enjoy your Pokemon adventure!** 