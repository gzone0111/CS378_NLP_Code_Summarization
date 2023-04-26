import matplotlib.pyplot as plt
import sys
import ast
import os
def add_list_to_dict(d,l):
    for k,v in zip(d.keys(),l):
        d[k].append(v)


if __name__ == "__main__":
    model_name = sys.argv[1]
    cwd = os.getcwd()
    p = r'../tmp/'+model_name+r'.txt'
    condition = 'train: Epoch'
    plot_type = sys.argv[2]
    valid = {
        'epoch':[],
        'bleu':[],
        'rouge_l':[],
        'precision':[],
        'recall':[],
        'f1':[],
        'examples':[],
        'valid_time':[]
    }
    train = {
        'epoch':[],
        'ml_loss':[],
        'perplexity':[],
        'time_for_epoch':[]
    }
    if plot_type=='valid':
        condition = 'dev valid official'
        
    with open(p) as f:
        lines = f.readlines()
        for line in lines:
            if plot_type =='train':
                if condition in line:
                    append_list = []
                    values_list = line.split('|')
                    append_list.append(int(values_list[0].split(' ')[-2]))
                    append_list.append(float(values_list[1].split('=')[1].strip()))
                    append_list.append(float(values_list[2].split('=')[1].strip()))
                    append_list.append(float(values_list[3].split('=')[1].split('(')[0].strip()))

                    add_list_to_dict(train,append_list)

                    
            elif plot_type == 'valid':
                if condition in line:
                    append_list = []
                    values_list = line.split('|')
                    append_list.append(int(values_list[0].split('=')[1].strip()))
                    append_list.append(float(values_list[1].split('=')[1].strip()))
                    append_list.append(float(values_list[2].split('=')[1].strip()))
                    append_list.append(float(values_list[3].split('=')[1].strip()))
                    append_list.append(float(values_list[4].split('=')[1].strip()))
                    append_list.append(float(values_list[5].split('=')[1].strip()))
                    append_list.append(float(values_list[6].split('=')[1].strip()))
                    append_list.append(float(values_list[7].split('=')[1].split('(')[0].strip()))

                    add_list_to_dict(valid, append_list)
    
    if plot_type == 'train':
        keys = list(train.keys())
        for i in range(len(keys)):
            if i == 0:
                continue
            plt.plot(train[keys[0]],train[keys[i]],label=keys[i])
            plt.title(f'plot for {keys[0]} against {keys[i]}')
        plt.show()
    if plot_type == 'valid':
        keys = list(valid.keys())
        for i in range(len(valid.keys())):
            if i == 0:
                continue
            plt.plot(valid[keys[0]],valid[keys[i]],label=keys[i])
            plt.title(f'plot for {keys[0]} against {keys[i]}')
        plt.show()
                
