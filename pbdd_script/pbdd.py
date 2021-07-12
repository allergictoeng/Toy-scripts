# python 2.7
# Author: @allergictoeng
# Parse from .groovy BDD tests blocks (given, when, then, and) and saves in .csv files
# PBDD (Parse from BDD)

import re
import csv
import os
import argparse

# Patterns in use (Regex)
PATTERN_METHOD_INIT = 'def\s*\"(.*?)\"\s*\(\)'
PATTERN_AND = 'and:\s*\"(.*?)\"'
PATTERN_GIVEN = 'given:\s*\"(.*?)\"'
PATTERN_WHEN = 'when:\s*\"(.*?)\"'
PATTERN_THEN = 'then:\s*\"(.*?)\"'
PATTERN_QUOTE_MASKS = '\"(.*?)\"'
PATTERN_SINGLE_QUOTE = "\""
PATTERN_VOID = ""

# Get a line from an .groovy file 
def brute_line(patr, line):
    resu = re.search(patr,line.strip()) 
    if resu:
        return resu.group()

# Clean not required characters
def sanitize_line(label, data):
    result = brute_line(PATTERN_QUOTE_MASKS, data)
    return label + result.replace(PATTERN_SINGLE_QUOTE,PATTERN_VOID)

# Return a selected and cleaned bdd sentences
def ret_bdd(line):
    def_method = brute_line(PATTERN_METHOD_INIT,line)    
    given_data = brute_line(PATTERN_GIVEN,line)   
    and_data = brute_line(PATTERN_AND,line)    
    when_data = brute_line(PATTERN_WHEN,line)    
    then_data = brute_line(PATTERN_THEN,line)    
    
    if def_method:
        return sanitize_line("Teste: ", def_method)        
    if given_data:
        return sanitize_line("Dado: ", given_data)            
    if and_data:
        return sanitize_line("E: ", and_data)        
    if when_data:
        return sanitize_line("Quando: ", when_data)        
    if then_data:
        return sanitize_line("Entao: ", then_data)

# Create a .csv dump and write dbb data inside
def create_file(root, name, data_dump_path):
    file = open(os.path.join(root, name))
    lines = file.readlines()
    with open(data_dump_path + name+ '_dump_bdd.csv','w') as f:
        write_file = csv.writer(f)
        for line in lines:
            item = ret_bdd(line.strip())
            if item:
                if 'Teste' in item:
                    write_file.writerow([''])
                    write_file.writerow([name])    
                write_file.writerow([item])

# Script entrypoint
def scpt_entrypoint(path):
    data_dump_path = path + "/DataDump/" 
    scan_path = os.getcwd()
    print("\n Dumps stored in folder called \"DataDump\"...")    
    print("\n Scan folder... " + scan_path)    
    if not os.path.exists("DataDump"):
        os.makedirs(data_dump_path)
    for root, dirs, files in os.walk(scan_path, topdown=False):
        for name in files:
                if 'fixture' not in root:
                    if '.groovy' in name:
                        print("processing..."+name)
                        #create_file(root, name, data_dump_path)      

# validate command-line Args
def validate_execute_path(args):
    if args.rootfolder == 'empty':
        print 'I need a path for a script dump'
    else:
        if os.path.exists(args.rootfolder):
            print("Store in folder: "+args.rootfolder)
            scpt_entrypoint(args.rootfolder)    
        else:
            print("Path not exists!")

# command-line Args
parser = argparse.ArgumentParser(description='Parse from .groovy BDD tests blocks (given, when, then, and) and saves in .csv files')
parser.add_argument('-r','--rootfolder', default="empty", help='root path from script dump ex: /home/user/folder/')

validate_execute_path(parser.parse_args())