"""
Project: Weather Dashboard

Extracted from the companion book.
"""

class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        
        # Initialize components
        self.weather_api = WeatherAPI("your_api_key_here")
        self.cities = self.load_saved_cities()
        self.weather_cards = []
        
        self.create_interface()
        self.refresh_all_weather()
        self.schedule_auto_refresh()
    
    def create_interface(self):
        # Title
        title = tk.Label(self.root, text="🌤️ Weather Dashboard", 
                        font=('Arial', 20, 'bold'))
        title.pack(pady=10)
        
        # Controls frame
        controls = tk.Frame(self.root)
        controls.pack(pady=5)
        
        tk.Button(controls, text="Add City", 
                 command=self.show_add_city_dialog).pack(side='left', padx=5)
        tk.Button(controls, text="Refresh All", 
                 command=self.refresh_all_weather).pack(side='left', padx=5)
        
        self.last_update_label = tk.Label(controls, text="")
        self.last_update_label.pack(side='right', padx=5)
        
        # Cities frame
        self.cities_frame = tk.Frame(self.root)
        self.cities_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def show_add_city_dialog(self):
        """Show dialog to add new city"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add City")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Enter city name:").pack(pady=10)
        
        city_entry = tk.Entry(dialog, width=20)
        city_entry.pack(pady=5)
        city_entry.focus()
        
        def add_city():
            city = city_entry.get().strip()
            if city:
                self.add_city(city)
                dialog.destroy()
        
        tk.Button(dialog, text="Add", command=add_city).pack(pady=10)
        
        # Allow Enter key to add
        dialog.bind('<Return>', lambda e: add_city())
    
    def add_city(self, city_name):
        """Add a new city to the dashboard"""
        if city_name not in self.cities:
            weather_data = self.weather_api.get_current_weather(city_name)
            if weather_data:
                self.cities.append(city_name)
                self.save_cities()
                self.refresh_display()
            else:
                tk.messagebox.showerror("Error", f"Could not find weather for {city_name}")
    
    def remove_city(self, city_name):
        """Remove a city from the dashboard"""
        if city_name in self.cities:
            self.cities.remove(city_name)
            self.save_cities()
            self.refresh_display()
    
    def refresh_all_weather(self):
        """Refresh weather data for all cities"""
        self.last_update_label.config(text="Updating...")
        self.root.update()
        
        self.refresh_display()
        
        now = datetime.now().strftime("%I:%M %p")
        self.last_update_label.config(text=f"Updated: {now}")
    
    def refresh_display(self):
        """Refresh the display with current weather data"""
        # Clear existing cards
        for widget in self.cities_frame.winfo_children():
            widget.destroy()
        
        # Create new cards
        row = 0
        col = 0
        max_cols = 3
        
        for city in self.cities:
            weather_data = self.weather_api.get_current_weather(city)
            if weather_data:
                card = WeatherCard(self.cities_frame, weather_data, self.remove_city)
                card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
        
        # Configure grid weights for responsive layout
        for i in range(max_cols):
            self.cities_frame.columnconfigure(i, weight=1)
    
    def schedule_auto_refresh(self):
        """Schedule automatic refresh every 10 minutes"""
        self.refresh_all_weather()
        self.root.after(600000, self.schedule_auto_refresh)  # 10 minutes
    
    def load_saved_cities(self):
        """Load saved cities from file"""
        try:
            with open('weather_cities.txt', 'r') as f:
                return [city.strip() for city in f.readlines() if city.strip()]
        except FileNotFoundError:
            return ['New York']  # Default city
    
    def save_cities(self):
        """Save current cities to file"""
        with open('weather_cities.txt', 'w') as f:
            for city in self.cities:
                f.write(city + '\n')

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()
