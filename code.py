"""
File Name: code.py
Description: A program to control an LED strip using an RP2040 SEEED chip.
             The program smoothly cycles the LED colors between two colors or
             a pattern.
Author: Richard Berrill
Date Created: September 3, 2023
Last Modified: September 4, 2023
Version: 0.1.1
License: Creative Commons Attribution 4.0 International License (CC BY 4.0)
         For full license details, please refer to the LICENSE file or visit:
         https://creativecommons.org/licenses/by/4.0/
Contact: rberrill@gmail.com
Dependencies: Adafruit_NeoPixel library
"""

import board
import neopixel
import time
import random

# Constants
PIN = board.D0
NUMPIXELS = 13
PATTERN_LENGTH = 7
LED_PATTERN_INTERVAL = 0.01  # fractional seconds
DEBUG = False  # Set to True for debug messages, False to disable
MODE = "shimmer"  # Set to "pattern" or "shimmer"

# Constants for saber_flash
FLASH_COLOR = (240, 255, 0, .5)  # Yellow color
SABER_FLASH_ENABLED = True
SABER_FLASH_CHANCE = 2  # saber flash chance out of 1000
MIN_FLASHES = 4  # Minimum number of flashes
MAX_FLASHES = 10  # Maximum number of flashes
MIN_FLASH_DELAY = 0.0001  # Min delay between flashes (seconds)
MAX_FLASH_DELAY = 0.005  # Max delay between flashes (seconds)
MIN_FLASH_SPREAD = 3  # Minimum number of LEDs the flash will spread to
MAX_FLASH_SPREAD = NUMPIXELS  # Maximum number of LEDs the flash will spread to

# NEOPIXEL setup
strip = neopixel.NeoPixel(PIN, NUMPIXELS, brightness=1.0, auto_write=False)

# Pattern: (R, G, B, Brightness)
pattern = [
    (255, 0, 0, 1),
    (255, 140, 0, 1),
    (255, 255, 0, 1),
    (0, 255, 0, 1),
    (0, 0, 255, 1),
    (255, 0, 255, 1),
    (0, 255, 255, 1),
]

# Background color: (R, G, B, Brightness)
bgColor = (245, 255, 200, 1)

# Shimmer colors
shimmerColor1 = (0, 149, 255, 0.8)
shimmerColor2 = (0, 174, 255, 0.6)

# Pixel order from left to right
pixelOrder = [9, 10, 8, 11, 7, 12, 6, 5, 0, 4, 1, 3, 2]

# Global frame counter for LED pattern
ledPatternFrameCounter = 0

# Variables for non-blocking delay
ledPatternPreviousMillis = time.monotonic()

# Initialize current and target colors for each pixel
currentColors = [bgColor for _ in range(NUMPIXELS)]
targetColors = [random.choice([shimmerColor1, shimmerColor2])
                for _ in range(NUMPIXELS)]

# Initialize step sizes for each pixel
stepSizes = [
    random.uniform(0.01, 0.1) for _ in range(NUMPIXELS)
]  # Random step sizes between 0.01 and 0.1

def debugPrint(message):
    if DEBUG:
        print(message)

def displayPattern(startPos):
    for j in range(PATTERN_LENGTH):
        pixelPos = startPos - j
        if 0 <= pixelPos < NUMPIXELS:
            r, g, b, brightness = pattern[j]
            strip[pixelOrder[pixelPos]] = (
                int(r * brightness),
                int(g * brightness),
                int(b * brightness),
            )
            debugPrint(
                f"LED {pixelOrder[pixelPos]} turned ON with color (R: {r}, G: {g}, B: {b}) and brightness {brightness}"
            )

def setBackground():
    r, g, b, brightness = bgColor
    for k in range(NUMPIXELS):
        strip[pixelOrder[k]] = (
            int(r * brightness),
            int(g * brightness),
            int(b * brightness),
        )
        debugPrint(
            f"LED {pixelOrder[k]} set to background with color (R: {r}, G: {g}, B: {b}) and brightness {brightness}"
        )

def adjustColor(current, target, step):
    """Adjust the current color towards the target color by a given step."""
    return tuple(current[i] + step * (target[i] - current[i]) for i in range(3))

def displayShimmer():
    if SABER_FLASH_ENABLED and random.randint(1, 1000) <= SABER_FLASH_CHANCE:
        saber_flash()
    else:
        for k in range(NUMPIXELS):
            # Check if current color is close to target color
            if all(abs(currentColors[k][i] - targetColors[k][i]) < 1 for i in range(3)):
                targetColors[k] = random.choice([shimmerColor1, shimmerColor2])
                stepSizes[k] = random.uniform(
                    0.001, 0.005
                )  # Assign a new random step size
            # Adjust current color towards target color
            # using the pixel-specific step size
            r, g, b = adjustColor(
                currentColors[k][:3], targetColors[k][:3], stepSizes[k]
            )
            brightness = targetColors[k][3]
            strip[pixelOrder[k]] = (
                int(r * brightness),
                int(g * brightness),
                int(b * brightness),
            )

            # Update current color
            currentColors[k] = (r, g, b, brightness)
            debugPrint(
                f"LED {pixelOrder[k]} shimmering with color (R: {int(r)}, G: {int(g)}, B: {int(b)}) and brightness {brightness}"
            )

def set_led_color(led_index, color):
    """Set the color of a specific LED."""
    if 0 <= led_index < NUMPIXELS:
        r, g, b, brightness = color
        strip[pixelOrder[led_index]] = (int(r * brightness), int(g * brightness), int(b * brightness))
        strip.show()

def flash_leds(start_led, flash_spread, color):
    """Illuminate the LEDs based on the starting LED and flash spread."""
    for step in range(-flash_spread, flash_spread + 1):
        set_led_color(start_led + step, color)

def saber_flash():
    # Randomly select a starting LED
    start_led = random.randint(0, NUMPIXELS - 1)

    # Determine the number of flashes and the delay between them
    num_flashes = random.randint(MIN_FLASHES, MAX_FLASHES)

    for _ in range(num_flashes):
        # Randomly determine the extent of the flash spread
        flash_spread = random.randint(MIN_FLASH_SPREAD, MAX_FLASH_SPREAD)

        # Illuminate the LEDs
        flash_leds(start_led, flash_spread, FLASH_COLOR)
        time.sleep(random.uniform(MIN_FLASH_DELAY, MAX_FLASH_DELAY))

        # Turn off the LEDs
        flash_leds(start_led, flash_spread, (0, 0, 0, 1))
        time.sleep(random.uniform(MIN_FLASH_DELAY, MAX_FLASH_DELAY))

while True:
    currentMillis = time.monotonic()
    if currentMillis - ledPatternPreviousMillis >= LED_PATTERN_INTERVAL:
        ledPatternPreviousMillis = currentMillis

        if MODE == "pattern":
            debugPrint(f"Displaying pattern frame {ledPatternFrameCounter}")
            setBackground()
            displayPattern(ledPatternFrameCounter)
            strip.show()

            ledPatternFrameCounter += 1
            if ledPatternFrameCounter >= NUMPIXELS + PATTERN_LENGTH:
                ledPatternFrameCounter = 0
                debugPrint("Pattern completed, restarting...")
        elif MODE == "shimmer":
            displayShimmer()
            strip.show()
