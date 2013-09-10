from urllib2 import urlopen
import sys
import hashlib
import os

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()

def download_file(url,outpath,md5):
    u = urlopen(url)
    f = open(outpath, 'wb')
    meta = u.info()
    file_size=0
    for header in meta.headers:
        if header[0:14] == 'Content-Length':
            file_size = int(header[16:-2])
    if file_size == 0:
        print("We have a problem right here.")
        exit(1)
    file_size_dl = float(0)
    block_sz = 262144
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
    
        file_size_dl = float(file_size_dl) + float(len(buffer))
        f.write(buffer)
        status = "    %s MB [%3.2f%%] (of %s MB)" % (str(round(float(file_size_dl)/float(1000000),2)).rjust(7,' '), float(file_size_dl) * float(100.) / float(file_size),str(round(float(file_size)/float(1000000),2)))
        sys.stdout.write("\r%s     " % status)
    sys.stdout.write("\n")    
    f.close()
    if not md5sum(outpath) == md5:
        print("Download Failed! Wrong MD5-Sum!")
        os.remove(outpath)
    else:
        open("%s.md5" % outpath, "w").write(md5)

