#!/usr/bin/env python

"""
Autor: Martin Maga
Popis: ClueWeb
Skript odstrani html tagy a naindexuje data pomocou mantee
"""
from warc import WARCReader, WARCHeader, WARCRecord, WARCFile
import sys
from optparse import OptionParser
import codecs
import justext
import os
import warc
import subprocess
import gzip


fileList=[]
move_on=0
tag_remove=0
usage = "usage: %prog [options] arg"
parser = OptionParser(usage)


parser.add_option("--file", dest="file",
                  help="Name of file from ClueWeb",
                  type="string", metavar="FILE")

parser.add_option("--folder", dest="folder",
                  help="Name of folder from which will be files from ClueWeb recursively processed",
                  type="string", metavar="FOLDER")


parser.add_option("--output", dest="output",
                  help="Name of folder where result file will be saved",
                  type="string", metavar="FOLDER")

(options, args) = parser.parse_args()

if (len(sys.argv) < 3):
    sys.stderr.write("Bad amount of arguments")
    sys.exit(1)

if (len(str(options.file)) < 1 or len(str(options.folder)) < 1):
    sys.stderr.write("Bad arguments")
    sys.exit(1)
options.folder=str(options.folder)
pom_prem=str(options.folder)
if (move_on == 0):
#odstranim / zo zaciatku parametra input
    if (options.folder[0] == '/'):
        pom_prem=input_file_name
        input_file_name=input_file_name.strip('/')
        tag_remove=1

        #otestujem, ci bol zadany priecinok
    if (os.path.isdir(options.folder) == True):
        move_on=1
#ak bol tak nacitam vsetky hlavickove subory do zoznamu fileList
        for root, subFolders, files in os.walk(input_file_name):
            for file in files:
                if file.endswith("warc.gz"):
                    fileList.append(os.path.join(root,file))
            is_param_file=0
    else:
        move_on=0
#testujem ci parameter input nie je priecinok s / na zaciatku
    if (tag_remove == 1):
        input_file_name=pom_prem
#pokial je to priecinok
        if (os.path.isdir(input_file_name) == True):
            move_on=1
            pom_prem=""
            #prehladavam vsetky priecinky a ukladam si do fileListu hlav.sub.
            for root, subFolders, files in os.walk(input_file_name):
                for file in files:
                    if file.endswith("warc.gz"):
                        fileList.append(os.path.join(root,file))
            is_param_file=0
        else:
            if (input_file_name[0] == '/'):
                input_file_name=input_file_name.strip('/')
                tag_sek=1
            if (move_on !=1):
                move_on=0
#testujem, ci nahodou nebol zadany subor na prehladavanie
if (move_on == 0):
    pomles=""
    move_on=0
    move_on2=0
    tag_sek=0
    input_file_name=str(options.file)
    input_file_name='/'+input_file_name
    #testuje, ci nebola zadana absolutna cesta k suboru
    if (os.path.isabs(input_file_name) == True):
        
        #pokusim sa subor otvorit 
        try:
            f = codecs.open(input_file_name, "r", "utf-8")
        except IOError:
            move_on2=1
        is_param_file=1
        if (move_on2 == 1):
            if (pom_prem[0] == '/'):
                tag_sek=1
            input_file_name=input_file_name.strip('/')
            try:
                f = codecs.open(input_file_name, "r", "utf-8")
            #pokial zadany subor neexistuje ukoncim program
            except IOError:
                sys.stderr.write("Neznamy subor/ priecinok\n")
                sys.exit(1)
        move_on=1
#testujem, ci bola zadana relativna cesta k suboru a ci esubor existuje
    if (os.path.isabs(input_file_name) == False and move_on==0):
        if (input_file_name[0] != '/'):
#ulozim subor s absolutnou cestou
            pomles=os.getcwd()+'/'+input_file_name
        else:
            pomles=os.getcwd()+input_file_name
        if (os.path.isfile(pomles) == True):
            is_param_file=1
        else:
            sys.stderr.write("Neexistujuci subor/priecinok\n")
            sys.exit(1)






