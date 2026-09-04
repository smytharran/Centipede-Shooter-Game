from adafruit_circuitplayground import cp

import time

class SensorLightDisplay:

    acceleration_peak = 9.81

    def __init__(self, brightness):
        self.pixels_off_state = [0, 0, 0]
        self.pixel_amount = len(cp.pixels)
        self.pixel_amount_half = len(cp.pixels) // 2
        cp.pixels.brightness = brightness
        cp.pixels.auto_write = False

    def control_feedback_x(self, acceleration_x, colour):
        x = acceleration_x
        flipped_x = abs(x)
        last_pixel_location = 0
        if x < -SensorLightDisplay.acceleration_peak or x > SensorLightDisplay.acceleration_peak:
            return

        if flipped_x < SensorLightDisplay.acceleration_peak:
            last_pixel_location = int(flipped_x * self.pixel_amount_half / SensorLightDisplay.acceleration_peak)

            if x < -1:
                cp.pixels.fill(self.pixels_off_state)
                for pixel in range(self.pixel_amount_half):
                    if pixel <= last_pixel_location:
                        cp.pixels[9 - pixel] = colour
                    else:
                        cp.pixels[9 - pixel] = self.pixels_off_state
            elif x > 1:
                cp.pixels.fill(self.pixels_off_state)
                for pixel in range(self.pixel_amount_half):
                    if pixel <= last_pixel_location:
                        cp.pixels[pixel] = colour
                    else:
                        cp.pixels[pixel] = self.pixels_off_state
            else:
                cp.pixels.fill(self.pixels_off_state)
        else:
            cp.pixels.fill(self.pixels_off_state)
        cp.pixels.show()
        time.sleep(0.1)

    def advanced_control_feedback(self, acceleration_x):
        x = acceleration_x
        tilt = abs(x)
        peak = SensorLightDisplay.acceleration_peak
        cp.pixels.fill(self.pixels_off_state)

        if x < -peak or x > peak:
            cp.pixels.show()
            return

        if tilt <= 3:
            cp.pixels.show()
            return

        start_tilt = 3
        tilt_past_start = tilt - start_tilt
        tilt_range = peak - start_tilt

        strength = tilt_past_start / tilt_range

        if strength < 0:
            strength = 0
        if strength > 1:
            strength = 1

        if strength < 1/3:
            max_offset = 0
        elif strength < 2/3:
            max_offset = 1
        else:
            max_offset = 2

        start_colour = (0, 0, 255)  # blue
        end_colour = (128, 0, 191)

        start_r, start_g, start_b = start_colour
        end_r, end_g, end_b = end_colour

        r = start_r + (end_r - start_r) * strength
        g = start_g + (end_g - start_g) * strength
        b = start_b + (end_b - start_b) * strength

        mapped_colour = (int(r), int(g), int(b))

        if x < -3:
            center_pixel = 7
            min_pixel = 5
            max_pixel = 9
        elif x > 3:
            center_pixel = 2
            min_pixel = 0
            max_pixel = 4

        for offset in range(max_offset + 1):
            left = center_pixel - offset
            right = center_pixel + offset

            if min_pixel <= left <= max_pixel:
                cp.pixels[left] = mapped_colour
            if min_pixel <= right <= max_pixel:
                cp.pixels[right] = mapped_colour

        cp.pixels.show()
        time.sleep(0.1)
