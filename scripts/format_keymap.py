#!/usr/bin/env python3
"""
Advanced ZMK Keymap Formatter
Formats key bindings in a grid pattern that mirrors physical keyboard layout.
"""

import re
import sys

def format_keymap_bindings(content):
    """Format key bindings in grid pattern."""
    # Find bindings sections
    def format_bindings(match):
        bindings = match.group(1)
        # Split into individual bindings
        bindings_list = re.findall(r'&[a-zA-Z0-9_]+', bindings)
        
        # Format in grid (adjust columns based on your keyboard)
        formatted = []
        columns = 10  # Adjust based on your keyboard layout
        
        for i in range(0, len(bindings_list), columns):
            row = bindings_list[i:i+columns]
            # Align each binding in columns
            formatted_row = ' '.join(f'{binding:12}' for binding in row)
            formatted.append(formatted_row)
        
        return 'bindings = <\\\n        ' + '\\\n        '.join(formatted) + '\\\n    >'
    
    # Apply formatting to all bindings sections
    pattern = r'bindings = <([^>]+)>'
    formatted_content = re.sub(pattern, format_bindings, content, flags=re.DOTALL)
    
    return formatted_content

def format_with_clang_and_grid(file_path):
    """Apply both clang-format and custom grid formatting."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # First apply custom grid formatting
        formatted_content = format_keymap_bindings(content)
        
        # Then apply clang-format if available
        try:
            import subprocess
            process = subprocess.Popen(['clang-format'], 
                                     stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     text=True)
            stdout, stderr = process.communicate(input=formatted_content)
            if process.returncode == 0:
                formatted_content = stdout
        except FileNotFoundError:
            print("clang-format not found, using custom formatting only")
        
        # Write back to file
        with open(file_path, 'w') as f:
            f.write(formatted_content)
            
        print(f"Formatted {file_path}")
        
    except Exception as e:
        print(f"Error formatting {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_keymap.py <keymap_file>")
        sys.exit(1)
    
    for file_path in sys.argv[1:]:
        format_with_clang_and_grid(file_path)