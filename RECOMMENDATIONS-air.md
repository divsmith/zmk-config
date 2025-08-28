# ZMK Keymap Organization and Formatting Recommendations

## Current State Analysis

The current keymap files in this ZMK config repository show several challenges:

1. **No syntax highlighting** in `.keymap` files
2. **Scattered key bindings** across multiple files (base_36.keymap, corne.keymap)
3. **Complex nested structures** with behaviors, combos, and layers mixed together
4. **Limited visual organization** for understanding key layouts

## Research Findings

### 1. ZMK Documentation and Best Practices

Let me gather the latest ZMK documentation to understand current best practices:

### 2. ZMK Documentation Findings

From the latest ZMK documentation, several best practices emerge:

#### File Organization
- **Separate configuration files**: Each keyboard should have its own `.conf` and `.keymap` files
- **Modular structure**: Use separate files for different keyboard configurations
- **Clear naming**: Use descriptive names like `corne.keymap`, `lily58.keymap`

#### Keymap Structure Best Practices
- **Use layer defines**: Define layer names with `#define` for better readability:
  ```c
  #define DEFAULT 0
  #define LOWER 1
  #define RAISE 2
  ```
- **Display names**: Add `display-name` properties to layers for better identification:
  ```dts
  default_layer {
      display-name = "Base";
      bindings = <...>;
  }
  ```
- **Proper includes**: Always include necessary headers:
  ```dts
  #include <behaviors.dtsi>
  #include <dt-bindings/zmk/keys.h>
  ```

#### Code Formatting
- **clang-format**: ZMK uses clang-format for consistent code styling
- **Prettier for documentation**: Use prettier for formatting documentation files
- **Consistent indentation**: Follow ZMK's standard formatting practices

### 3. Current Repository Analysis

The current repository structure shows:
- **base_36.keymap**: Contains the main keymap with multiple layers
- **corne.keymap**: Extends the base keymap with custom behaviors
- **Mixed organization**: Behaviors, combos, and layers are mixed together
- **No clear separation**: Different concerns are not well separated

### 4. Recommended Organization Structure

Based on ZMK best practices and common community patterns:

#### File Structure Recommendations
```
config/
├── keymaps/
│   ├── base/
│   │   ├── base.keymap          # Base keymap with common layers
│   │   ├── behaviors.dtsi      # Common behaviors
│   │   └── combos.dtsi         # Common combos
│   ├── keyboards/
│   │   ├── corne/
│   │   │   ├── corne.keymap     # Corne-specific keymap
│   │   │   └── corne.conf       # Corne-specific config
│   │   └── mono_corne/
│   │       ├── mono_corne.keymap
│   │       └── mono_corne.conf
│   ├── layers/
│   │   ├── common/              # Reusable layer definitions
│   │   ├── symbols.keymap       # Symbol layer definitions
│   │   ├── numbers.keymap       # Number layer definitions
│   │   └── media.keymap         # Media layer definitions
│   └── macros/
│       └── common.dtsi         # Common macros and helpers
├── keymap-drawer/
│   └── generate_keymaps.py      # Script to generate visual keymaps
└── formatting/
    └── .clang-format            # Clang format configuration
```

#### Content Organization
1. **Separate concerns**: Split behaviors, combos, and layers into different files
2. **Use includes**: Import common definitions with `#include`
3. **Modular design**: Create reusable components that can be shared across keyboards
4. **Clear naming**: Use descriptive names for all components

### 5. Formatting and Syntax Highlighting Recommendations

#### VS Code Configuration
Create a `.vscode/settings.json` file with:
```json
{
    "files.associations": {
        "*.keymap": "dts",
        "*.dtsi": "dts"
    },
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-vscode.cpptools",
    "[dts]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "james-yu.latex-workshop"
    }
}
```

