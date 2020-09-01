import sys
import csv
from cs50 import SQL

db = SQL('sqlite:///students.db')
query = 'DELETE FROM students'
students = db.execute(query)