# ZMK Keymap Organization and Formatting Recommendations

## Current State Analysis

The current ZMK keymap files in this repository have several challenges that make them difficult to maintain and read:

1. **No syntax highlighting** in `.keymap` files
2. **Scattered key bindings** across multiple files (`base_36.keymap`, `corne.keymap`)
3. **Complex nested structures** with behaviors, combos, and layers mixed together
4. **Limited visual organization** for understanding key layouts

## Research Findings and Recommendations

### 1. File Organization Improvements

#### Modular Structure
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

#### Separation of Concerns
Split large keymap files into focused components:
- **Behaviors**: Put all custom behaviors in a separate `behaviors.dtsi` file
- **Combos**: Keep combo definitions in their own file
- **Layers**: Organize each layer in a visually clear format
- **Includes**: Use `#include` directives to compose keymaps from modular components

### 2. Syntax Highlighting Solutions

#### VS Code Configuration
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

#### Recommended Extensions
Install these VS Code extensions:
- **Devicetree Language Support**: Provides syntax highlighting for `.keymap` files
- **C/C++ Extension Pack**: Enables formatting with clang-format
- **ZMK Tools**: Provides keymap validation and other ZMK-specific features

### 3. Formatting Improvements

#### Visual Layout Organization
Format key bindings in a grid pattern that mirrors the physical keyboard layout:

```dts
default_layer {
    display-name = "Base";
    bindings = <
        &kp Q     &kp W     &kp E     &kp R     &kp T       &kp Y     &kp U     &kp I     &kp O     &kp P
        &kp A     &kp S     &kp D     &kp F     &kp G       &kp H     &kp J     &kp K     &kp L     &kp SEMI
        &kp Z     &kp X     &kp C     &kp V     &kp B       &kp N     &kp M     &kp COMMA &kp DOT   &kp SLASH
                          &kp LCTRL &kp LGUI  &kp LSHFT              &kp SPACE &kp RALT  &kp RCTRL
    >;
};
```

#### Consistent Indentation and Spacing
- Use consistent indentation (4 spaces) for nested structures
- Align key bindings in columns for easy visual scanning
- Add blank lines between logical sections

#### Layer Definition Standards
Always include:
- `display-name` property for each layer
- Consistent naming conventions for layers
- Comments explaining layer purpose when not obvious

### 4. Keymap Visualization Tools

#### Keymap-Drawer Integration
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

#### Benefits of Visualization
- Easy understanding of complex keymap layouts
- Quick identification of layer differences
- Better collaboration and sharing of keymap designs
- Visual validation of keymap logic

### 5. Automation and Validation Scripts

#### Advanced Formatting Script
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
        
        return 'bindings = <\n        ' + '\n        '.join(formatted) + '\n    >'
    
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

#### Pre-commit Hook for Automatic Formatting
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

#### Editor Integration for Real-time Formatting
Configure your editor to automatically format on save:

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

#### Validation Script
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

### 6. Documentation and Comments

#### Add Header Comments
Include header comments explaining the purpose of each file:

```dts
/*
 * Corne keyboard keymap
 * 
 * This keymap defines the base layer and custom behaviors for the Corne keyboard.
 * It includes homerow mods, layer tap behaviors, and custom key combinations.
 */
```

#### Comment Complex Behaviors
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

### 7. Community Best Practices

#### Follow ZMK Standards
- Use standard ZMK keycode names (e.g., `&kp A` instead of custom macros when possible)
- Follow ZMK's layer naming conventions
- Keep up to date with ZMK best practices documentation

#### Use ZMK Helpers
Consider using [zmk-helpers](https://github.com/urob/zmk-helpers) for:
- Simplified macro definitions
- Standardized key position labels
- Unicode character support
- Cleaner keymap syntax

#### Version Control Best Practices
- Commit visual keymap diagrams along with keymap changes
- Use descriptive commit messages for keymap modifications
- Tag releases with keymap versions for easy rollback

## Implementation Priority

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

## Expected Benefits

### Immediate Benefits
- **Better readability**: Syntax highlighting and proper formatting
- **Easier maintenance**: Separation of concerns makes changes easier
- **Reduced errors**: Validation catches syntax issues early

### Long-term Benefits
- **Improved collaboration**: Clear structure makes it easier for others to contribute
- **Better documentation**: Visual keymaps and organized files
- **Automated workflows**: Scripts reduce manual work and ensure consistency