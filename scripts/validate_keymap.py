#!/usr/bin/env python3
"""
ZMK Keymap Validation Script
Validates keymap syntax and provides feedback on organization.
"""

import re
import sys

def validate_keymap_syntax(keymap_file):
    """Basic syntax validation for ZMK keymaps."""
    errors = []
    
    try:
        with open(keymap_file, 'r') as f:
            content = f.read()
            
        # Check for required includes
        if '#include <behaviors.dtsi>' not in content:
            errors.append("Missing required include: #include <behaviors.dtsi>")
            
        if '#include <dt-bindings/zmk/keys.h>' not in content:
            errors.append("Missing required include: #include <dt-bindings/zmk/keys.h>")
            
        # Check for keymap node
        if 'compatible = "zmk,keymap"' not in content:
            errors.append("Missing keymap node with compatible property")
            
        # Check for layer structure
        layer_count = len(re.findall(r'\w+_layer\s*\{', content))
        if layer_count == 0:
            errors.append("No layers found in keymap")
            
        return errors
        
    except Exception as e:
        return [f"Error reading file: {e}"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_keymap.py <keymap_file>")
        sys.exit(1)
    
    keymap_file = sys.argv[1]
    errors = validate_keymap_syntax(keymap_file)
    
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Keymap validation passed!")