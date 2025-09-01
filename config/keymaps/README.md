# ZMK Keymap Structure

This directory contains the modular ZMK keymap configuration organized according to best practices.

## Directory Structure

```
keymaps/
├── base/
│   ├── base.keymap          # Base keymap with common layers
│   ├── behaviors.dtsi       # Common behaviors
│   └── combos.dtsi          # Common combos
├── keyboards/
│   ├── corne/
│   │   ├── corne.keymap     # Corne-specific keymap
│   │   └── corne.conf       # Corne-specific config
│   └── mono_corne/
│       ├── mono_corne.keymap
│       └── mono_corne.conf
└── layers/
    ├── symbols.keymap       # Symbol layer definitions
    ├── numbers.keymap       # Number layer definitions
    └── media.keymap         # Media layer definitions
```

## Usage

Each keyboard-specific keymap includes the base keymap and then overrides any keyboard-specific configurations.

## Keymap Visualization

The keymap diagram is automatically generated and updated via GitHub Actions whenever changes are pushed to keymap files.