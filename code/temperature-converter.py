"""
Project: Temperature Converter

Extracted from the companion book.
"""

def main():
    """Run the temperature converter"""
    history = []  # Store conversions
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == "8":
            break
        elif choice == "1":
            temp = get_temperature_input("Celsius")
            result = celsius_to_fahrenheit(temp)
            display_result(temp, result, "°C", "°F")
            history.append({"from": temp, "to": result, "type": "C→F"})
