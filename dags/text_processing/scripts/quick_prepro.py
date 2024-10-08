#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:52:49 2020

@author: antonio
Quick preprocessing for txt files
"""
import os
import argparse
import re
import unicodedata
import codecs

def argparser():
    '''
    DESCRIPTION: Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("-d", "--datapath", required = True, dest = "path", 
                        help = "path to directory with txt files")
    return parser.parse_args().path

pattern = re.compile("[^\S+\r\n]")

def quick_prepro(file, old2new_simple, old2new_regex, pattern, r):
    '''
    Substitute/remove patterns in text file
    
    Parameters
    ----------
    file: str
        path to .txt file
    old2new_simple: dict
        Substitution patterns that will be dealt with str.replace() python method
        key: old pattern
        value: new pattern
    old2new_regex: dict
        Substitution patterns that will be dealt with re.sub() python method
        key: old pattern
        value: new pattern
    
    Returns
    -------
    None
    '''
    
    # Open file
    print(file)
    txt = open(os.path.join(r, file)).read()
    
    # Quick preprocessing
    for k,v in old2new_simple.items():
        txt = txt.replace(k, v) 
    for k,v in old2new_regex.items():
        txt = re.sub(k,v, txt)
        
    # Remove all multiple whitespaces by ' ' except \n and \r
    txt = pattern.sub(' ', txt)

    # Remove whitespaces at the beginning and ending of string
    tmp = []
    for line in txt.split('\n'):
        tmp.append(line.strip())
    txt = '\n'.join(tmp).strip('\n')


    # Rewrite good file with NFKC Unicode
    with codecs.open(os.path.join(r, file), 'w', 'utf-8') as f:
        f.write(unicodedata.normalize('NFKC', txt).encode("utf-8").decode("utf-8"))

def quick_preprosessing(output_dir, **kwargs):
    config_dict = kwargs['dag_run'].conf if kwargs['dag_run'].conf != {} else None
    source_dir = config_dict['source_dir']
    dest_dir_temp = f"{output_dir}{source_dir.replace('/storage','')}"
    os.makedirs(dest_dir_temp, exist_ok=True)
    
    # Define substitution dictionaries
    old2new_simple = {u'\uf0fc':'', # Remove 
                      u'\uf0b7':'', # remove 
                      u'”':'"', # substitute ” by "
                      u'\r':'\n', # substitute \r by \n
                      u'“':'"', # substitute “ by "
                      u'’':'"'} # substitute ’ by '
                      #u'\uFFFD':' '} # Subst � by blankspace -> I am not doing this
    
    old2new_regex = {':(?=[A-Za-z])':': ', # add space after all :
                     '•(?=[A-Za-z])':'• '} # add space after all •
    
    for r, d, f in os.walk(dest_dir_temp):
        for file in f:
            if file.split('.')[-1] != 'txt':
                continue
            quick_prepro(file, old2new_simple, old2new_regex, pattern, r)