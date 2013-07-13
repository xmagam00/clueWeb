#!/usr/bin/env python

"""
Autor: Martin Maga
Popis: ClueWeb
Skript odstrani html tagy a naindexuje data pomocou mantee
"""

import sys
from optparse import OptionParser
import codecs
import justext
import os
import subprocess
#import unicode

#pomocne premenne
fileList=[]
move_on=0
tag_remove=0


usage = "usage: %prog [options] arg"
parser = OptionParser(usage)


#parametre skriptus
parser.add_option("--file", dest="file",
                  help="Nazov suboru z ClueWeb",
                  type="string", metavar="SUBOR")

parser.add_option("--folder", dest="folder",
                  help="Nazov adresa, ktory obsahuje subory z ClueWeb a bude rekurzive spracovany",
                  type="string", metavar="ADRESAR")


parser.add_option("--output", dest="output",
                  help="Nazov adresa, do ktoreho bude ulozeny vysledok z nastroja mantee",
                  type="string", metavar="ADRESAR")

(options, args) = parser.parse_args()

#testovanie na dostatocny pocet parametrov
if (len(sys.argv) < 3):
    sys.stderr.write("Zly pocet parametrov\n")
    sys.exit(1)


if (len(str(options.file)) < 1 or len(str(options.folder)) < 1):
    sys.stderr.write("Zle argumenty\n")
    sys.exit(1)

#pretypovanie na retazec
options.folder=str(options.folder)
pom_prem=str(options.folder)


#kontrola cesty options.folder
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
        for root, subFolders, files in os.walk(options.folder):
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
#bol zadany priecinok
if (str(options.folder) != "None"):
     #pomocne premenne
    pathname=""
    kam=""
    pom=""
    pom_list=[]
    g=""
    slov=dict()
    index2=0
    pom_parse=""
    ind=0
    url =[]
    file_parse=[]
    suborList=[]
    folderList=[]
    pom_file=""
    pom_file2=""
    for i in range(0,len(fileList)):
        #odzipujem subor
        try:
            subprocess.call(['gunzip','-f', os.path.abspath(str(fileList[i]))])
        except: 
            pass
            
    
    index=0
    zoznam=[]
    for i in range(0,len(fileList)):
    #zistim nazov suboru
      
        
        index=str((fileList[i])).rfind(".")
        
        file_name=""
        file_name=(str(fileList[i]))[:index]
        file_name=file_name
        html=""
        pom=""
        
      
        #otvorim odzipovany subor pre citanie
        f= codecs.open(os.path.abspath(str(file_name)),"rb","ISO8859-15")
        
        while (0 == 0):
        
            moje = f.readline()
        
        
            moje=unicode(moje)
            if not moje:
                break
        
            #hlavicka WARC
            if (moje.find("WARC/1.0") != -1):
                zoznam.append(moje)
                while (0==0):
                    moje = f.readline()
                    if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1 ):
                        slov[ind]=zoznam
                        html=html+moje
                        ind=ind+1
                        zoznam=[]
                        break
                    else:
                        if (moje.find("Target-URI") != -1):
                            index2=moje.find(":")

                       
                       
                            pom_file2=moje[index2+2:]
                            #sys.stdout.write(pom_file2)
                            url.append(pom_file2)
                            #sys.stdout.write(pom_file2)
                        
                            index2=0
                            pom_file2=""
                        
                        if (moje.find("TREC-ID") != -1):
                            pom_file=moje
                            index2=pom_file.find(":")
                            pom_file2=pom_file[index2+2:len(pom_file)-2]
                            file_parse.append(pom_file2)
                            #sys.stdout.write(pom_file2)
                            index2=0
                            pom_file=""
                            pom_file2=""
                        zoznam.append(moje)
                    
            #html telo alebo xml telo
            if (html.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1):
                while (0 == 0):
                    pom= f.readline()
                    pom=unicode(pom)
                    if (pom.find("</html>") != -1 or pom.find("</rss") != -1):
                        html=html+pom
                        slov[ind]=html
                        html=""
                        ind=ind+1
                        break
                   
                    else:
                        html=html+pom


  


  
        #sys.stdout.write(str(slov[3]))
    #   sys.exit(0)
        folder_name=""
        index=0
    #zistim cestu
        index=str(os.path.basename(fileList[i])).find(".")
        folder_name=str(os.path.basename(fileList[i]))[:index]
        
        pathname = os.path.dirname(sys.argv[0])        
        if (str(options.file).find("/") == -1):
            options.file=str(options.file)
            options.file=str(os.getcwd())+ "/"+fileList[i]
    
    
    
        kam = os.path.abspath(pathname)
        moje=""
