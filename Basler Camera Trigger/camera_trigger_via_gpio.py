from pypylon import pylon
import cv2
import gpiod
import time
import threading
import os

'''
Trigger Activation Format:
Rising Edge - only works when 0 to 1
Falling Edge
Any Edge
Level High
Level Low
'''

cv2.namedWindow("Camera Trigger", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera Trigger", (1024, 1024))

devices = list(pylon.TlFactory.GetInstance().EnumerateDevices())
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[0]))
camera.Open()

camera.UserSetSelector.Value = "Default"
camera.UserSetLoad.Execute()

camera.TriggerSelector.Value = "FrameStart"
camera.TriggerMode.Value = "On"
camera.TriggerSource.Value = "Line1"
camera.TriggerActivation.Value = "RisingEdge"
# camera.TriggerDelay.Value = 1000 # in microseconds (1000us = 1ms)

camera.PixelFormat.Value = "BayerGB8"
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
# camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

camera.ExposureAuto.Value="Off"
camera.ExposureTime.Value=10000

running = True

chip = gpiod.Chip("/dev/gpiochip0")
line = 51
capturing_time = 0.05
delay_time = 3

config = gpiod.LineSettings()
config.direction = gpiod.line.Direction.OUTPUT

request = chip.request_lines(
    consumer="strobe",
    config={line:config}
)

camera.ExposureTime.Value = 20000

latest_img = None
img_lock = threading.Lock()

def _cam_grabbing():
    global running, latest_img
    while camera.IsGrabbing() and running:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_Return)
        if grabResult and grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            with img_lock:
                latest_img = image.GetArray()
            grabResult.Release()

cam_thread = threading.Thread(target=_cam_grabbing)
cam_thread.start()

try:
    while True:
        request.set_values({line: gpiod.line.Value.ACTIVE}) 
        time.sleep(capturing_time)
        request.set_values({line: gpiod.line.Value.INACTIVE})
        
        with img_lock:
            if latest_img is not None:
                cv2.imshow("Camera Trigger", latest_img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(delay_time) 
except KeyboardInterrupt:
    print("Exit")
finally:
    running = False
    cam_thread.join()
    request.release()

    camera.StopGrabbing()
    camera.Close()
    cv2.destroyAllWindows()
