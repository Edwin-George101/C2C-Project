import sqlite3

conn = sqlite3.connect('example.db')  # This creates or opens the file 'example.db' as a database
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE student
            (id integer primary key, name text, age integer, grade text, gpa real)''')
conn.commit()
conn.close()

print("Hello User!")
action = input("Welcome to the best bank in the world! We can check your balance, deposit funds, withdraw funds, create an account, delete an account, and lastly modify an account. What would you like to do? ")
print("I would like to " + action)

