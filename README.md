# ZMK Configuration

A sophisticated ZMK (Zephyr Keyboard Firmware) configuration supporting both Mono and Split Corne keyboards with advanced features and custom behaviors.

## Supported Keyboards

### Mono Corne
- **Controller**: RP2040 Zero (e.g., Adafruit RP2040 Zero)
- **Layout**: 4x5+3 (36-key Corne layout with thumb cluster)
- **Features**: Faster tap timing for responsive feel

### Split Corne
- **Controllers**:
  - Left/Right halves: nice!nano v2
  - Dongle: Raytac MDBT50Q-RX
- **Layout**: 6x5 split Corne layout with thumb clusters
- **Features**: Central dongle mode with enhanced Bluetooth capabilities

## Key Features

### Advanced Key Behaviors
- **Hold-Tap Configurations**: Multiple custom hold-tap behaviors optimized for different use cases
- **Balanced Homerow Mods**: Efficient modifier keys on home row using `bhm` behavior
- **Smart Space/Backspace**: Spacebar acts as backspace when held, shifted becomes Hyper key
- **Adaptive Shift Keys**: Shift becomes brackets when held
- **Double-Tap Comma**: Double-tap comma triggers caps word and deletes previous character

### Layer System
1. **Default Layer**: QWERTY with homerow mods
2. **Symbols Layer** (1): Punctuation and symbols
3. **Numbers Layer** (2): Numeric pad layout
4. **Arrows Layer** (3): Arrow key navigation
5. **Nav Layer** (4): Advanced navigation with Hyper/Meh combos
6. **Media Layer** (5): Media controls
7. **Bluetooth Layer** (6): Device switching and management
8. **Empty Layer**: Available for custom configuration

### Smart Combinations
- **Space+Tab**: Triggers caps word mode
- **Caps Word**: Automatic capitalization with smart continue list
- **Layer Tap Fast**: Quick layer access with optimized timing
- **Hyper/Meh Keys**: Advanced chorded key combinations

## Project Structure

```
zmk-config/
├── config/
│   ├── base_36.keymap          # Main keymap with all layers
│   ├── mono_corne.keymap       # Mono-specific overrides
│   ├── corne.keymap           # Split-specific overrides
│   └── west.yml               # ZMK manifest with custom components
├── boards/
│   └── shields/
│       ├── mono_corne/        # Mono Corne board definitions
│       └── corne/             # Split Corne board definitions
├── build.yaml                 # GitHub Actions build matrix
└── README.md                  # This file
```

## Setup Instructions

### Prerequisites
- ZMK development environment set up
- West tool installed
- Compatible hardware (see Supported Keyboards section)

### Building Firmware

#### Using GitHub Actions (Recommended)
1. Push changes to this repository
2. GitHub Actions will automatically build firmware for all supported configurations
3. Download the appropriate `.uf2` file from the Actions tab

#### Local Build
```bash
# Update dependencies
west update

# Build for Mono Corne
west build -b rp2040_zero -- -DSHIELD=mono_corne

# Build for Split Corne (Left)
west build -b nice_nano_v2 -- -DSHIELD=corne_left -DCONFIG_ZMK_SPLIT=y -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n

# Build for Split Corne (Right)
west build -b nice_nano_v2 -- -DSHIELD=corne_right -DCONFIG_ZMK_SPLIT=y -DCONFIG_ZMK_SPLIT_ROLE_CENTRAL=n

# Build for Corne Dongle
west build -b raytac_mdbt50q_rx -- -DSHIELD=corne_dongle
```

### Flashing Firmware

#### RP2040 Zero (Mono Corne)
1. Connect RP2040 Zero while holding BOOTSEL button
2. Drag and drop the `.uf2` file to the mounted drive

#### nice!nano v2 (Split Corne)
1. Use a programmer (like UF2 bootloader) or
2. Use OTA updates if already configured with ZMK

#### Raytac Dongle
1. Connect via USB while in bootloader mode
2. Flash the appropriate firmware file

## Custom Components

This configuration uses several custom ZMK components:
- **zmk-component-raytac-dongle**: Enhanced dongle functionality
- **zmk-component-rp2040-zero**: RP2040 controller support
- **zmk-adaptive-key**: Adaptive key behaviors (e.g., double-tap comma)

## Keymap Details

### Home Row Modifiers
- `A`: Left Ctrl
- `S`: Left Alt
- `D`: Left Shift
- `F`: Left GUI
- `J`: Right GUI
- `K`: Right Shift
- `L`: Right Alt
- `;`: Right Ctrl

### Special Keys
- **Space**: Tap = Space, Hold = Backspace, Shift+Hold = Hyper
- **Esc**: Layer tap to Symbols layer
- **Enter**: Layer tap to Numbers layer
- **Comma**: Double-tap = Caps Word + Backspace

### Layer Access
- **Symbols**: Esc (hold)
- **Numbers**: Enter (hold)
- **Arrows**: V (hold)
- **Navigation**: E (hold)
- **Bluetooth**: N (hold)
- **Media**: M (hold)

## Bluetooth Configuration

The split configuration supports up to 5 Bluetooth profiles:
- **Layer 6**: Access Bluetooth switching controls
- **BT_CLR**: Clear all pairings
- **BT_SEL 0-4**: Switch between profiles
- **Bootloader**: Enter bootloader mode for flashing

## Development Notes

### Recent Optimizations
- Consolidated layer hold timing for better responsiveness
- Optimized tap timing differences between mono and split configurations
- Enhanced comma caps feature with adaptive behavior

### Configuration Differences
- **Mono Corne**: 150ms tap timing for more responsive feel
- **Split Corne**: 200ms tap timing with additional safeguards for reliability

## License

This configuration follows the ZMK project's MIT license. See individual component licenses for details.

## Contributing

When making changes:
1. Test on both mono and split configurations if applicable
2. Update build.yaml if adding new board/shield combinations
3. Update this README if adding significant new features