#!virtualenv/bin/python
import pycurl
from bs4 import BeautifulSoup, Tag
from StringIO import StringIO
from download import download_file, md5sum
import os
import urllib2
from config import username, password, outfolder

systems={
    'ebook': 'E-Books',
    'windows': 'Windows',
    'mac': 'Mac',
    'android': 'Android',
    'linux': 'Linux',
    'audio': 'Soundtrack',
}

if not os.path.isdir(outfolder):
    print("%s does not exist." % outfolder)

c = pycurl.Curl()
c.setopt(c.URL, 'https://www.humblebundle.com/login')
c.setopt(c.POSTFIELDS, 'goto=/home&qs=&username=%s&password=%s&submit=Log%%20In' % (username, password))
c.setopt(c.COOKIEFILE, '')
c.perform()

storage = StringIO()
c.setopt(c.URL, 'https://www.humblebundle.com/home')
c.setopt(c.POSTFIELDS, '')
c.setopt(c.POST, 0)
c.setopt(c.WRITEFUNCTION, storage.write)
c.perform()
c.close()
content = storage.getvalue()

soup=BeautifulSoup(content)

if not os.path.isdir("%s/All" % outfolder):
    os.mkdir("%s/All" % outfolder)

for game in soup(attrs={'class': 'row'}):
    title=game(attrs={'class': 'title'})[0].find("a").contents[0]
    for downloads in game(attrs={'class': 'downloads'}):
        for download in downloads(attrs={'class': 'download'}):
            classname=downloads.attrs['class'][1]
            url = download(attrs={'class': 'a'})[0]
            weburl = url['data-web']
            filename = weburl.split("?key=")[0]
            if filename[0:25] == 'https://hb1.ssl.hwcdn.net':
                md5 = download(attrs={'class': 'dlmd5'})[0]['href'][1:]
                filename=filename.split("/")[-1]
                path = "%s/All/%s/%s/%s" % (outfolder, title, systems[classname], filename)
                if not os.path.isdir("%s/All/%s" % (outfolder, title)):
                    os.mkdir("%s/All/%s" % (outfolder, title))
                if not os.path.isdir("%s/All/%s/%s" % (outfolder, title, systems[classname])):
                    os.mkdir("%s/All/%s/%s" % (outfolder, title, systems[classname]))
                if os.path.exists(path) and not os.path.exists("%s.md5" % path):
                    print("Generating md5: %s" % filename)
                    md5file = md5sum(path)
                    if md5file == md5:
                        print("OK")
                        open("%s.md5" % path, "w").write(md5file)
                    else:
                        print("MISMATCH!")
                        os.unlink(path)
                        exit(1)
                elif not os.path.exists(path):
                    print("Downloading: %s" % filename)
                    download_file(weburl,path,md5)
