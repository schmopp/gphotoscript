from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid, signal.SIGKILL)

shot_date = datetime.now().strftime("%m-%d-%Y")
picID = "testShots"

clearCommand = ["--folder", "/store_00020001/DCIM/110CANON", \
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" + folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Folder already exists!")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    sleep(3)
    gp(clearCommand)

killgphoto2Process()
gp(clearCommand)
createSaveFolder()
while True:
    captureImages()
    sleep(5)
