import os
import textstat
import sys
if __name__ == '__main__':
    language = sys.argv[1]
    list_of_sets = ['original_data','repro_data']
    file_names_ext = ['javadoc.original']


    for s in list_of_sets:
        f_score=0
        g_score=0
    # get list of index to remove in example
        for ext in file_names_ext:
            # do code_subtoken first
            input_path = os.getcwd()+r'/'+language+r'/'+s+r'/'+'train/'+ext
            output = []
            with open(input_path, encoding='utf8') as f:
                lines = f.readlines()
                for line in lines:
                    f_score += textstat.flesch_kincaid_grade(line)
                    g_score += textstat.gunning_fog(line)
            print(f_score/len(lines))
            print(g_score/len(lines))
    