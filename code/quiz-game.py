"""
Project: Quiz Game

Extracted from the companion book.
"""

def load_questions(filename):
    """Load questions from a text file"""
    questions = []
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
        i = 0
        while i < len(lines):
            if lines[i].strip() and not lines[i].startswith('#'):
                # Parse question format
                question_text = lines[i].strip()
                options = []
                
                # Next 4 lines are options
                for j in range(4):
                    if i + j + 1 < len(lines):
                        options.append(lines[i + j + 1].strip())
                
                # Next line is correct answer (A, B, C, or D)
                if i + 5 < len(lines):
                    correct = ord(lines[i + 5].strip()[0]) - 65
                
                # Optional explanation
                explanation = ""
                if i + 6 < len(lines) and lines[i + 6].strip():
                    explanation = lines[i + 6].strip()
                
                question = create_question(
                    question_text, options, correct, explanation
                )
                questions.append(question)
                
                i += 7  # Move to next question
            else:
                i += 1
                
    except FileNotFoundError:
        print(f"Question file {filename} not found!")
        
    return questions
