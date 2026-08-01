import gpiod
import time

chip = gpiod.Chip("/dev/gpiochip0")
line = 105

config = gpiod.LineSettings()
config.direction = gpiod.line.Direction.INPUT
config.edge_detection = gpiod.line.Edge.BOTH

request = chip.request_lines(
    consumer="sensor input",
    config={line:config}
)

try:
    while True:
        if request.wait_edge_events():
            for event in request.read_edge_events():
                if event.event_type == gpiod.EdgeEvent.Type.FALLING_EDGE:
                    print(f"[{time.time}] Falling edge")
                elif event.event_type == gpiod.EdgeEvent.Type.RISING_EDGE:
                    print(f"[{time.time}] Rising edge")

except KeyboardInterrupt:
    print("Exit")
finally:
    request.release()