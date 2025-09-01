# Consolidated ZMK Keymap Organization and Formatting Recommendations

## Overview

This document consolidates recommendations for improving the readability, maintainability, and organization of ZMK keymap files based on analysis from multiple sources.

## 1. File Organization Improvements

### Modular Structure
Organize keymap files into a clear, modular structure that separates concerns:

```
config/
├── keymaps/
│   ├── base/
│   │   ├── base.keymap          # Base keymap with common layers
│   │   ├── behaviors.dtsi       # Common behaviors
│   │   └── combos.dtsi          # Common combos
│   ├── keyboards/
│   │   ├── corne/
│   │   │   ├── corne.keymap     # Corne-specific keymap
│   │   │   └── corne.conf       # Corne-specific config
│   │   └── mono_corne/
│   │       ├── mono_corne.keymap
│   │       └── mono_corne.conf
│   └── layers/
│       ├── symbols.keymap       # Symbol layer definitions
│       ├── numbers.keymap       # Number layer definitions
│       └── media.keymap         # Media layer definitions
```

### Separation of Concerns
Split large keymap files into focused components:
- **Behaviors**: Put all custom behaviors in a separate `behaviors.dtsi` file
- **Combos**: Keep combo definitions in their own file
- **Layers**: Organize each layer in a visually clear format
- **Includes**: Use `#include` directives to compose keymaps from modular components

## 2. Syntax Highlighting Solutions

### VS Code Configuration
Add the following to `.vscode/settings.json`:

```json
{
    "files.associations": {
        "*.keymap": "dts",
        "*.dtsi": "dts"
    },
    "editor.formatOnSave": true,
    "[dts]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-vscode.cpptools"
    }
}
```

This configuration:
- Associates `.keymap` and `.dtsi` files with the Devicetree language for syntax highlighting
- Enables automatic formatting on save using the C/C++ extension

### Recommended Extensions
Install these VS Code extensions:
- **Devicetree Language Support**: Provides syntax highlighting for `.keymap` files
- **C/C++ Extension Pack**: Enables formatting with clang-format
- **ZMK Tools**: Provides keymap validation and other ZMK-specific features

## 3. Formatting Improvements

### Visual Layout Organization
Format key bindings in a grid pattern that mirrors the physical keyboard layout:

```dts
default_layer {
    display-name = "Base";
    bindings = <
//,-----------------------------------------------------.                    ,-----------------------------------------------------.
//|  Q  |  W  |  E  |  R  |  T  |                     |  Y  |  U  |  I  |  O  |  P  |
//`---------------------------+-------------------------'                    `---------------------------+-------------------------'
    &kp Q  &kp W  &ltf NAV E  &kp R  &kp T                                        &kp Y  &kp U  &bhm RC(RALT) I  &kp O  &kp P
//,---------------------------+-------------------------.                    ,---------------------------+-------------------------.
//|  A  |  S  |  D  |  F  |  G  |                     |  H  |  J  |  K  |  L  |  '  |
//`---------------------------+-------------------------'                    `---------------------------+-------------------------'
    &bhm LCTRL A  &kp S  &bhm LSHFT D  &bhm LGUI F  &kp G                      &kp H  &bhm RGUI J  &bhm RSFT K  &kp L  &bhm RCTRL APOS
//,---------------------------+-------------------------.                    ,---------------------------+-------------------------.
//|  Z  |  X  |  C  |  V  |  B  |                     |  N  |  M  |  ,  |  .  |  /  |
//`---------------------------+-------------------------'                    `---------------------------+-------------------------'
    &bhm LALT Z  &kp X  &kp C  &ltf ARROWS V  &kp B                               &lt BLUETOOTH N  &lt MEDIA M  &kp COMMA  &kp DOT  &bhm RALT FSLH
//,---------------------+-----------------------.           ,----------------------+--------------------.
//|     | SYM |     |           |      | NUM |      |
//`-------------------------------------------'           `------------------------------------------'
                      &trans  &escTap SYMBOLS ESC  &kp RSHFT  &spaceb  &ltf NUMBERS RET  &trans
        >;
};
```

### Layer Definition Standards
Always include:
- `display-name` property for each layer
- Consistent naming conventions for layers
- Comments explaining layer purpose when not obvious

## 4. Use Macros for Cleaner Code

Use C preprocessor macros (`#define`) to create aliases for complex or frequently used key bindings:

```c
// Layer Taps
#define SYM_ESC &escTap SYMBOLS ESC
#define NUM_RET &ltf NUMBERS RET
#define NAV_E &ltf NAV E
#define ARR_V &ltf ARROWS V
#define BT_N &lt BLUETOETOOTH N
#define MED_M &lt MEDIA M

// Home Row Mods
#define HC_A &bhm LCTRL A
#define HS_D &bhm LSHFT D
#define HG_F &bhm LGUI F
#define H_A_Z &bhm LALT Z
#define H_RGUI_J &bhm RGUI J
#define H_RSFT_K &bhm RSFT K
#define H_RCTL_APOS &bhm RCTRL APOS
#define H_RALT_FSLH &bhm RALT FSLH
```

## 5. Keymap Visualization Tools

