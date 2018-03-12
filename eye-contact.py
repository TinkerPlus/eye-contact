from subprocess import call



def cupture_video():
    '''
    use shell command 'raspivid' 
    '''
    call(['raspivid', '-o', 'eye'])

def display_video():
    '''
    use shell command 'omxplayer'
    '''
    call(['omxplayer', 'eye'])


def trigger():
    '''
    read a trigger stat
    return 0 or 1 to close or open this system
    '''
    pass

# option
def eye_trigger():
    '''
    using simplecv to detact eye blink
    return 0 or 1 to close or open this system
    '''
