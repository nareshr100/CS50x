import numpy as np
import csv
import sys
import collections


def main():
    
    if (len(sys.argv) != 3):
        
        sys.exit("Usage: dna.py -csv -sequence")
    
    # get file names
    csvname = sys.argv[1]
    sequence = sys.argv[2]
    
    # open CSV file and store in memory
    try:
        open(csvname)
    except OSError:
        print('cannot open', csvname)

    data_list = []
    
    with open(csvname, newline='') as csvfile:
        reader1 = list(csv.reader(csvfile))
        data_list = reader1
    
    # open DNA sequence and store to memory
    try:
        f = open(sequence, 'r')
        contents_seq = f.read()
    except OSError:
        print('cannot open', sequence)
        
    # count STRs in sequence
    count = count_str(data_list, contents_seq)
    
    # check data to see if count matches any keys
    for i in data_list:
        
        # set match bool to false initially
        match = False
        
        # check each entry in line with entry in count
        for j in range(1, len(i)):
            
            # ignore first line of data_list
            if (i[0] == 'name'):
                break
            
            elif (int(i[j]) == int(count[j-1])):
                match = True
                
            else:
                match = False
                break
        
        if (match):
            return print(i[0])
            
    return print("No match")
        
# function to count STRs


def count_str(data_list, contents_seq):
    
    names = []
    names_str = []
    
    for i in range(1, len(data_list)):
        
        names.append(data_list[i][0])
    
    for i in range(1, len(data_list[0])):
        
        names_str.append(data_list[0][i])

    # create empty counting array
    count = np.zeros(len(names_str))
    
    # count number of consecutive STRs for each in names_str
    for i in range(len(names_str)):
        
        name = names_str[i]
        counter = 0
        j = 0
        
        while (j < len(contents_seq)):
            
            if (contents_seq[j:j+len(name)] == name):
                
                counter += 1
                j += len(name)
                
            elif (counter > count[i]):
                
                count[i] = int(counter)
                counter = 0
                j += 1
            else:
                
                counter = 0
                j += 1
    
    return count
    
    
main()