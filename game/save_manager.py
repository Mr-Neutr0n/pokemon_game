"""
Save manager for handling game saves and statistics
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional

class SaveManager:
    """Manages game saves and statistics"""
    
    def __init__(self):
        self.save_directory = "saves"
        self.stats_file = "saves/global_stats.json"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure save directories exist"""
        os.makedirs(self.save_directory, exist_ok=True)
    
    def save_game(self, trainer, save_name: str = None) -> bool:
        """Save the current game state"""
        try:
            if save_name is None:
                save_name = f"{trainer.name}_{int(time.time())}"
            
            save_data = {
                "save_name": save_name,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "trainer_data": trainer.get_save_data()
            }
            
            filename = f"{self.save_directory}/{save_name}.json"
            
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            # Update global statistics
            self.update_global_stats(trainer)
            
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, save_name: str) -> Optional[Dict]:
        """Load a saved game"""
        try:
            filename = f"{self.save_directory}/{save_name}.json"
            
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            return save_data.get("trainer_data")
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def get_save_files(self) -> List[str]:
        """Get list of available save files"""
        try:
            save_files = []
            
            for filename in os.listdir(self.save_directory):
                if filename.endswith('.json') and filename != 'global_stats.json':
                    save_files.append(filename[:-5])  # Remove .json extension
            
            return sorted(save_files)
            
        except Exception as e:
            print(f"Error getting save files: {e}")
            return []
    
    def get_save_info(self, save_name: str) -> Dict:
        """Get information about a save file"""
        try:
            filename = f"{self.save_directory}/{save_name}.json"
            
            if not os.path.exists(filename):
                return {}
            
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            trainer_data = save_data.get("trainer_data", {})
            
            return {
                "trainer_name": trainer_data.get("trainer_name", "Unknown"),
                "trainer_level": trainer_data.get("trainer_level", 1),
                "current_location": trainer_data.get("current_location", "Unknown"),
                "pokemon_count": len(trainer_data.get("pokemon_team", [])),
                "badges": len(trainer_data.get("badges", [])),
                "play_time": self.format_play_time(trainer_data.get("stats", {}).get("play_time", 0)),
                "timestamp": save_data.get("timestamp", "Unknown"),
                "pokedex_caught": len(trainer_data.get("pokedex_caught", []))
            }
            
        except Exception as e:
            print(f"Error getting save info: {e}")
            return {}
    
    def delete_save(self, save_name: str) -> bool:
        """Delete a save file"""
        try:
            filename = f"{self.save_directory}/{save_name}.json"
            
            if os.path.exists(filename):
                os.remove(filename)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting save: {e}")
            return False
    
    def update_global_stats(self, trainer):
        """Update global statistics"""
        try:
            # Load existing stats
            global_stats = self.load_global_stats()
            
            # Update stats
            global_stats["total_games"] = global_stats.get("total_games", 0) + 1
            global_stats["total_play_time"] += trainer.stats.get("play_time", 0)
            global_stats["total_pokemon_caught"] += trainer.stats.get("pokemon_caught", 0)
            global_stats["total_battles_won"] += trainer.stats.get("battles_won", 0)
            global_stats["total_gyms_defeated"] += trainer.stats.get("gyms_defeated", 0)
            global_stats["last_played"] = datetime.now().isoformat()
            
            # Save updated stats
            with open(self.stats_file, 'w') as f:
                json.dump(global_stats, f, indent=2)
                
        except Exception as e:
            print(f"Error updating global stats: {e}")
    
    def load_global_stats(self) -> Dict:
        """Load global statistics"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            
            return self.get_default_stats()
            
        except Exception as e:
            print(f"Error loading global stats: {e}")
            return self.get_default_stats()
    
    def get_default_stats(self) -> Dict:
        """Get default statistics"""
        return {
            "total_games": 0,
            "total_play_time": 0,
            "total_pokemon_caught": 0,
            "total_battles_won": 0,
            "total_gyms_defeated": 0,
            "first_played": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat()
        }
    
    def get_global_statistics(self) -> Dict:
        """Get formatted global statistics"""
        stats = self.load_global_stats()
        
        return {
            "total_games": stats.get("total_games", 0),
            "total_play_time": self.format_play_time(stats.get("total_play_time", 0)),
            "total_pokemon_caught": stats.get("total_pokemon_caught", 0),
            "total_battles_won": stats.get("total_battles_won", 0),
            "total_gyms_defeated": stats.get("total_gyms_defeated", 0),
            "first_played": self.format_date(stats.get("first_played")),
            "last_played": self.format_date(stats.get("last_played"))
        }
    
    def format_play_time(self, minutes: int) -> str:
        """Format play time in minutes to readable format"""
        if minutes < 60:
            return f"{minutes}m"
        
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if hours < 24:
            return f"{hours}h {remaining_minutes}m"
        
        days = hours // 24
        remaining_hours = hours % 24
        
        return f"{days}d {remaining_hours}h {remaining_minutes}m"
    
    def format_date(self, date_string: str) -> str:
        """Format ISO date string to readable format"""
        try:
            if not date_string:
                return "Unknown"
            
            dt = datetime.fromisoformat(date_string)
            return dt.strftime("%Y-%m-%d %H:%M")
            
        except Exception:
            return "Unknown"
    
    def backup_save(self, save_name: str) -> bool:
        """Create a backup of a save file"""
        try:
            source = f"{self.save_directory}/{save_name}.json"
            backup = f"{self.save_directory}/{save_name}_backup_{int(time.time())}.json"
            
            if os.path.exists(source):
                with open(source, 'r') as src:
                    data = json.load(src)
                
                with open(backup, 'w') as bak:
                    json.dump(data, bak, indent=2)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def auto_save(self, trainer, interval_minutes: int = 5) -> bool:
        """Auto-save the game if enough time has passed"""
        try:
            auto_save_file = f"{self.save_directory}/autosave.json"
            
            # Check if auto-save should occur
            if os.path.exists(auto_save_file):
                stat = os.stat(auto_save_file)
                last_save_time = stat.st_mtime
                current_time = time.time()
                
                if current_time - last_save_time < interval_minutes * 60:
                    return False  # Too soon for auto-save
            
            # Perform auto-save
            save_data = {
                "save_name": "autosave",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "trainer_data": trainer.get_save_data()
            }
            
            with open(auto_save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error auto-saving: {e}")
            return False
    
    def load_auto_save(self) -> Optional[Dict]:
        """Load the auto-save file"""
        try:
            auto_save_file = f"{self.save_directory}/autosave.json"
            
            if not os.path.exists(auto_save_file):
                return None
            
            with open(auto_save_file, 'r') as f:
                save_data = json.load(f)
            
            return save_data.get("trainer_data")
            
        except Exception as e:
            print(f"Error loading auto-save: {e}")
            return None
    
    def export_save(self, save_name: str, export_path: str) -> bool:
        """Export a save file to a different location"""
        try:
            source = f"{self.save_directory}/{save_name}.json"
            
            if not os.path.exists(source):
                return False
            
            with open(source, 'r') as src:
                data = json.load(src)
            
            with open(export_path, 'w') as exp:
                json.dump(data, exp, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting save: {e}")
            return False
    
    def import_save(self, import_path: str, save_name: str) -> bool:
        """Import a save file from a different location"""
        try:
            if not os.path.exists(import_path):
                return False
            
            with open(import_path, 'r') as imp:
                data = json.load(imp)
            
            # Validate save data structure
            if not self.validate_save_data(data):
                return False
            
            destination = f"{self.save_directory}/{save_name}.json"
            
            with open(destination, 'w') as dest:
                json.dump(data, dest, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error importing save: {e}")
            return False
    
    def validate_save_data(self, save_data: Dict) -> bool:
        """Validate save data structure"""
        try:
            required_fields = ["save_name", "timestamp", "version", "trainer_data"]
            
            for field in required_fields:
                if field not in save_data:
                    return False
            
            trainer_data = save_data["trainer_data"]
            required_trainer_fields = ["trainer_name", "trainer_level", "current_location"]
            
            for field in required_trainer_fields:
                if field not in trainer_data:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_save_file_size(self, save_name: str) -> int:
        """Get the size of a save file in bytes"""
        try:
            filename = f"{self.save_directory}/{save_name}.json"
            
            if os.path.exists(filename):
                return os.path.getsize(filename)
            
            return 0
            
        except Exception:
            return 0
    
    def cleanup_old_saves(self, max_saves: int = 10) -> int:
        """Clean up old save files, keeping only the most recent ones"""
        try:
            save_files = self.get_save_files()
            
            if len(save_files) <= max_saves:
                return 0
            
            # Sort by modification time
            save_info = []
            for save_name in save_files:
                filename = f"{self.save_directory}/{save_name}.json"
                if os.path.exists(filename):
                    mtime = os.path.getmtime(filename)
                    save_info.append((save_name, mtime))
            
            # Sort by modification time (newest first)
            save_info.sort(key=lambda x: x[1], reverse=True)
            
            # Delete old saves
            deleted_count = 0
            for save_name, _ in save_info[max_saves:]:
                if self.delete_save(save_name):
                    deleted_count += 1
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up saves: {e}")
            return 0 