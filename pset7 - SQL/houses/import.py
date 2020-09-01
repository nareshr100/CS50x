import sys
import csv
from cs50 import SQL


def main():
    
    # check if filename entered as command-line argument
    if (len(sys.argv) != 2):
        
        sys.exit("Usage: import.py -filename")
    
    # read student data from csv file + insert data into students.db with SQl
    name = house = birth = str(0)
    db = SQL('sqlite:///students.db')
    
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            name = row['name']

            # split name into first middle and last
            name = name.split()
            f = m = l = str(0)
            
            if (len(name) == 2):
                
                f = name[0]
                m = None
                l = name[1]
                
            elif (len(name) == 3):
                
                f = name[0]
                m = name[1]
                l = name[2]
            
            query = 'INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)'
            db.execute(query, f, m, l, row['house'], row['birth'])
    
    
main()