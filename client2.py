import requests
from goprocam import GoProCamera
from goprocam import constants
import time
import requests
import os
start = time.time()
print("hello")
end = time.time()
print(end - start)

urlup = 'http://127.0.0.1:5000/uploadimage'

# Connect the camera
my_gopro = GoProCamera.GoPro()

# Delete all the media
time.sleep(1)
my_gopro.delete('all')

# Take pics, send and delete
cont = 0
while cont < 2:
    time.sleep(0.5)
    my_gopro.take_photo()
    time.sleep(1)
    media = my_gopro.downloadLastMedia()
    media_name = my_gopro.getMediaInfo("file")
    files = {'image': open(f'100GOPRO-{media_name}','rb')}
    r = requests.post(urlup, files=files)
    files.clear()
    filename = f'100GOPRO-{media_name}'
    os.remove(filename)
    cont = cont + 1

# Send device data
rem_space = my_gopro.parse_value("rem_space",my_gopro.getStatus(constants.Status.Status, constants.Status.STATUS.RemainingSpace))
battery_left = my_gopro.parse_value("battery",my_gopro.getStatus(constants.Status.Status, constants.Status.STATUS.BatteryLevel))
clients_connected = str(my_gopro.getStatus(constants.Status.Status, constants.Status.STATUS.IsConnected))
pictures_left = str(my_gopro.getStatus(constants.Status.Status,constants.Status.STATUS.RemPhotos))
camera_SSID = str(my_gopro.getStatus(constants.Status.Status,constants.Status.STATUS.CamName))
serial_number = my_gopro.infoCamera(constants.Camera.SerialNumber)


url='http://127.0.0.1:5000/json'

myobj = {
    "name": "Raspberry pi 4",
    "message": "Gopro hero 4",
    "rem_space": rem_space,
    "battery_left": battery_left,
    "clients_connected": clients_connected,
    "pictures_left": pictures_left,
    "camera_SSID": camera_SSID,
    "serial_number": serial_number
}
start = time.time()
r = requests.post(url, json=myobj)
end = time.time()
print(end - start)
#print(r.status_code)
#print(r.text)