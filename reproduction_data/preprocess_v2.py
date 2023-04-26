import nltk
import pandas as pd
import re    
import glob
import random
import os
import sys
import ast
from nltk.tokenize import RegexpTokenizer

nl_tokenizer = RegexpTokenizer(r'\w+|[^\w\s\n\r]+')
def remove_nl(text):
    tokens = nl_tokenizer.tokenize(text)
    return ' '.join(tokens)
def remove_special_characters(string):
    pattern = r'[#\'"`\\_]'
    return re.sub(pattern, '', string)
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

# Split camel case string
def split_camel_case(string):
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', string)

# Split snake case string
def split_snake_case(string):
    return string.split('_')
    
def contains_list(lst):
    for elem in lst:
        if isinstance(elem, list):
            return True
    return False
# Split words in list
def split_words_in_list(word_list):
    split_words_list = []
    for word in word_list:
        if '_' in word: # If word is in snake case
            split_words_list += split_snake_case(remove_special_characters(word).lower())
        elif word.isupper(): # If word is in all caps
            split_words_list.append(remove_special_characters(word).lower())
        elif any(c.isupper() for c in word): # If word is in camel case
            split_words_list += split_camel_case(remove_special_characters(word).lower())
        else: # If word is in normal case
            split_words_list.append(remove_special_characters(word).lower())
        
    return split_words_list


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
                if len(tokens)>25:
                    index_list.append(i)



        for ext,out_name in zip(file_names_ext,output_names):
            # do code_subtoken first
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
                        sen = split_words_in_list(ast.literal_eval(line))
                        tokens = ' '.join(sen)
                        output.append(remove_nl(tokens))
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


                
         
