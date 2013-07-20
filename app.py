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
    sys.stderr.write("Zly pocet parametrov")
    sys.exit(1)


if (len(str(options.file)) < 1 or len(str(options.folder)) < 1):
    sys.stderr.write("Zle argumenty")
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
    url =""
    file_parse=""
    pom_file=""
    pom_file2=""
    for hh in range(0,len(fileList)):
        try:
            subprocess.check_call(['gunzip', os.path.abspath(str(fileList[hh]))])
            
        except: 
            print "Chyba pri unzip suboru\n",str(os.path.abspath(str(fileList[hh])))
            fileList.remove(fileList[hh])
    
   
    
    for hh in range(0,len(fileList)):
        
        print "*** Prave spracovavom",fileList[hh],"***\n"
        #odzipujem subor
       
        index=0
        zoznam=[]
        url=[]
        index=str((fileList[hh])).rfind(".")
        
        file_name=""
        file_name=(str(fileList[hh]))[:index]
        html=""
        pom=""
        
        
        #vyparsujem folder
        folder_name=""
        index=0
        #zistim cestu
        index=str(os.path.basename(fileList[hh])).find(".")
        folder_name=str(os.path.basename(fileList[hh]))[:index]
  
        pathname = os.path.dirname(sys.argv[0])        
        if (str(fileList[hh]).find("/") == -1):
            fileList[hh]=str(fileList[hh])
            fileList[hh]=str(os.getcwd())+ "/"+ fileList[hh]
    
    
        doc=0
        warc=1
        kam = os.path.abspath(pathname)
        moje=""
        #index pre url z WARC hlavicky
        m=0
        #vytvorim priecinok pre vysledok
        try:
            os.makedirs(options.output+"/"+folder_name)
        except:
            pass
            
            
        #otvorim odzipovany subor pre citanie
        f= codecs.open(file_name,"rb","ISO8859-15")
    
         #prehladavam cele telo
        while(0==0):
            #precitam riadok
            moje = f.readline()
        
            #pretypujem na unicode
            moje=unicode(moje)
            if not moje:
                break
        
            #hlavicka WARC
            if (moje.find("WARC/1.0") != -1):
                doc=0
                warc=1
        
            #narazim na html telo
            if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1 ):
                warc=0
                doc=1
            #spracuj subor a naindexuj
            if (moje.find("</html>") != -1 or moje.find("</rss") != -1):
                html=html+moje
                warc=1
                doc=0
            
            
            
                #indexaciua vytvarenie priecinku a justext
                try:
                    os.makedirs(str(options.output) +"/"+folder_name+"/"+file_parse)
                except:
                    pass
                p = codecs.open(options.output+"/"+folder_name+"/"+file_parse+ "/" +file_parse,"w")
                p.write(url.encode("UTF-8"))
                p.write("\r\n")
            
                #justext
                paragraphs = justext.justext(html.encode("utf-8"), justext.get_stoplist('English'))
            
                for paragraph in paragraphs:
                    p.write(paragraph['text'].encode("UTF-8"))
                
                    #doplnim potrebne znacky
                    p.write("\r\n")
           
                p.close()
            
            
                #indexacia vytvorim si subor pre definiciu korpusu
                cest=""
                try:
                    subor = codecs.open("vert.korp", "w")
                except IOError:
                    sys.stderr.write("Nemozno vytvorit korpus subor pre endodevert\n")
                cest="PATH  "+    os.path.abspath(str(options.output))+"/"+folder_name+"/"+str(file_parse)+"\n" +     "VERTICAL " + os.path.abspath(str(options.output))+"/"+folder_name+"/"+str(file_parse)+"/"+str(file_parse) + "\nENCODING iso8859-2\n" + "INFO "+   "\""+ file_parse +"\"" + "\n"   + "\n" + "ATTRIBUTE word {\n" + "    TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE lemma {\n" + "   TYPE \"FD_FBD\"\n"    +  "}\n" + "\n" + "ATTRIBUTE tag {\n" + "   TYPE \"FD_FBD\"\n" + "}\n"
                subor.write(cest)
                subor.close()
                print cest
                
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
                html=""
                url=""
                file_parse=""
                zoznam=[]
                doc=0
                warc=1
        
        
        
        
            #ukladam do zoznamu    
            if (warc == 1 and doc == 0):
                zoznam.append(moje)
                if (moje.find("TREC-ID") != -1):
                    pom_file=moje
                    index2=pom_file.find(":")
                    pom_file2=pom_file[index2+2:len(pom_file)-2]
                    file_parse=pom_file2
                    index2=0
                    pom_file=""
                    pom_file2=""
                if (moje.find("Target-URI") != -1):
                    index2=moje.find("Target-URI") 
                    pom_file2=moje[index2:]
                    url=pom_file2
                    index2=0
                    pom_file2=""
        
       
            #citam html
            if (doc == 1 and warc == 0):
                html=html+moje
        
       
     
        
    sys.exit(0)