if (str(options.folder) != "None"):
    
    pom=""
    pom_list=[]
    for i in range(0,len(fileList)):
        f = warc.open(fileList[i])
        for record in f:
            paragraphs = justext.justext(record, justext.get_stoplist('English'))
            paragraphs = paragraphs.replace("<p>","")
            paragraphs = paragraphs.replace("<h>","")
            pom_list.append(paragraphs)
        f = warc.open(options.file, "w")
        for i in range(0,len(pom_list)):
            f.write_record(pom_list[i])
        h.close()
        korp="PATH  "+ fileList[i]+ "\n"
        + "VERTICAL "+str(options.output) + "\n"
        + "ENCODING iso8859-2\n"
        + "INFO"+ "\""+ subor +"\"" + "\n"
        + "\n"
        + "ATTRIBUTE word {\n"
        + "   TYPE \"FD_FBD\"\n"
        + "}\n"
        + "\n"
        + "ATTRIBUTE lemma {\n"
        + "   TYPE \"FD_FBD\"\n"
        + "}\n"
        + "\n"
        + "ATTRIBUTE tag {\n"
        + "   TYPE \"FD_FBD\"\n"
        + "}\n"
        try:
            os.environ["MANATEE_REGISTRY"] = ""
            os.environ["MANATEE_REGISTRY"]  = korp
            subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c', fileList[i]])
            subprocess.Popen(['/mnt/minerva1/nlp/local64/bin/encodevert','-c'])
            # thread continues ...
            p.terminate()
        except:
            sys.stderr.write("Error in encodevert")
            sys.exit(1)
#bol zadany subor
else:
    pathname=""
    kam=""
    pom=""
    pom_list=[]
    g=""
    slov=dict()
    ind=0
    try:
        subprocess.call(['gunzip', str(options.file)])
    except: 
        pass
    index=0
    zoznam=[]
    index=str(os.path.basename(options.file)).find(".")
    file_name=""
    file_name=(str(options.file))[:index]
    file_name=file_name+".warc"
    html=""
    pom=""
    f= codecs.open(file_name,"rb","ISO8859-15")
    while (0==0):
        
        moje = f.readline()
        
        if not moje: break
        moje=unicode(moje)
        if (moje.find("WARC/1.0") != -1):
            if (len(html) > 0):
               
                
                paragraphs = justext.justext(unicode(html).encode("utf-8"), justext.get_stoplist('English'))
                for paragraph in paragraphs:
                    pom =  paragraph['text']
                    zoznam.append(pom)
            html=""
            slov[ind]=zoznam
            pom=""
            zoznam.append(moje)
            
            while(0==0):
                moje=f.readline()
            
              
                if (moje.find("!DOCTYPE") != -1):
                    html=html+moje
                    break
                else:
                    zoznam.append(moje)
            slov[ind]=zoznam
            
            ind=ind+1
            zoznam=[]
        else:
            html=html+unicode(moje)
            #aragraphs = justext.justext(record, justext.get_stoplist('English'))
            #paragraphs = paragraphs.replace("<p>","")
            #paragraphs = paragraphs.replace("<h>","")
    p = codecs.open(file_name,"w")
    for i in range(0,len(slov)):
        for h in range(0,9):
            p.write((slov[i][h]).encode('utf-8'))
    p.close()
    
    try:
        subprocess.call(['gzip',  file_name])
    except: 
        pass
    
    
    try:
        subor = codecs.open("vert.korp", "w")
    except IOError:
        sys.stderr.write("Nemozno vytvorit korpus subor pre endodevert\n")
    
    folder_name=""
    index=0
    index=str(os.path.basename(options.file)).find(".")
    folder_name=str(os.path.basename(options.file))[:index]
  
    pathname = os.path.dirname(sys.argv[0])        
    if (str(options.file).find("/") == -1):
            options.file=str(options.file)
            options.file=str(os.getcwd())+ "/"+options.file
    
    
    
    try:
        os.makedirs(options.output+"/"+folder_name)
    except:
        pass
  
    kam = os.path.abspath(pathname)
    moje=""
    moje="PATH  "+ "/"+str(options.output)+"/"+folder_name  + "\n" + "VERTICAL " + str(options.file)  + "\nENCODING iso8859-2\n" + "INFO "+ "\""+ str(os.path.basename(options.file)) +"\"" + "\n"   + "\n" + "ATTRIBUTE word {\n" + "   TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE lemma {\n" + "   TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE tag {\n" + "   TYPE \"FD_FBD\"\n" + "}"
    subor.write(moje)
    sys.exit(0)
    try:
        subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c', str(options.file)])
    except:
        sys.stderr.write("Error in encodevert\n")
        os.remove("vert.korp")
        sys.exit(1)
    subor.close()
    os.remove("vert.korp")
sys.exit(0)


