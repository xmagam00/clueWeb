#!/usr/bin/env python

"""
Autor: Martin Maga
Popis: ClueWeb

"""
import sys
from optparse import OptionParser
import codecs
import justext
import os
import warc
import subprocess

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

(options, args) = parser.parse_args()

if (len(sys.argv) < 1):
    sys.stderr.write("Bad amount of arguments")
    sys.exit(1)

if (len(str(options.file)) < 1 or len(str(options.folder)) < 1):
    sys.stderr.write("Bad arguments")

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

#bol zadany priecinok
if (len(options.folder) > 1):
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
        korp="PATH"+ fileList[i]+ "\n" +
        "VERTICAL"+fileList[i] + "\n" +
        "ENCODING iso8859-2\n" +
        "INFO"+ "\""+ subor +"\"" + "\n"+
        "\n" +
        "ATTRIBUTE word {\n" +
        "   TYPE \"FD_FBD\"\n" +
        "}\n" +
        "\n" + 
        "ATTRIBUTE lemma {\n" +
        "   TYPE \"FD_FBD\"\n"+
        "}"+
        "\n"+
        "ATTRIBUTE tag {\n"+
        "   TYPE \"FD_FBD\"\n"+
        "}\n"
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
    pom=""
    pom_list=[]
    f = warc.open(options.file)
    for record in f:
        paragraphs = justext.justext(record, justext.get_stoplist('English'))
        paragraphs = paragraphs.replace("<p>","")
        paragraphs = paragraphs.replace("<h>","")
        pom_list.append(paragraphs)
    f = warc.open(options.file, "w")
    for i in range(0,len(pom_list)):
        f.write_record(pom_list[i])
    h.close()
    
    try:
        os.environ["MANATEE_REGISTRY"] = ""
        os.environ["MANATEE_REGISTRY"]  = korp
        subprocess.call(['/mnt/minerva1/nlp/local64/bin/encodevert','-c', options.file])
        subprocess.Popen(['/mnt/minerva1/nlp/local64/bin/encodevert','-c'])
        # thread continues ...
        p.terminate()
    except:
        sys.stderr.write("Error in encodevert")
        sys.exit(1)