### Keymap-Drawer Integration
Use [keymap-drawer](https://github.com/caksoylar/keymap-drawer) to generate visual representations of keymaps:

1. Install keymap-drawer:
   ```bash
   pip install keymap-drawer
   ```

2. Generate visual keymaps:
   ```bash
   keymap parse config/corne.keymap | keymap draw > corne.svg
   ```

3. Add to build process to automatically generate updated diagrams

### Automated Workflow
Automate the process of generating and updating your keymap diagram using a GitHub Actions workflow:

```yaml
name: 'Keymap'

on:
  workflow_dispatch:
  push:
    paths:
      - 'config/**.keymap'

jobs:
  draw:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout'
        uses: actions/checkout@v3

      - name: 'Draw keymap'
        uses: caksoylar/keymap-drawer-action@v1.3.0
        with:
          config_path: 'keymap_drawer.config.yaml'
          output_path: 'keymap.svg'
          zmk_config_url: 'https://github.com/parker/zmk-config/tree/main/config'

      - name: 'Commit keymap'
        uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: 'Update keymap diagram'
          file_pattern: 'keymap.svg'
```

## 6. Automated Keymap Formatting

### Advanced Formatting Script
Create a Python script to automatically format key bindings in a grid pattern:

```python
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
        
        return 'bindings = <\
        ' + '\
        '.join(formatted) + '\
    >'
    
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
```

### Pre-commit Hook for Automatic Formatting
Create a pre-commit hook to automatically format keymaps before each commit:

1. Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook to format ZMK keymap files

# Format keymap files
find config/ -name "*.keymap" -o -name "*.dtsi" | while read file; do
    python3 scripts/format_keymap.py "$file"
    git add "$file"
done
```

2. Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Editor Integration for Real-time Formatting
Configure your editor to automatically format on save with custom grid formatting:

**VS Code settings.json**:
```json
{
    "files.associations": {
        "*.keymap": "dts",
        "*.dtsi": "dts"
    },
    "editor.formatOnSave": true,
    "[dts]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-vscode.cpptools",
        "editor.codeActionsOnSave": {
            "source.fixAll": true
        }
    },
    "editor.rulers": [100]
}
```

**VS Code Tasks for Custom Formatting on Save**:
Create `.vscode/tasks.json` to run custom formatting:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "format-keymap",
            "type": "shell",
            "command": "python3",
            "args": ["scripts/format_keymap.py", "${file}"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "silent",
                "focus": false,
                "panel": "shared"
            },
            "options": {
                "cwd": "${workspaceFolder}"
            }
        }
    ]
}
```

**VS Code File Watcher for Automatic Formatting**:
Install the "Trigger Task on Save" extension and configure `.vscode/settings.json`:

```json
{
    "files.associations": {
        "*.keymap": "dts",
        "*.dtsi": "dts"
    },
    "triggerTaskOnSave.tasks": {
        "format-keymap": ["**/*.keymap", "**/*.dtsi"]
    },
    "triggerTaskOnSave.showMessageOnSuccess": false
}
```

## 7. Validation and Quality Assurance

### Validation Script
Create a script to validate keymap syntax:

```python
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
```

## 8. Documentation and Comments

### Add Header Comments
Include header comments explaining the purpose of each file:

```dts
/*
 * Corne keyboard keymap
 * 
 * This keymap defines the base layer and custom behaviors for the Corne keyboard.
 * It includes homerow mods, layer tap behaviors, and custom key combinations.
 */
```

### Comment Complex Behaviors
Add comments for complex behaviors to explain their purpose:

```dts
// Balanced hold-tap for homerow mods
// Flavor balanced provides a good compromise between hold and tap preferences
bhm: balanced_homerow_mods {
    compatible = "zmk,behavior-hold-tap";
    label = "HOMEROW_MODS";
    #binding-cells = <2>;
    tapping-term-ms = <200>;
    quick-tap-ms = <0>;
    flavor = "balanced";
    bindings = <&kp>, <&kp>;
};
```

## 9. Implementation Priority

### High Priority (Immediate Benefits)
1. **VS Code configuration**: Enable syntax highlighting and formatting
2. **Basic validation**: Add syntax checking for keymap files
3. **File reorganization**: Split large keymap files into focused components

### Medium Priority (Improved Workflow)
1. **Formatting standards**: Implement consistent visual layout formatting
2. **Documentation**: Add header comments and behavior explanations
3. **Automation scripts**: Create validation and formatting tools
4. **Automatic formatting**: Set up pre-commit hooks or editor integration for automatic grid formatting

### Low Priority (Long-term Improvements)
1. **Visualization tools**: Integrate keymap-drawer for visual documentation
2. **CI/CD integration**: Add automated validation to build process
3. **Community contribution**: Share organization patterns with ZMK community

## 10. Expected Benefits

### Immediate Benefits
- **Better readability**: Syntax highlighting and proper formatting
- **Easier maintenance**: Separation of concerns makes changes easier
- **Reduced errors**: Validation catches syntax issues early

### Long-term Benefits
- **Improved collaboration**: Clear structure makes it easier for others to contribute
- **Better documentation**: Visual keymaps and organized files
- **Automated workflows**: Scripts reduce manual work and ensure consistency
```