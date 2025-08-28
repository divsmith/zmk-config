# ZMK Keymap Recommendations

This document provides recommendations for improving the readability and maintainability of ZMK keymap files.

## 1. Use a Visual Layout in Your Keymap

The biggest improvement you can make to your keymap is to format it in a way that visually represents the physical layout of your keyboard. This makes it much easier to understand and edit your keymap.

Instead of a long list of bindings, you can use comments and careful spacing to create a visual grid.

**Recommendation:** Reformat your `base_36.keymap` to visually represent your Corne keyboard layout.

Here's an example of how you can format your `default_layer` to match the physical layout of your Corne keyboard. This format is much more readable and easier to maintain.

```dts
/ {
    keymap {
        compatible = "zmk,keymap";

        default_layer {
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

        // ... other layers
    };
};
```

## 2. Use Macros for Cleaner Code

You are already using macros for `HYPER` and `MEH`. You can extend this practice to simplify your keymap further. For example, you can create macros for your layer taps and home row mods.

**Recommendation:** Use C preprocessor macros (`#define`) to create aliases for complex or frequently used key bindings.

Here are some examples based on your current keymap:

```c
// In base_36.keymap

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

Using these macros will make your keymap significantly cleaner and easier to read:

```dts
default_layer {
    bindings = <
&kp Q  &kp W  NAV_E   &kp R  &kp T      &kp Y  &kp U  &bhm RC(RALT) I  &kp O  &kp P
HC_A   &kp S  HS_D    HG_F   &kp G      &kp H  H_RGUI_J   H_RSFT_K   &kp L  H_RCTL_APOS
H_A_Z  &kp X  &kp C   ARR_V  &kp B      BT_N   MED_M      &kp COMMA  &kp DOT  H_RALT_FSLH
           &trans  SYM_ESC  &kp RSHFT  &spaceb  NUM_RET  &trans
    >;
};
```

## 3. Visualize Your Keymap with `keymap-drawer`

`keymap-drawer` is a powerful tool that can generate a visual representation of your keymap. This is a great way to get an overview of your layers and bindings, and it can be included in your repository's documentation to make it easier for others to understand your layout.

**Recommendation:** Use `keymap-drawer` to generate an SVG image of your keymap and include it in your `README.md`. You can even automate this process with GitHub Actions.

### 3.1. Manual Usage

1.  **Install `keymap-drawer`:**

    ```bash
    pip install keymap-drawer
    ```

2.  **Create a `keymap_drawer.config.yaml` file:**

    This file tells `keymap-drawer` how to parse your `.keymap` file.

    ```yaml
    zmk:
      # Path to your ZMK app folder, with which you can use #include <behaviors.dtsi>
      # You can set this to a local path on your machine, or a URL to a github repo
      zmk_app: "https://github.com/zmkfirmware/zmk/tree/main/app"

      # Path to your ZMK config folder. Like zmk_app, you can use a local path or a github URL
      # This is used to resolve local #include "my_keymap.keymap"
      zmk_config: "https://github.com/parker/zmk-config/tree/main/config"

      # keymap file to parse
      keymap: "base_36.keymap"

      # (optional) A list of C #define's to add to the beginning of the keymap file
      # This can be useful to resolve "undefined macro" errors
      defines:
        - "HYP=LS(LC(LA(LGUI)))"
        - "HYPER(key)=LS(LC(LA(LG(key))))"
        - "MEH(key)=LS(LC(LA(key)))"
    ```

3.  **Generate the SVG:**

    ```bash
    keymap-drawer parse-zmk --config-file keymap_drawer.config.yaml > my_keymap.yaml
    keymap-drawer draw my_keymap.yaml > my_keymap.svg
    ```

### 3.2. Automated Workflow

You can automate the process of generating and updating your keymap diagram using a GitHub Actions workflow. Here is an example workflow that you can add to `.github/workflows/keymap.yml`:

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

## 4. Use a Graphical Keymap Editor

For users who prefer a more visual approach, there are online keymap editors that provide a graphical interface for editing your keymap. These tools allow you to see your keyboard layout and assign keys, macros, and behaviors without writing any code. A popular one is [Nick Coutsos's Keymap Editor](https://nickcoutsos.github.io/keymap-editor/).

**Recommendation:** Use a graphical keymap editor for a more user-friendly experience. These editors can connect directly to your GitHub repository and commit changes automatically.