#### Language Support
- **Install Devicetree Language Support**: VS Code extension for DTS syntax highlighting
- **Configure file associations**: Ensure `.keymap` and `.dtsi` files are recognized as Devicetree
- **Enable IntelliSense**: Get code completion and hover information for ZMK constructs

### 6. Keymap Visualization and Drawing Tools

#### Keymap-Drawer Integration
Create a Python script to generate visual keymaps:

```python
#!/usr/bin/env python3
"""
Keymap visualization generator for ZMK keymaps.
Uses keymap-drawer to create visual representations of keymaps.
"""

import subprocess
import os
import sys
from pathlib import Path

def generate_keymap_visualization(keymap_file, output_dir="keymap-drawer"):
    """Generate visual keymap from ZMK keymap file."""
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate keymap visualization
        cmd = [
            "keymap-drawer",
            "--input", keymap_file,
            "--output", os.path.join(output_dir, os.path.basename(keymap_file) + ".svg"),
            "--format", "svg"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Generated visualization: {os.path.join(output_dir, os.path.basename(keymap_file) + '.svg')}")
        else:
            print(f"Error generating visualization: {result.stderr}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_keymaps.py <keymap_file>")
        sys.exit(1)
    
    generate_keymap_visualization(sys.argv[1])
```

#### Integration with Build Process
Add to `build.yaml` or create a separate visualization build target:

```yaml
visualization:
  description: "Generate keymap visualizations"
  commands:
    - python3 keymap-drawer/generate_key_maps.py config/keymaps/base/base.keymap
    - python3 keymap-drawer/generate_key_maps.py config/keymaps/keyboards/corne/corne.keymap
```

### 7. Maintenance and Automation Scripts

#### Keymap Validation Script
Create a script to validate keymap syntax and structure:

```python
#!/usr/bin/env python3
"""
ZMK Keymap Validation Script
Validates keymap syntax and provides feedback on organization.
"""

import re
import os
from pathlib import Path

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

def check_organization(keymap_file):
    """Check keymap organization and provide suggestions."""
    suggestions = []
    
    try:
        with open(keymap_file, 'r') as f:
            content = f.read()
            
        # Check for long lines
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                suggestions.append(f"Line {i}: Consider breaking long line for readability")
                
        # Check for consistent spacing
        if 'bindings = <' in content and '&trans' in content:
            trans_count = content.count('&trans')
            if trans_count > 10:
                suggestions.append(f"High number of &trans ({trans_count}): Consider using empty layers")
                
        return suggestions
        
    except Exception as e:
        return [f"Error analyzing organization: {e}"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_keymap.py <keymap_file>")
        sys.exit(1)
    
    keymap_file = sys.argv[1]
    errors = validate_keymap_syntax(keymap_file)
    suggestions = check_organization(keymap_file)
    
    if errors:
        print("Errors found:")
        for error in errors:
            print(f"  - {error}")
            
    if suggestions:
        print("\nSuggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
            
    if not errors and not suggestions:
        print("Keymap validation passed!")
```

#### Automated Formatting Script
Create a script to automatically format keymaps according to ZMK standards:

```bash
#!/bin/bash
# Format ZMK keymaps according to project standards

find config/ -name "*.keymap" -o -name "*.dtsi" | while read file; do
    echo "Formatting $file..."
    # Apply clang-format if available
    if command -v clang-format &> /dev/null; then
        clang-format -i -style=file "$file"
    else
        echo "clang-format not found, skipping formatting"
    fi
done

echo "Formatting complete!"
```

### 8. Community Resources and Further Reading

#### Recommended Tools
1. **VS Code Extensions**:
   - Devicetree Language Support
   - C/C++ Extension Pack (for clang-format integration)
   - Prettier (for documentation formatting)

2. **Command Line Tools**:
   - `clang-format` for code formatting
   - `prettier` for documentation
   - Custom Python scripts for validation and visualization

3. **Online Resources**:
   - ZMK Documentation: https://zmk.dev/docs
   - ZMK Studio: For interactive keymap editing
   - Community forums for best practices

