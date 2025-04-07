def print_colored_feedback(guess, feedback):
    """Print the guess with colored feedback in terminal"""
    result = ""
    for i, (letter, status) in enumerate(zip(guess, feedback)):
        if status == "G":
            result += f"\033[92m{letter.upper()}\033[0m"  # Green
        elif status == "Y":
            result += f"\033[93m{letter.upper()}\033[0m"  # Yellow
        else:
            result += f"\033[90m{letter.upper()}\033[0m"  # Gray
    
    # Also show the feedback symbols for clarity
    symbols = ""
    for status in feedback:
        if status == "G":
            symbols += "🟩"
        elif status == "Y":
            symbols += "🟨"
        else:
            symbols += "⬛"
    
    return f"{result} {symbols}"