import sqlite3

connect = sqlite3.connect('openrecycle.db')
c = connect.cursor()

c.execute('''DROP TABLE users''')

connect.commit()
connect.close()