import os
import textstat
import sys
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
def print_np_stat(arr,metric,set_name):
    print(f"{set_name}'s {metric} Minimum:{arr.min()}")
    print(f"{set_name}'s {metric} Maximum:{arr.max()}")
    print(f"{set_name}'s {metric} Mean:{arr.mean()}")
    print(f"{set_name}'s {metric} Standard deviation:{arr.std()}")
    print(f"{set_name}'s {metric} Variance:{arr.var()}")




if __name__ == '__main__':
    language = sys.argv[1]
    list_of_sets = ['original_data','repro_data']
    file_names_ext = ['javadoc.original']


    for s in list_of_sets:
        syn_f_score_array = []
        syn_g_score_array = []
        rd_f_score_array = []
        lex_d_score_array = []
    # get list of index to remove in example
        for ext in file_names_ext:
            # do code_subtoken first
            input_path = os.getcwd()+r'/'+language+r'/'+s+r'/'+'train/'+ext
            output = []
            with open(input_path, encoding='utf8') as f:
                lines = f.readlines()
                for line in lines:
                    syn_f_score_array.append(textstat.flesch_kincaid_grade(line))
                    syn_g_score_array.append(textstat.gunning_fog(line))
                    rd_f_score_array.append(textstat.flesch_reading_ease(line))
                    words = word_tokenize(line)
                    ttr = len(set(words)) / len(words)
                    lex_d_score_array.append(ttr)
            syn_f_score_array = np.array(syn_f_score_array)
            syn_g_score_array = np.array(syn_g_score_array)
            rd_f_score_array = np.array(rd_f_score_array)
            lex_d_score_array = np.array(lex_d_score_array)
            print_np_stat(syn_f_score_array,'Flesch-Kincaid Grade Level',s)
            print_np_stat(syn_g_score_array,'Gunning Fog Index',s)