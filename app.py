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
    
    pathname=""
    kam=""
    pom=""
    pom_list=[]
    g=""
    slov=dict()
    ind=0
    
    for i in range(0
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
    while(0==0):
        
        moje = f.readline()
        
        
        moje=unicode(moje)
        if not moje:
            break
        
        #hlavicka WARC
        if (moje.find("WARC/1.0") != -1):
            zoznam.append(moje)
            while (0==0):
                moje = f.readline()
                if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1):
                    slov[ind]=zoznam
                    html=html+moje
                    ind=ind+1
                    zoznam=[]
                    break
                else:
                    zoznam.append(moje)
                    
        #html
        if (html.find("DOCTYPE") != -1 or moje.find("<html") != -1):
            while (0 == 0):
                pom= f.readline()
                pom=unicode(pom)
                if (pom.find("</html>") != -1):
                    html=html+pom
                    slov[ind]=html
                    html=""
                    ind=ind+1
                    break
                   
                else:
                    html=html+pom
        #   while (0 == 0):
              #  moje=f.readline()
                #print "TAG:",moje.encode("ISO8859-15")
                #print moje.encode("utf-8")
               # if (moje.find("</html>") != -1):
      #              html=html+moje
      #              slov[ind]=html
    #                ind=ind+1
     #               zoznam=[]
                  #  break
      #          else:
      #              html=html+moje
                
               
               
            
            
      
            
        
            
  

    p = codecs.open(file_name,"w")
    for i in range(0,len(slov)):
        
        if (i % 2 == 1):
            
            
            paragraphs = justext.justext(slov[i].encode("utf-8"), justext.get_stoplist('English'))
            for paragraph in paragraphs:
                p.write(paragraph['text'].encode("UTF-8"))
                #print paragraph['text'].encode("UTF-8")
                
                p.write("\r\n")
            p.write("\r\n\r\n")
        if (i % 2 == 0):
            for h in range(0,len(slov[i])):
                p.write(slov[i][h].encode("UTF-8"))
                
                if (i != 0):
                    p.write("\r\n")
       
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
    
    try:
        subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c', str(options.file)])
    except:
        sys.stderr.write("Error in encodevert\n")
        os.remove("vert.korp")
        sys.exit(1)
    subor.close()
    os.remove("vert.korp")
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
    while(0==0):
        
        moje = f.readline()
        
        
        moje=unicode(moje)
        if not moje:
            break
        
        #hlavicka WARC
        if (moje.find("WARC/1.0") != -1):
            zoznam.append(moje)
            while (0==0):
                moje = f.readline()
                if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1):
                    slov[ind]=zoznam
                    html=html+moje
                    ind=ind+1
                    zoznam=[]
                    break
                else:
                    zoznam.append(moje)
                    
        #html
        if (html.find("DOCTYPE") != -1 or moje.find("<html") != -1):
            while (0 == 0):
                pom= f.readline()
                pom=unicode(pom)
                if (pom.find("</html>") != -1):
                    html=html+pom
                    slov[ind]=html
                    html=""
                    ind=ind+1
                    break
                   
                else:
                    html=html+pom
        #   while (0 == 0):
              #  moje=f.readline()
                #print "TAG:",moje.encode("ISO8859-15")
                #print moje.encode("utf-8")
               # if (moje.find("</html>") != -1):
      #              html=html+moje
      #              slov[ind]=html
    #                ind=ind+1
     #               zoznam=[]
                  #  break
      #          else:
      #              html=html+moje
                
               
               
            
            
      
            
        
            
  

    p = codecs.open(file_name,"w")
    for i in range(0,len(slov)):
        
        if (i % 2 == 1):
            
            
            paragraphs = justext.justext(slov[i].encode("utf-8"), justext.get_stoplist('English'))
            for paragraph in paragraphs:
                p.write(paragraph['text'].encode("UTF-8"))
                #print paragraph['text'].encode("UTF-8")
                
                p.write("\r\n")
            p.write("\r\n\r\n")
        if (i % 2 == 0):
            for h in range(0,len(slov[i])):
                p.write(slov[i][h].encode("UTF-8"))
                
                if (i != 0):
                    p.write("\r\n")
       
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
    
    try:
        subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c', str(options.file)])
    except:
        sys.stderr.write("Error in encodevert\n")
        os.remove("vert.korp")
        sys.exit(1)
    subor.close()
    os.remove("vert.korp")
sys.exit(0)