#### Workflow Integration
1. **Pre-commit hooks**: Run validation before commits
2. **CI/CD integration**: Include keymap validation in build pipeline
3. **Documentation generation**: Auto-generate keymap documentation from source

### 9. Specific Recommendations for Current Repository

#### Current Issues Identified
Based on analysis of the existing keymap files:

1. **Mixed concerns**: `base_36.keymap` contains behaviors, combos, and layers mixed together
2. **No syntax highlighting**: `.keymap` files not properly associated with Devicetree language
3. **Scattered definitions**: Layer definitions, behaviors, and combos are not well organized
4. **Large file size**: `base_36.keymap` is quite large and handles multiple keyboards
5. **No visual documentation**: No visual representation of keymaps for easy understanding

#### Recommended Refactoring

##### Step 1: Separate Concerns
Split `base_36.keymap` into focused files:

**`config/keymaps/base/behaviors.dtsi`**
```dts
// Common behaviors for all keyboards
#include <behaviors.dtsi>

/ {
    behaviors {
        spaceb: space_backspace {
            compatible = "zmk,behavior-mod-morph";
            label = "SPACE_BACKSPACE";
            #binding-cells = <0>;
            bindings = <&ht_tp HYP SPACE>, <&ht_tp DEL BSPC>;
            mods = <(MOD_RSFT)>;
        };
        
        lsb: left_shift_bracket {
            compatible = "zmk,behavior-mod-morph";
            label = "LEFT_SHIFT_BRACKET";
            #binding-cells = <0>;
            bindings =  <&kp LBRC>, <&kp LBKT>;
            mods = <(MOD_LSFT)>;
        };
        
        rsb: right_shift_bracket {
            compatible = "zmk,behavior-mod-morph";
            label = "RIGHT_SHIFT_BRACKET";
            #binding-cells = <0>;
            bindings = <&kp RBRC>, <&kp RBKT>;
            mods = <(MOD_LSFT)>;
        };
    };
};
```

**`config/keymaps/base/combos.dtsi`**
```dts
// Common combos for all keyboards
/ {
    combos {
        compatible = "zmk,combos";
        
        combo_caps_word {
            timeout-ms = <50>;
            key-positions = <15 20>;
            bindings = <&caps_word>;
        };
    };
};
```

**`config/keymaps/base/layers.keymap`**
```dts
// Common layer definitions
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <combos.dtsi>

// Layer Definitions
#define SYMBOLS 1
#define NUMBERS 2
#define ARROWS 3
#define NAV 4
#define MEDIA 5
#define BLUETOOTH 6

/ {
    keymap {
        compatible = "zmk,keymap";
        
        default_layer {
            display-name = "Base";
            bindings = <
            &kp Q &kp W &ltf NAV E &kp R &kp T                     &kp Y &kp U &bhm RC(RALT) I &kp O &kp P
            &bhm LCTRL A &kp S &bhm LSHFT D &bhm LGUI F &kp G     &kp H &bhm RGUI J &bhm RSFT K &kp L &bhm RCTRL APOS
            &bhm LALT Z  &kp X &kp C &ltf ARROWS V                 &kp B &lt BLUETOOTH N &lt MEDIA M &kp COMMA &kp DOT &bhm RALT FSLH
            &trans &escTap SYMBOLS ESC &kp RSHFT        &spaceb &ltf NUMBERS RET &trans
            >;
        };
        
        symbol_layer {
            display-name = "Symbols";
            bindings = <
            &trans &trans &trans &trans &trans       &kp BSLH    &kp PIPE    &kp LPAR &kp RPAR &kp GRAVE
            &trans &trans &trans &trans &trans       &kp MINUS &kp EQUAL &lsb &rsb &kp SEMI
            &trans &trans &trans &trans &trans       &trans    &trans    &kp LT   &kp GT   &trans
            &trans &trans &trans       &ht_tp DEL BSPC &kp TAB &trans
            >;
        };
        
        // ... other layers
    };
};
```

