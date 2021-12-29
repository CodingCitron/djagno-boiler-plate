import string
import random

def changeToObject(list, cursor):
    if list is None: return []  
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in list:
        insertObject.append( dict(zip( columnNames , record )))
    return insertObject

def randomPwd():
    number_of_strings = 5
    length_of_string = 10
    
    for x in range(number_of_strings):
        return (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))