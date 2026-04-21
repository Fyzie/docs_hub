import gpiod
import time

chip = gpiod.Chip("/dev/gpiochip0")
line = 51

config = gpiod.LineSettings()
config.direction = gpiod.line.Direction.OUTPUT

request = chip.request_lines(
    consumer="strobe",
    config={line:config}
)

try:
    while True:
        request.set_values({51:gpiod.line.Value.ACTIVE}) 
        time.sleep(0.01)
        request.set_values({51:gpiod.line.Value.INACTIVE})
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Exit")
finally:
    request.release()