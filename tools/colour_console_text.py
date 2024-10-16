# colour_console_text.py

red = '\033[91m'
green = '\033[92m'
END = '\033[0m'
NEON_GREEN = '\033[32m'
RESET_COLOR = '\033[0m'
grey = '\033[90m'  # Added grey color

def get_grey_text(text):
    """Return the text to be colored grey and the color tag name."""
    return text, 'grey'
