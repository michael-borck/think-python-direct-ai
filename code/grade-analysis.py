"""
Project: Grade Analysis Tool

Extracted from the companion book.
"""

def clean_grade(grade_str):
    """Convert grade string to float, handling edge cases"""
    if not grade_str or grade_str.strip() == "":
        return None
    
    # Remove common non-numeric characters
    cleaned = grade_str.strip().replace('%', '')
    
    # Handle common text values
    if cleaned.lower() in ['n/a', 'na', 'absent', 'missing']:
        return None
    
    try:
        grade = float(cleaned)
        # Validate range
        if 0 <= grade <= 100:
            return grade
        else:
            print(f"Warning: Grade {grade} outside valid range")
            return None
    except ValueError:
        print(f"Warning: Could not parse grade '{grade_str}'")
        return None

def clean_student_grades(student):
    """Clean all grades for a student"""
    cleaned = {}
    cleaned['name'] = student.get('Name', 'Unknown')
    cleaned['id'] = student.get('StudentID', 'Unknown')
    
    # Get all assignment columns (skip Name and StudentID)
    assignment_columns = [col for col in student.keys() 
                         if col not in ['Name', 'StudentID']]
    
    cleaned['assignments'] = {}
    for assignment in assignment_columns:
        grade = clean_grade(student.get(assignment, ''))
        cleaned['assignments'][assignment] = grade
    
    return cleaned