#index pre url z WARC hlavicky
        m=0
#vytvorim priecinok pre vysledok
        try:
            os.makedirs(options.output+"/"+folder_name)
        except:
            pass
      
#vyparsovane subory sa ulozia do vopred vytvorenych priecinkov podla nazvu suboru
        for i in range(0,len(slov)):


                #pre HTML zaznam pouzijem nastroj justext alebo xml
            if (i % 2 == 1):

            
                paragraphs = justext.justext(slov[i].encode("utf-8"), justext.get_stoplist('English'))
                for paragraph in paragraphs:
                    p.write(paragraph['text'].encode("UTF-8"))
                
                #doplnim potrebne znacky
                    p.write("\r\n")
                p.write("\r\n\r\n")
                p.close()

            #WARC hlavicky zapisem
            if (i % 2 == 0):
                
                try:
                    os.makedirs(str(options.output) +"/"+folder_name+"/"+file_parse[m])
                except:
                    pass
                suborList.append(options.output+"/"+folder_name+"/"+file_parse[m]+"/" +file_parse[m])
                folderList.append(folder_name)
                p = codecs.open(options.output+"/"+folder_name+"/"+file_parse[m]+"/" +file_parse[m],"w")

                p.write(url[m].encode("UTF-8"))
                m=m+1
                p.write("\r\n")
                
                
   
    
    for i in range(0,len(suborList)/2):
        
        #vytvorim si subor pre definiciu korpusu
        try:
            subor = codecs.open("vert.korp", "w")
        except IOError:
            sys.stderr.write("Nemozno vytvorit korpus subor pre endodevert\n")
    
    #upravim obsah korpusu
        pom= suborList[i]
        moje="PATH  "+os.path.abspath(pom)+ "\n" +     "VERTICAL " + str(os.path.abspath(suborList[i]))  + "\nENCODING iso8859-2\n" + "INFO "+   "\""+ suborList[i] +"\"" + "\n"   + "\n" + "ATTRIBUTE word {\n" + "    TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE lemma {\n" + "   TYPE \"FD_FBD\"\n"    +  "}\n" + "\n" + "ATTRIBUTE tag {\n" + "   TYPE \"FD_FBD\"\n" + "}"
        #vysledok zapisem do korpus suboru pre nastroj mantee
        subor.write(moje)
    
        
        #zavolam nastroj na indexaciu mantee
        try:
            subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c',   str(os.getcwd())+"/"+"vert.korp" ])
        except:
            sys.stderr.write("Error in encodevert\n")
            os.remove("vert.korp")
            sys.exit(1)
        
        subor.close()
            #vymazem nepotrebny korpus subor
        os.remove("vert.korp")
        
            #vysledny subor zazipujem naspet
    
    for i in range(0,len(fileList)):
        pom=fileList[i][:len(fileList[i])-3]
      
        try:
            subprocess.call(['gzip','-f',  os.path.abspath(pom)])
        except: 
            pass

      
    sys.exit(0)

