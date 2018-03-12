from subprocess import call
from pygame import key


def cupture_video():
    '''
    use shell command 'raspivid' 
    '''
    call(['raspivid', '-o', 'eye.h264'])

def convert_video():
    '''
    use shell command 'MP4Box -add video.h264 video.mp4'
    sudo apt-get install -y gpac
    '''
    call(["MP4Box", "-add", "eye.h264", "eye.mp4"])

def clear_history():
    '''
    rm the last eye*
    '''
    call(["rm", "eye.mp4"])


def display_video():
    '''
    use shell command 'omxplayer'
    '''
    call(['omxplayer', 'eye.mp4'])


def trigger():
    '''
    read a trigger stat
    return 0 or 1 to close or open this system
    '''
    pass

def main():
    cupture_video()
    clear_history() # insure the eye.mp4 is not exist.
    convert_video()
    display_video()


# option
def eye_trigger():
    '''
    using simplecv to detact eye blink
    return 0 or 1 to close or open this system
    '''
