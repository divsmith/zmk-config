#!/bin/bash
# ZMK Keymap Utilities

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

case "$1" in
    validate)
        echo "Validating keymap files..."
        find "$PROJECT_DIR/config/keymaps" -name "*.keymap" -o -name "*.dtsi" | while read file; do
            echo "Checking $file"
            python3 "$SCRIPT_DIR/validate_keymap.py" "$file"
        done
        ;;
    format)
        echo "Formatting keymap files..."
        find "$PROJECT_DIR/config/keymaps" -name "*.keymap" -o -name "*.dtsi" | while read file; do
            echo "Formatting $file"
            python3 "$SCRIPT_DIR/format_keymap.py" "$file"
        done
        ;;
    visualize)
        echo "Generating keymap visualization..."
        if command -v keymap &> /dev/null; then
            keymap parse "$PROJECT_DIR/config/keymaps/base/base.keymap" | keymap draw > "$PROJECT_DIR/keymap.svg"
            echo "Keymap visualization saved to keymap.svg"
        else
            echo "keymap-drawer not found. Please install it with: pip install keymap-drawer"
        fi
        ;;
    *)
        echo "ZMK Keymap Utilities"
        echo "Usage: $0 {validate|format|visualize}"
        echo "  validate  - Validate all keymap files"
        echo "  format    - Format all keymap files"
        echo "  visualize - Generate keymap visualization (requires keymap-drawer)"
        ;;
esac