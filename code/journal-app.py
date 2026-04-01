"""
Project: Personal Journal

Extracted from the companion book.
"""

def save_entry(entry, filename="journal.txt"):
    """Save entry to journal file"""
    try:
        with open(filename, "a") as file:
            file.write(entry)
        return True
    except Exception as e:
        print(f"Error saving entry: {e}")
        return False

def read_recent_entries(filename="journal.txt", count=5):
    """Read the most recent journal entries"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            
        # Split by entry separator
        entries = content.split("=" * 50)
        # Filter out empty entries
        entries = [e.strip() for e in entries if e.strip()]
        
        # Return last 'count' entries
        return entries[-count:] if len(entries) > count else entries
        
    except FileNotFoundError:
        return []