##### Step 2: Create Keyboard-Specific Files
**`config/keymaps/keyboards/corne/corne.keymap`**
```dts
#include "../base/layers.keymap"

/ {
    behaviors {
        ht_tp: tap_preferred_thumbkeys {
            compatible = "zmk,behavior-hold-tap";
            label = "TAP_PREFERRED_THUMBKEYS";
            #binding-cells = <2>;
            tapping-term-ms = <200>;
            quick-tap-ms = <200>;
            require-prior-idle-ms = <125>;
            flavor = "tap-preferred";
            bindings = <&kp>, <&kp>;
        };

        bhm: balanced_homerow_mods {
            compatible = "zmk,behavior-hold-tap";
            label = "HOMEROW_MODS";
            #binding-cells = <2>;
            tapping-term-ms = <200>;
            quick-tap-ms = <0>;
            flavor = "balanced";
            bindings = <&kp>, <&kp>;
        };

        ltf: layer_tap_fast {
            compatible = "zmk,behavior-hold-tap";
            label = "LAYER_TAP_FAST";
            #binding-cells = <2>;
            tapping-term-ms = <200>;
            quick-tap-ms = <200>;
            require-prior-idle-ms = <125>;
            flavor = "tap-preferred";
            bindings = <&mo>, <&kp>;
        };

        escTap: escapeTap {
            compatible = "zmk,behavior-hold-tap";
            label = "ESCAPE_TAP";
            #binding-cells = <2>;
            tapping-term-ms = <200>;
            flavor = "hold-preferred";
            bindings = <&mo>, <&kp>;
        };
    };
};
```

##### Step 3: Add VS Code Configuration
**`.vscode/settings.json`**
```json
{
    "files.associations": {
        "*.keymap": "dts",
        "*.dtsi": "dts"
    },
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-vscode.cpptools",
    "[dts]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "james-yu.latex-workshop"
    },
    "editor.codeActionsOnSave": {
        "source.fixAll": true
    }
}
```

**`.vscode/extensions.json`**
```json
{
    "recommendations": [
        "ms-vscode.cpptools",
        "james-yu.latex-workshop",
        "ms-python.python"
    ]
}
```

### 10. Implementation Priority

#### High Priority (Immediate Benefits)
1. **File reorganization**: Split large keymap files into focused components
2. **VS Code configuration**: Enable syntax highlighting and formatting
3. **Basic validation**: Add syntax checking for keymap files

#### Medium Priority (Improved Workflow)
1. **Visualization tools**: Integrate keymap-drawer for visual documentation
2. **Automation scripts**: Create validation and formatting tools
3. **Documentation**: Generate README files for each keyboard configuration

#### Low Priority (Long-term Improvements)
1. **CI/CD integration**: Add automated validation to build process
2. **Advanced tools**: Explore ZMK Studio and other interactive tools
3. **Community contribution**: Share organization patterns with ZMK community

### 11. Expected Benefits

#### Immediate Benefits
- **Better readability**: Syntax highlighting and proper formatting
- **Easier maintenance**: Separation of concerns makes changes easier
- **Reduced errors**: Validation catches syntax issues early

#### Long-term Benefits
- **Improved collaboration**: Clear structure makes it easier for others to contribute
- **Better documentation**: Visual keymaps and organized files
- **Automated workflows**: Scripts reduce manual work and ensure consistency

### 12. Conclusion

The recommendations above provide a comprehensive approach to making ZMK keymaps more manageable and visually friendly. By following these suggestions, the repository will benefit from:

1. **Better organization**: Clear separation of concerns and modular structure
2. **Improved tooling**: Syntax highlighting, formatting, and validation
3. **Visual documentation**: Keymap visualizations for easier understanding
4. **Automated workflows**: Scripts for maintenance and validation

The implementation can be done incrementally, starting with the high-priority items and gradually adding more advanced features as needed.