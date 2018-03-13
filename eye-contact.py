from subprocess import call, check_output
from pygame import key
from multiprocessing import Process

def start_cupture_video():
    '''
    use shell command 'raspivid' 
    '''
    call(['raspivid', '-t', '6000', '-n','-o', 'eye.h264']) # run background

def get_cupture_PID():
    '''
    find PID of raspivid using shell command 'pgrep raspivid'
    '''
    pid = check_output(["pgrep", "raspivid"])
    pid = pid[:-1] # drop the last char '\n'
    return pid

def stop_cupture_video():
    '''
    kill the PID using 'kill PID_NUM'
    '''
    pid = get_cupture_PID() # get_PID return a string
    call(["kill", pid])


    
def convert_video():
    '''
    use shell command 'MP4Box -add video.h264 video.mp4'
    sudo apt-get install -y gpac
    '''
    clear_eye_mp4_history()
    call(["MP4Box", "-add", "eye.h264", "eye.mp4"])

def clear_eye_mp4_history():
    '''
    rm the last eye*
    '''
    call(["rm", "eye.mp4"])


def display_video():
    '''
    use shell command 'omxplayer'
    '''
    call(['omxplayer', '--loop', 'eye.mp4'])

def trigger():
    '''
    read a trigger stat
    return 0 or 1 to close or open this system
    '''
    button = 0
    if button_press:
        button +=1
        #
        if button == 3:
            button = 0

def main():
    p_display = Process(target=display_video)
    p_cupture = Process(target=start_cupture_video)
    #display_video()
    #start_cupture_video()
    p_display.start()
    p_cupture.start()
        
       

# option
def eye_trigger():
    '''
    using simplecv to detact eye blink
    return 0 or 1 to close or open this system
    '''


if __name__ == "__main__":
    main()
