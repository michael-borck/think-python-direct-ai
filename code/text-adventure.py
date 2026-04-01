"""
Project: Text Adventure Game

Extracted from the companion book.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import json

class AdventureGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🗡️ The Crystal Caves Adventure")
        self.root.geometry("900x700")
        
        # Initialize game components
        self.story_engine = StoryEngine()
        self.player = Player()
        self.inventory = Inventory()
        self.game_state = self.create_initial_state()
        
        self.create_interface()
        self.start_game()
    
    def create_interface(self):
        # Main title
        title_frame = tk.Frame(self.root, bg='darkblue', height=50)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🗡️ THE CRYSTAL CAVES ADVENTURE", 
                              font=('Arial', 16, 'bold'), fg='white', bg='darkblue')
        title_label.pack(expand=True)
        
        # Story display area
        story_frame = tk.Frame(self.root)
        story_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(story_frame, text="STORY", font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.story_text = scrolledtext.ScrolledText(
            story_frame, height=15, wrap=tk.WORD, 
            font=('Arial', 11), bg='lightyellow'
        )
        self.story_text.pack(fill='both', expand=True)
        
        # Choices frame
        choices_frame = tk.Frame(self.root)
        choices_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(choices_frame, text="CHOICES", font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.choices_frame = tk.Frame(choices_frame)
        self.choices_frame.pack(fill='x')
        
        # Status panel
        status_frame = tk.Frame(self.root, bg='lightgray', height=100)
        status_frame.pack(fill='x', padx=10, pady=5)
        status_frame.pack_propagate(False)
        
        # Split status into three columns
        player_frame = tk.Frame(status_frame, bg='lightgray')
        player_frame.pack(side='left', fill='both', expand=True)
        
        inventory_frame = tk.Frame(status_frame, bg='lightgray')
        inventory_frame.pack(side='left', fill='both', expand=True)
        
        progress_frame = tk.Frame(status_frame, bg='lightgray')
        progress_frame.pack(side='left', fill='both', expand=True)
        
        # Player status
        tk.Label(player_frame, text="PLAYER STATUS", font=('Arial', 10, 'bold'), 
                bg='lightgray').pack()
        self.player_status = tk.Label(player_frame, text="", justify='left', 
                                     bg='lightgray', font=('Arial', 9))
        self.player_status.pack()
        
        # Inventory
        tk.Label(inventory_frame, text="INVENTORY", font=('Arial', 10, 'bold'), 
                bg='lightgray').pack()
        self.inventory_status = tk.Label(inventory_frame, text="", justify='left', 
                                        bg='lightgray', font=('Arial', 9))
        self.inventory_status.pack()
        
        # Progress
        tk.Label(progress_frame, text="PROGRESS", font=('Arial', 10, 'bold'), 
                bg='lightgray').pack()
        self.progress_status = tk.Label(progress_frame, text="", justify='left', 
                                       bg='lightgray', font=('Arial', 9))
        self.progress_status.pack()
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(control_frame, text="💾 Save Game", 
                 command=self.save_game).pack(side='left', padx=5)
        tk.Button(control_frame, text="📁 Load Game", 
                 command=self.load_game).pack(side='left', padx=5)
        tk.Button(control_frame, text="🎒 Use Item", 
                 command=self.show_inventory_dialog).pack(side='left', padx=5)
        tk.Button(control_frame, text="❌ Quit", 
                 command=self.quit_game).pack(side='right', padx=5)
    
    def start_game(self):
        """Start the adventure"""
        self.story_engine.current_scene = 'cave_entrance'
        self.display_current_scene()
    
    def display_current_scene(self):
        """Display the current scene and update interface"""
        scene = self.story_engine.get_scene(self.story_engine.current_scene)
        if not scene:
            return
        
        # Mark scene as visited
        scene.visited = True
        
        # Clear and update story text
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(tk.END, f"{scene.title}\n\n")
        self.story_text.insert(tk.END, scene.description)
        
        # Clear previous choices
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
        
        # Display available choices
        available_choices = scene.get_available_choices(self.game_state)
        for i, choice in enumerate(available_choices):
            btn = tk.Button(
                self.choices_frame, 
                text=f"{i+1}. {choice['text']}", 
                command=lambda c=choice: self.make_choice(c),
                width=40, height=2, wraplength=300
            )
            btn.pack(pady=2, fill='x')
        
        # Update status displays
        self.update_status_displays()
    
    def make_choice(self, choice):
        """Process a player choice"""
        # Update game state based on choice
        self.game_state = self.story_engine.process_choice(choice, self.game_state)
        
        # Add choice to history
        self.game_state['story']['choices_made'].append(choice['text'])
        
        # Display the scene
        self.display_current_scene()
        
        # Check for special events
        self.check_random_events()
    
    def update_status_displays(self):
        """Update all status displays"""
        # Player status
        player_text = f"""❤️ Health: {self.player.health}/{self.player.max_health}
⭐ Magic: {self.player.magic}/{self.player.max_magic}
🏆 Level: {self.player.level} (XP: {self.player.experience})
🧭 Location: {self.story_engine.current_scene.replace('_', ' ').title()}"""
        self.player_status.config(text=player_text)
        
        # Inventory
        if self.inventory.items:
            inventory_text = "\n".join([f"• {item.get('name', 'Unknown')}" 
                                      for item in self.inventory.items[:5]])
            if len(self.inventory.items) > 5:
                inventory_text += f"\n... and {len(self.inventory.items) - 5} more"
        else:
            inventory_text = "Empty"
        self.inventory_status.config(text=inventory_text)
        
        # Progress
        progress_text = f"""⏱️ Scenes Visited: {len([s for s in self.story_engine.scenes.values() if s.visited])}
🎯 Choices Made: {len(self.game_state['story']['choices_made'])}
📊 Items Found: {len(self.inventory.items)}"""
        self.progress_status.config(text=progress_text)

    def save_game(self):
        """Save current game state"""
        save_data = {
            'player': {
                'name': self.player.name,
                'health': self.player.health,
                'max_health': self.player.max_health,
                'magic': self.player.magic,
                'max_magic': self.player.max_magic,
                'level': self.player.level,
                'experience': self.player.experience,
                'stats': self.player.stats
            },
            'inventory': self.inventory.items,
            'current_scene': self.story_engine.current_scene,
            'game_state': self.game_state
        }
        
        try:
            with open('adventure_save.json', 'w') as f:
                json.dump(save_data, f, indent=2)
            messagebox.showinfo("Save Game", "Game saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save game: {e}")
    
    def load_game(self):
        """Load saved game state"""
        try:
            with open('adventure_save.json', 'r') as f:
                save_data = json.load(f)
            
            # Restore player
            player_data = save_data['player']
            self.player.name = player_data['name']
            self.player.health = player_data['health']
            self.player.max_health = player_data['max_health']
            self.player.magic = player_data['magic']
            self.player.max_magic = player_data['max_magic']
            self.player.level = player_data['level']
            self.player.experience = player_data['experience']
            self.player.stats = player_data['stats']
            
            # Restore inventory
            self.inventory.items = save_data['inventory']
            
            # Restore scene
            self.story_engine.current_scene = save_data['current_scene']
            
            # Restore game state
            self.game_state = save_data['game_state']
            
            self.display_current_scene()
            messagebox.showinfo("Load Game", "Game loaded successfully!")
            
        except FileNotFoundError:
            messagebox.showerror("Load Error", "No saved game found!")
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load game: {e}")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = AdventureGameGUI(root)
    root.mainloop()
