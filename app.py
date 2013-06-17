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
    for i in range(0,len(fileList)):
        f = warc.open(fileList[i])
        paragraphs = justext.justext(f, justext.get_stoplist('English'))

#bol zadany subor
else:
    
    f = warc.open(options.file)
    paragraphs = justext.justext(f, justext.get_stoplist('English'))
