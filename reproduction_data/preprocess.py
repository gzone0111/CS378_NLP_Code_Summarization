import nltk
import pandas as pd
import re    
import glob
import random
import os
import sys
import ast
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')
def remove_lists_by_indices(lst, indices):
    return [sublist for i, sublist in enumerate(lst) if i not in indices]

def split_function_name(name):
    # Convert the name to a string
    name = str(name)
    # Use regular expressions to split the name
    words = re.findall('[A-Z][a-z]*', name)
    # Join the words together with spaces
    return ' '.join(words)

if __name__ == '__main__':
    language = sys.argv[1]
    list_of_sets = ['train','test','valid']
    file_names_ext = ['code_tokens','docstring']
    output_names = ['code.original_subtoken','javadoc.original']


    for s in list_of_sets:
    # get list of index to remove in example
        index_path = os.getcwd()+r'/'+language+r'/'+s+r'/'+s+'.'+'docstring'
        index_list = []
        with open(index_path) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                tokenizer = RegexpTokenizer('\w+')
                tokens = tokenizer.tokenize(ast.literal_eval(lines[i]))
                if len(tokens)>20:
                    index_list.append(i)

        for ext,out_name in zip(file_names_ext,output_names):
            # do subtoken first
            input_path = os.getcwd()+r'/'+language+r'/'+s+r'/'+s+'.'+ext
            output_path = os.getcwd()+r'/'+language+r'/'+s+r'/'+out_name
            output = []
            if ext == 'code_tokens':
                with open(input_path) as f:
                    lines = f.readlines()
                    lines = remove_lists_by_indices(lines,index_list)
                    if len(lines)>50000:
                        lines = random.sample(lines,50000)
                    for line in lines:
                        tokenizer = RegexpTokenizer(r'\w+|[^\w\s]+|[\w.]+\([\w\s,]*\)')
                        tokens = ' '.join(tokenizer.tokenize(' '.join(ast.literal_eval(line)).replace('_',' ')))
                        output.append(tokens)
                with open(output_path,'a') as f:
                    for o in output:
                        f.write(f'{o}\n')
          
            else:
                with open(input_path, encoding='utf8') as f:
                    lines = f.readlines()
                    lines = remove_lists_by_indices(lines,index_list)
                    if len(lines)>50000:
                        lines = random.sample(lines,50000)
                    for line in lines:
                        tokenizer = RegexpTokenizer('\w+')
                        tokens = tokenizer.tokenize(ast.literal_eval(line))
                        output.append(' '.join(tokens).lower()+' .')
                    
                with open(output_path,'a',encoding='utf8') as f:
                    for o in output:
                        f.write(f'{o}\n')


                
         
