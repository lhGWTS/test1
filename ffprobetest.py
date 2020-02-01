#!*script
import json,os,glob,subprocess,tqdm

def getData():
    writedata = []
    maxsize = 0
    cmd_str = 'ffprobe -v quiet -print_format json -show_format -show_streams -i "%s"'

    files = glob.glob('*.jpg')
    files.extend(glob.glob('*.jpeg'))
    files.extend(glob.glob('*.webp'))

    for f in tqdm.tqdm(files):
        #ffexe = ffmpy.FFprobe(inputs={f:'-v quiet -print_format json -show_format -show_streams'})
        try:
            s = subprocess.check_output(cmd_str % f,shell=False)
            jd = json.loads(s)
        except:
            print("error : " + f)
        finally:
            filename = jd['format']['filename']
            width = int(jd['streams'][0]['width'])
            height = int(jd['streams'][0]['height'])
            writedata.append((filename,width*height,width,height))
            if maxsize < width*height:
                maxsize = width*height

    maxsize = str(len(str(maxsize)))
    return writedata , maxsize

with open('00_index.txt','w') as f:
    data,maxsize = getData()
    format_string = "%s\t" + "%0" + maxsize + "d\t%d\t%d\n"
    for x in data:
        f.writelines(format_string % x)
