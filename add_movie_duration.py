import os
import subprocess
import re

def getLength(filename):
    result = subprocess.Popen(["ffprobe", filename],
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.STDOUT)
    line = [x.decode("utf-8") for x in result.stdout.readlines() if "Duration" in x.decode("utf-8")][0]
    duration = re.search('\d\d:\d\d:\d\d.\d\d', line).group(0)[0:5] # extract duration
    return(duration)

vid_extensions = ['mp4', 'mpeg', 'avi', 'mkv']

for x in os.listdir('.'): # all files and directories
    if os.path.isfile(x): # for the files in the directory
        if x.endswith(tuple(vid_extensions)) and '__' not in x: # without a duration already
            dur = getLength(x)
            new_name = x[0:-4] + '__' + dur + '__' + x[-4:]
            os.rename(x, new_name)
    elif os.path.isdir(x) and '__' not in x: # for the directories in the directory
        mov_list = [x for x in os.listdir(x) if x.endswith(tuple(vid_extensions))]
        dur = ''
        if len(mov_list) == 1:
            mov = mov_list[0]
            dur = getLength(x+'/'+mov)
            new_name = x + '__' + dur + '__'
            os.rename(x, new_name)
            
        elif len(mov_list) == 0:
            print('no movies (perhaps in subfolders) in:', x)
        
        elif len(mov_list) > 1 and len(mov_list) < 4:
            lens = []
            for m in mov_list:
                l = getLength(x+'/'+m)
                lens.append(l)
            dur = [x for x in lens if x[0:2] != '00'][0]
            new_name = x + '__' + dur + '__'
            os.rename(x, new_name)
        else:
            print('Many movies in:', x)