#bol zadany subor na spracovanie , parameter --file
else:
    #pomocne premenne
    pathname=""
    kam=""
    pom=""
    pom_list=[]
    g=""
    slov=dict()
    index2=0
    pom_parse=""
    ind=0
    url =[]
    file_parse=[]
    pom_file=""
    pom_file2=""
    #odzipujem subor
    try:
        subprocess.call(['gunzip', os.path.abspath(str(options.file))])
    except: 
        pass
    index=0
    zoznam=[]
    
    #zistim nazov suboru
    index=str(options.file).rfind(".")
    file_name=""
    file_name=(str(options.file))[:index]
    file_name=file_name
    html=""
    pom=""
    
    #otvorim odzipovany subor pre citanie
    f= codecs.open(file_name,"rb","ISO8859-15")
    
    #prehladavam cele telo
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
                if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1 ):
                    slov[ind]=zoznam
                    html=html+moje
                    ind=ind+1
                    zoznam=[]
                    break
                else:
                    if (moje.find("Target-URI") != -1):
                        index2=moje.find(":")

                       
                       
                        pom_file2=moje[index2+2:]
                        #sys.stdout.write(pom_file2)
                        url.append(pom_file2)
                        #sys.stdout.write(pom_file2)
                        
                        index2=0
                        pom_file2=""
                        
                    if (moje.find("TREC-ID") != -1):
                        pom_file=moje
                        index2=pom_file.find(":")
                        pom_file2=pom_file[index2+2:len(pom_file)-2]
                        file_parse.append(pom_file2)
                        #sys.stdout.write(pom_file2)
                        index2=0
                        pom_file=""
                        pom_file2=""
                    zoznam.append(moje)
                    
        #html telo alebo xml telo
        if (html.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1):
            while (0 == 0):
                pom= f.readline()
                pom=unicode(pom)
                if (pom.find("</html>") != -1 or pom.find("</rss") != -1):
                    html=html+pom
                    slov[ind]=html
                    html=""
                    ind=ind+1
                    break
                   
                else:
                    html=html+pom


  


  
    #sys.stdout.write(str(slov[3]))
    #sys.exit(0)
    folder_name=""
    index=0
    #zistim cestu
    index=str(os.path.basename(options.file)).find(".")
    folder_name=str(os.path.basename(options.file))[:index]
  
    pathname = os.path.dirname(sys.argv[0])        
    if (str(options.file).find("/") == -1):
            options.file=str(options.file)
            options.file=str(os.getcwd())+ "/"+options.file
    
    
    
    kam = os.path.abspath(pathname)
    moje=""
#index pre url z WARC hlavicky
    m=0
#vytvorim priecinok pre vysledok
    try:
        os.makedirs(options.output+"/"+folder_name)
    except:
        pass

#vyparsovane subory sa ulozia do vopred vytvorenych priecinkov podla nazvu suboru
    for i in range(0,len(slov)):


                #pre HTML zaznam pouzijem nastroj justext alebo xml
        if (i % 2 == 1):

            
            paragraphs = justext.justext(slov[i].encode("utf-8"), justext.get_stoplist('English'))
            for paragraph in paragraphs:
                p.write(paragraph['text'].encode("UTF-8"))
                
                #doplnim potrebne znacky
                p.write("\r\n")
            p.write("\r\n\r\n")
            p.close()

        #WARC hlavicky zapisem
        if (i % 2 == 0):
         
            try:
                os.makedirs(str(options.output) +"/"+folder_name+"/"+file_parse[m])
            except:
                pass
            
            p = codecs.open(options.output+"/"+folder_name+"/"+file_parse[m]+"/" +file_parse[m],"w")

            p.write(url[m].encode("UTF-8"))
            m=m+1
            p.write("\r\n")
                
                
       
    for i in range(0,len(file_parse)):
        
        #vytvorim si subor pre definiciu korpusu
        try:
            subor = codecs.open("vert.korp", "w")
        except IOError:
            sys.stderr.write("Nemozno vytvorit korpus subor pre endodevert\n")
    
    #upravim obsah korpusu
        pom=str(options.output)+"/"+folder_name  + "/"+ file_parse[i]
        moje="PATH  "+os.path.abspath(pom)+ "\n" +     "VERTICAL " + str(os.path.abspath(file_parse[i]))  + "\nENCODING iso8859-2\n" + "INFO "+   "\""+ file_parse[i] +"\"" + "\n"   + "\n" + "ATTRIBUTE word {\n" + "    TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE lemma {\n" + "   TYPE \"FD_FBD\"\n"    +  "}\n" + "\n" + "ATTRIBUTE tag {\n" + "   TYPE \"FD_FBD\"\n" + "}"
        #vysledok zapisem do korpus suboru pre nastroj mantee
        subor.write(moje)
      
        
        #zavolam nastroj na indexaciu mantee
        try:
            subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c',   str(os.getcwd())+"/"+"vert.korp" ])
        except:
            sys.stderr.write("Error in encodevert\n")
            os.remove("vert.korp")
            sys.exit(1)
        
        subor.close()
        #vymazem nepotrebny korpus subor
        os.remove("vert.korp")
        
        #vysledny subor zazipujem naspet
    
    try:
        subprocess.call(['gzip',  os.path.abspath(file_name)])
    except: 
        pass

sys.exit(0)
