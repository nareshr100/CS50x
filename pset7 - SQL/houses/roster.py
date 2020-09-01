import sys
import csv
from cs50 import SQL


def main():

    # check if house entered as command-line argument
    if (len(sys.argv) != 2):
        if sys.argv[1] != "Gryffindor" or sys.argv[1] != "Slytherin" or sys.argv[1] != "Hufflepuff" or sys.argv[1] != "Ravenclaw":
            sys.exit("Usage: roster.py -house")

    # query students.db for students in certain house
    house = sys.argv[1]
    db = SQL('sqlite:///students.db')
    query = 'SELECT * FROM students WHERE house = ? ORDER BY last ASC, first ASC'
    students = db.execute(query, house)

    for i in students:

        if (i['middle'] == None):
            print(i['first'] + " " + i['last'] + ', born' + " " + str(i['birth']))
        else:
            print(i['first'] + " " + i['middle'] + " " + i['last'] + ', born' + " " + str(i['birth']))


main()