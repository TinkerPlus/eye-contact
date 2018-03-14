from subprocess import call, check_output
#from pygame import key
from multiprocessing import Process
import RPi.GPIO as GPIO
from time import sleep
       
       
def start_cupture_video():
    '''
    use shell command 'raspivid' 
    '''
    call(['raspivid', '-t', '10000', '-n','-o', 'eye.h264']) 

def get_cupture_PID():
    '''
    find PID of raspivid using shell command 'pgrep raspivid'
    '''
    try:
        pid = check_output(["pgrep", "raspivid"])
        pid = pid[:-1] # drop the last char '\n'
    except:
        pid = 0
    return pid

def get_display_PID():
    '''
    find PID of raspivid using shell command 'pgrep raspivid'
    '''
    try:
        pid = check_output(["pgrep", "omxplayer"])
        pid = pid[:-1] # drop the last char '\n'
    except Exception:
        #print 'pid is not exist'
        pid = 0
    return pid

def stop_cupture_video():
    '''
    kill the PID using 'kill PID_NUM'
    '''
    pid =  get_cupture_PID() # get_PID return a string
    if (pid != 0):
        call(["kill", pid])
    else:
        pass
    
def stop_display_video():
    '''
    kill the PID using 'kill PID_NUM'
    '''
    pid = get_display_PID()
    if(pid != 0):
        call(["kill", pid])
    else:
        pass
    
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
    #call(['omxplayer', '--loop', 'eye.mp4'])
    call(['omxplayer','eye.mp4'])
def trigger():
    '''
    read a trigger stat
    return 0 or 1 to close or open this system
    '''
    global state
    global input_signal
    if GPIO.event_detected(input_signal):
        if state < 1:
            state += 1
        else:
            state = 0


def rising_callback(rising_channel):
    p_display = Process(target=display_video)
    p_cupture = Process(target=start_cupture_video)
    p_display.start()
    p_cupture.start()    


def falling_callback(falling_channel):
    stop_cupture_video()
    stop_display_video()
    convert_video()
    
def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global input_signal
    input_signal = 22
    GPIO.setup(input_signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(input_signal, GPIO.BOTH, bouncetime=200)
    
def setup():
    gpio_setup()
    global state 
    state = 0

def loop():
    global state
    while True:
        trigger()
        if state == 0:
            '''
            kill display and cupture
            then covert h264 to mp4
            '''
            #stop_cupture_video()
            #stop_display_video()
            #convert_video()
            print ('off')
            
        elif state == 1:
            '''
            display last person's eyes as cupture current person's ones 
            '''
            #p_display = Process(target=display_video)
            #p_cupture = Process(target=start_cupture_video)
            #p_display.start()
            #p_cupture.start()
            print ('on')
            
        else:
            pass
    time.sleep(0.001)
    
def start_system():
    p_display = Process(target=display_video)
    p_cupture = Process(target=start_cupture_video)
    p_display.start()
    p_cupture.start()

def stop_system():
    stop_cupture_video()
    stop_display_video()
    convert_video()
    
def main():
    input_signal = 22
    gpio_setup()
    state = 0
    while True:
        if GPIO.event_detected(input_signal):
            if state < 1:
                state += 1
            else:
                state = 0
                
            if state == 1:
                start_system()
            elif state == 0:
                stop_system()
            else:
                pass
        else:
            pass
            
        sleep(0.001)
# option
def eye_trigger():
    '''
    using simplecv to detact eye blink
    return 0 or 1 to close or open this system
    '''


if __name__ == "__main__":
    main()
