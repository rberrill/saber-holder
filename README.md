# NEOPIXEL Pattern Display for RP2040

## Description

This repository hosts code designed for the SEEED RP2040 microcontroller to control a series of NEOPIXELS LEDs. The primary feature is a dynamic lighting effect that displays a shifting pattern across the LEDs. As the pattern progresses, it begins with the rightmost pixel of the pattern on the first NEOPIXEL (ID 0) and concludes when the leftmost pixel of the pattern reaches the last NEOPIXEL. Once the pattern completes its cycle, it restarts, creating a continuous loop of the shifting pattern effect.

## Purpose

The primary purpose of this code is to enhance visual displays by providing a dynamic lighting effect using NEOPIXELS. The shifting pattern effect can be used in various applications, including decorative displays, signage, or any other project that requires dynamic LED patterns.

## Features

- Uses the Adafruit NEOPIXEL library to control the LEDs.
- The order of the NEOPIXELS in the circuit can be customized.
- Constants in the code allow for easy modification of the number of NEOPIXELS, frame rate, pattern, background color, and brightness.
- Modular code structure for easy integration and expansion.

## Version

Current Version: **0.1.2**

### Changelog

- **0.1.2** - Removed pattern method for now.
- **0.1.1** - Added shimmer and saber flash modes.
- **0.1.0** - Initial release with basic pattern shifting functionality.

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
