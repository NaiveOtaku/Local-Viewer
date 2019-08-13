
import codecs

import os
from os import listdir
from os.path import isfile, join

from lzpy import Table
Table.encoding = "GBK"



def writeto(sent, filename):
    file = open(filename,"r")
    file.write(sent)
    file.close

def getfilenames(path):
    filenames = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return filenames


topsent="""    
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
</head>
"""

bodytopsent="""

    <span class=topbar>
        <div class=dirbox>
            目录
        </div>

        <div class=tagbox>
            tag
        </div>


        <div class=viewbox>
            观看模式
        </div>


        <div class=timebox>
            时间
        </div>


        <div class=makerbox>
            制作人
        </div>

        <div class=sortbox>
            排序
        </div>


    </span>
    
"""



bodysent = "<body>{}</body>"




class Viewer:


    def __init__(self,filename,infoname,topath):
        self.filename = filename
        self.infoname = infoname
        self.table = Table.read(infoname)
        self.topath = topath
    

    def make(self):
        #make html
        file = codecs.open(self.filename,"w","utf-8")
        file.write(topsent)

        file.write("<body>")
        file.write(bodytopsent)
        file.write("<div class=content>")#
        lastname = ""
        
        def mkpath(path,filename):
            if path == None:
                return join(self.topath,filename)

            elif filename==None:
                return join(self.topath,path)

            else:
                return join(self.topath,path,filename)

        def mkhtml(name,tp,cover,path,content, episode):

            fullname = name+" "+str(episode) if episode is not None else name
            fullcoverpath = mkpath(path,cover)
            fullcontentpath = mkpath(path,content)
            
            if tp=="video":
                s = f"""
                <h1>{fullname}</h1>
                <img src="{fullcoverpath}" height=720>
                <video src="{fullcontentpath}" width=1280 height=720 controls></video>
                """
                return s
            elif tp == "img":
                s =f"""
                <details>
                <summary><h1>{fullname}</h1>"
                <img src="{fullcoverpath}" height=720></summary>
                    """

                filenames = getfilenames(mkpath(path,""))
                filenames.sort()
                for filename in filenames:
                    if filename!=fullcoverpath:
                        s+=f"""
                              <img src="{filename}" height=720>
                            """
                s+="</details>"
                return s
            elif tp=="exe":

                fullcontentpath = os.getcwd() + fullcontentpath
                s=f"""
                  <h1>{fullname}</h1>
          
                   
                   <a href="localexplorer:{fullcontentpath}"><img src ="{fullcoverpath}" height=720>
                   </a>

                """
                return s
        
        for i in range(1,len(self.table)+1):
            row= self.table[i]

            name = row["name"]
            tp = row["type"]
            cover = row["cover"]
            path = row["path"]
            content = row["content"]
            episode = row["episode"]
            

            if name==lastname:
                sent = mkhtml(name,tp,cover,path,content, episode)
                
                file.write(sent)
            else:
                if i !=1:
                    file.write("</div>")
                file.write("<div class=box>")
                sent = mkhtml(name,tp,cover,path,content, episode)
                
                file.write(sent)
            lastname=name
            
        file.write("</div>")
            
        file.write("</div></body>")#
        file.close()





v = Viewer(filename="viewerx.html",infoname="info", topath ="classify")
v.make()
