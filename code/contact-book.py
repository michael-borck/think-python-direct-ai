"""
Project: Contact Book

Extracted from the companion book.
"""

def save_contacts(contacts, filename="contacts.txt"):
    """Save contacts to file"""
    with open(filename, "w") as file:
        for contact in contacts:
            # Create a formatted line for each contact
            line = f"{contact['name']}|{contact['phone']}|{contact['email']}|{contact['address']}|{contact['notes']}\n"
            file.write(line)
    print(f"Saved {len(contacts)} contacts!")

def load_contacts(filename="contacts.txt"):
    """Load contacts from file"""
    contacts = []
    try:
        with open(filename, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) >= 2:  # At least name and phone
                    contact = create_contact(
                        parts[0],
                        parts[1] if len(parts) > 1 else "",
                        parts[2] if len(parts) > 2 else "",
                        parts[3] if len(parts) > 3 else "",
                        parts[4] if len(parts) > 4 else ""
                    )
                    contacts.append(contact)
    except FileNotFoundError:
        print("No existing contacts file found. Starting fresh!")
    
    return contacts
