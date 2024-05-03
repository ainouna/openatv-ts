import time
from Directories import resolveFilename, SCOPE_CONFIG, fileExists
from HardInfo import HardInfo
vfdSIZE = HardInfo().get_vfdsize()
if HardInfo().get_rcstype() == 'HS7429':
    vfdSIZE += 1
PERCENTAGE_START = 80
PERCENTAGE_END = 100
LAST_PERCENTAGE = 0
profile_start = time.time()
profile_data = {}
total_time = 1
profile_file = None
LastVFDtext = ''
try:
    profile_old = open(resolveFilename(SCOPE_CONFIG, 'profile'), 'r').readlines()
    t = None
    for line in profile_old:
        t, id = line[:-1].split('\t')
        t = float(t)
        total_time = t
        profile_data[id] = t

    if total_time == 0:
        total_time = 1
except:
    print 'no profile data available'

try:
    profile_file = open(resolveFilename(SCOPE_CONFIG, 'profile'), 'w')
except IOError:
    print "WARNING: couldn't open profile file!"

def profile(id):
    global LAST_PERCENTAGE
    global LastVFDtext
    global profile_file
    now = time.time() - profile_start
    if profile_file:
        profile_file.write('%.2f\t%s\n' % (now, id))
        print '%s\t%.2f\t%s\n' % (time.strftime('%H:%M:%S', time.localtime()), now, id)
        if id in profile_data:
            t = profile_data[id]
            perc = t * (PERCENTAGE_END - PERCENTAGE_START) / total_time + PERCENTAGE_START
            if perc > LAST_PERCENTAGE:
                if vfdSIZE == 4:
                    CurrentText = 'openTS-E2-%d' % (perc - 1)
                    CurrentText = CurrentText[0:4]
                if vfdSIZE == 5:
                    CurrentText = 'openTS-E2:%d' % (perc - 1)
                    CurrentText = CurrentText[0:5]
                else:
                    if vfdSIZE == 8:
                        CurrentText = 'openTS-%d' % perc
                        CurrentText = CurrentText[0:8]
                    else:
                        CurrentText = 'openTS-%d' % perc
                        CurrentText = CurrentText[0:14]
                    try:
                        open('/proc/progress', 'w').write('%d \n' % perc)
                        if LastVFDtext != CurrentText and perc < 100:
                            print '[Profile] %s' % CurrentText
                            open('/dev/vfd', 'w').write(CurrentText)
                            LastVFDtext = CurrentText
                    except IOError:
                        pass

                LAST_PERCENTAGE = perc


def profile_final():
    global profile_file
    try:
        open('/proc/progress', 'w').write('100 \n')
    except:
        pass

    if profile_file is not None:
        profile_file.close()
        profile_file = None
    return