#bol zadany subor na spracovanie , parameter --file
else:
    #pomocne premenne
    pathname=""
    kam=""
    pom=""
    pom_list=[]
    g=""
    
    index2=0
    pom_parse=""
    ind=0
    url =""
    file_parse=""
    pom_file=""
    pom_file2=""
    #odzipujem subor
    try:
        subprocess.check_call(['gunzip', os.path.abspath(str(options.file))])
    except: 
        print "Chyba pri odzipovani",options.file
        sys.exit(1)
    index=0
    zoznam=[]
    
    #zistim nazov suboru
    index=str(os.path.basename(options.file)).find(".")
    file_name=""
    file_name=(str(options.file))[:index]
    file_name=file_name+".warc"
    html=""
    pom=""
    warc=1
    doc=0
    
    cest=""
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
    
    
    
    #otvorim odzipovany subor pre citanie
    f= codecs.open(file_name,"rb","ISO8859-15")
    
    #prehladavam cele telo
    while(0==0):
        #precitam riadok
        moje = f.readline()
        
        #pretypujem na unicode
        moje=unicode(moje)
        if not moje:
            break
        
        #hlavicka WARC
        if (moje.find("WARC/1.0") != -1):
            doc=0
            warc=1
        
         #narazim na html telo
        if (moje.find("DOCTYPE") != -1 or moje.find("<html") != -1 or moje.find("<?xml") != -1 ):
            warc=0
            doc=1
        #spracuj subor a naindexuj
        if (moje.find("</html>") != -1 or moje.find("</rss") != -1):
            html=html+moje
            warc=1
            doc=0
            
            
            
            #indexaciua vytvarenie priecinku a justext
            try:
                os.makedirs(str(options.output) +"/"+folder_name+"/"+file_parse)
            except:
                pass
            p = codecs.open(options.output+"/"+folder_name+"/"+file_parse+ "/" +file_parse,"w")
            p.write(url.encode("UTF-8"))
            p.write("\r\n")
            
            #justext
            paragraphs = justext.justext(html.encode("utf-8"), justext.get_stoplist('English'))
            
            for paragraph in paragraphs:
                p.write(paragraph['text'].encode("UTF-8"))
                
                #doplnim potrebne znacky
                p.write("\r\n")
           
            p.close()
            
            
            #indexacia vytvorim si subor pre definiciu korpusu
            
            try:
                subor = codecs.open("vert.korp", "w")
            except IOError:
                sys.stderr.write("Nemozno vytvorit korpus subor pre endodevert\n")
            cest="PATH  "+    os.path.abspath(str(options.output))+"/"+folder_name+"/"+str(file_parse)+"\n" +     "VERTICAL " + os.path.abspath(str(options.output))+"/"+folder_name+"/"+str(file_parse)+"/"+str(file_parse) + "\nENCODING iso8859-2\n" + "INFO "+   "\""+ file_parse +"\"" + "\n"   + "\n" + "ATTRIBUTE word {\n" + "    TYPE \"FD_FBD\"\n"    + "}\n" + "\n" + "ATTRIBUTE lemma {\n" + "   TYPE \"FD_FBD\"\n"    +  "}\n" + "\n" + "ATTRIBUTE tag {\n" + "   TYPE \"FD_FBD\"\n" + "}\n"
            subor.write(cest)
            subor.close()
            
            
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
            html=""
            url=""
            file_parse=""
            zoznam=[]
        
        
        
        
        
        #ukladam do zoznamu    
        if (warc == 1 and doc == 0):
            zoznam.append(moje)
            if (moje.find("TREC-ID") != -1):
                    pom_file=moje
                    index2=pom_file.find(":")
                    pom_file2=pom_file[index2:]
                    file_parse=pom_file2
                    file_parse=file_parse[2:len(file_parse)-2]
                    index2=0
                    pom_file=""
                    pom_file2=""
            if (moje.find("Target-URI") != -1):
                    index2=moje.find("Target-URI") 
                    pom_file2=moje[index2:]
                    url=pom_file2
                    
                    index2=0
                    pom_file2=""
        
       
        #citam html
        if (doc == 1 and warc == 0):
            html=html+moje
        
       
        
                
            
                 
sys.exit(0)
