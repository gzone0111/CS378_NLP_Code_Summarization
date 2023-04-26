import sys
import ast
import os
class Indexer(object):
    """
    Bijection between objects and integers starting at 0. Useful for mapping
    labels, features, etc. into coordinates of a vector space.

    Attributes:
        objs_to_ints
        ints_to_objs
    """
    def __init__(self):
        self.objs_to_ints = {}
        self.ints_to_objs = {}

    def __repr__(self):
        return str([str(self.get_object(i)) for i in range(0, len(self))])

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.objs_to_ints)

    def get_object(self, index):
        """
        :param index: integer index to look up
        :return: Returns the object corresponding to the particular index or None if not found
        """
        if (index not in self.ints_to_objs):
            return None
        else:
            return self.ints_to_objs[index]

    def contains(self, object):
        """
        :param object: object to look up
        :return: Returns True if it is in the Indexer, False otherwise
        """
        return self.index_of(object) != -1

    def index_of(self, object):
        """
        :param object: object to look up
        :return: Returns -1 if the object isn't present, index otherwise
        """
        if (object not in self.objs_to_ints):
            return -1
        else:
            return self.objs_to_ints[object]

    def add_and_get_index(self, object, add=True):
        """
        Adds the object to the index if it isn't present, always returns a nonnegative index
        :param object: object to look up or add
        :param add: True by default, False if we shouldn't add the object. If False, equivalent to index_of.
        :return: The index of the object
        """
        if not add:
            return self.index_of(object)
        if (object not in self.objs_to_ints):
            new_idx = len(self.objs_to_ints)
            self.objs_to_ints[object] = new_idx
            self.ints_to_objs[new_idx] = object
        return self.objs_to_ints[object]
    
if __name__ == "__main__":
    language = sys.argv[1]
    file_type = sys.argv[2]
    is_repro = sys.argv[3]
    is_2set = sys.argv[4]
    list_of_path = []
    input_path = os.getcwd()
    f_path = ' '
    indexer = Indexer()
    train_test_indexer = Indexer()
    train_dev_indexer = Indexer()
    if is_repro != 'y':
        input_path = r'../NeuralCodeSum/data'
    if file_type == 'doc':
        f_path = input_path+r'/'+language+r'/train'+r'/javadoc.original'
    if file_type == 'code':
        f_path = input_path+r'/'+language+r'/train'+r'/code.original_subtoken'
    
    list_of_path.append(f_path)
    if is_2set =='y':
        list_of_path = [input_path+r'/'+language+r'/train'+r'/javadoc.original',
                        input_path+r'/'+language+r'/test'+r'/javadoc.original',
                        input_path+r'/'+language+r'/dev'+r'/javadoc.original',]
    
    max_len = 0
    min_len = 20000
    count = 0
    print_word_len = []
    for p in list_of_path:
        with open(p) as f:
            lines = f.readlines()
            if 'train' in p and is_2set:
                for line in lines:
                    l = line.split(' ')
                    sen_len = len(l)
                    for word in l:
                        train_dev_indexer.add_and_get_index(word)
                        train_test_indexer.add_and_get_index(word)
                print_word_len.append(len(train_test_indexer))
                print_word_len.append(len(train_dev_indexer))
            elif 'test' in p:
                for line in lines:
                    l = line.split(' ')
                    sen_len = len(l)
                    for word in l:
                        train_test_indexer.add_and_get_index(word)
                print_word_len.append(len(train_test_indexer)-print_word_len[0])
            elif 'dev' in p:
                for line in lines:
                    l = line.split(' ')
                    sen_len = len(l)
                    for word in l:
                        train_dev_indexer.add_and_get_index(word)
                print_word_len.append(len(train_dev_indexer)-print_word_len[1])
    print(print_word_len)
            # for line in lines:
            #     l = line.split(' ')
            #     sen_len = len(l)
            #     for word in l:
            #         indexer.add_and_get_index(word)
            # print(count/len(lines))
            # print(len(indexer))

