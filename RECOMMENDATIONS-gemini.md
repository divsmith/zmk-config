# ZMK Keymap Recommendations

This document provides recommendations for improving the readability and maintainability of ZMK keymap files.

## 1. Use `matrix_transform` for a Visual Layout

The ZMK documentation shows that you can use a `matrix_transform` to define a visual layout of your keyboard within the `.keymap` file itself. This makes it much easier to see the physical layout of the keys and how they correspond to the bindings.

**Recommendation:** Use a `matrix_transform` to create a visual representation of your keymap.

**Example from the ZMK documentation:**

```dts
/ {
    chosen {
        zmk,kscan = &kscan0;
        zmk,matrix-transform = &default_transform;
    };

    kscan0: kscan {
        compatible = "zmk,kscan-gpio-matrix";
        // define row-gpios with 5 elements and col-gpios with 4...
    };

    default_transform: matrix_transform {
        compatible = "zmk,matrix-transform";
        rows = <5>;
        columns = <4>;
        // ┌───┬───┬───┬───┐
        // │NUM│ / │ * │ - │
        // ├───┼───┼───┼───┤
        // │ 7 │ 8 │ 9 │ + │
        // ├───┼───┼───┤   │
        // │ 4 │ 5 │ 6 │   │
        // ├───┼───┼───┼───┤
        // │ 1 │ 2 │ 3 │RET│
        // ├───┴───┼───┤   │
        // │ 0     │ . │   │
        // └───────┴───┴───┘
        map = <
            RC(0,0) RC(0,1) RC(0,2) RC(0,3)
            RC(1,0) RC(1,1) RC(1,2) RC(1,3)
            RC(2,0) RC(2,1) RC(2,2)
            RC(3,0) RC(3,1) RC(3,2) RC(3,3)
            RC(4,0)         RC(4,1)
        >;
    };
};
```

## 2. Use a Graphical Keymap Editor

For users who prefer a more visual approach, there are online keymap editors that provide a graphical interface for editing your keymap. These tools allow you to see your keyboard layout and assign keys, macros, and behaviors without writing any code. A popular one is [Nick Coutsos's Keymap Editor](https://nickcoutsos.github.io/keymap-editor/).

**Recommendation:** Use a graphical keymap editor for a more user-friendly experience.

## 3. Visualize Your Keymap with `keymap-drawer`

`keymap-drawer` is a tool that can generate a visual representation of your keymap. This is a great way to get an overview of your layers and bindings, and it can be included in your repository's documentation to make it easier for others to understand your layout.

**Recommendation:** Use `keymap-drawer` to generate an SVG image of your keymap and include it in your `README.md`.

`keymap-drawer` works by parsing a YAML file that describes your keymap. You can create this YAML file manually, or you can use the tool's ability to parse a ZMK keymap file.

**Example Usage:**

1.  **Install `keymap-drawer`:**

    ```bash
    pip install keymap-drawer
    ```

2.  **Create a YAML file to describe your keymap:**

    You can find the specification for the YAML format in the [`keymap-drawer` documentation](https://github.com/caksoylar/keymap-drawer/blob/main/KEYMAP_SPEC.md).

3.  **Generate the SVG:**

    ```bash
    keymap-drawer draw my_keymap.yaml > my_keymap.svg
    ```

There is also a [live demo](https://caksoylar.github.io/keymap-drawer/app/) available where you can test the tool and get a feel for how it works.
