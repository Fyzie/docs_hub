from pypylon import pylon
import cv2
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

# camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_Return)

    if grabResult:
        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            cv2.imshow("Camera Trigger", img)
        
        grabResult.Release()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.Close()
cv2.destroyAllWindows()
