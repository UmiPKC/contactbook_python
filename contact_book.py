#creating a contact book that connects to sqlite3 using the python sqlite API
#lets you see all contacts, see specific ones, update contacts, add new contacts, delete old contacts, delete all contacts
#everytime an action is done, user is returned to main 'screen' and is asked what to do next -- while loop
#when done, remember to close connection() object

import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """creates sqlite Connection() object
    :param db_file: database file """
    
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        
    except:
        print('something')
    
    return conn

def create_table(conn, new_table_sql):
    """ creates a new table using CREATE TABLE
    :param conn: Connection object
    :param new_table_sql: CREATE TABLE statement """
    
    cur = conn.cursor()
    cur.execute(new_table_sql)
    conn.commit()

def add_contact(conn, contact_info):
    """adds a row to the contacts table using INSERT INTO
    conn: Connection object
    contact_info: tuple of values """
    
    sql = """ INSERT INTO contacts (name, email, phone, address) VALUES (?, ?, ?, ?) """
    cur = conn.cursor()
    cur.execute(sql, contact_info)
    conn.commit()
    print("\nAdded new contact")

def update_contact_column(conn, row_id, column_id, contact_info):
    """updates a column value of a specific row
    conn: connection object
    row_id: row ID number
    column_id: column name string 
    contact_info: new value to update with
    """
    
    sql = """ UPDATE contacts
              SET """ + column_id + """ = ?
              WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, (contact_info, row_id))
    conn.commit() 
    print("\nUpdated %s of row %d" % (column_id, row_id))

def update_entire_contact(conn, contact_info):
    """updates an entire row
    conn: connection object
    contact_info: tuple of new values - must also include row ID at the end """
    
    sql = """ UPDATE contacts
              SET name = ?, email = ?, phone = ?, address = ?
              WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, contact_info)
    conn.commit()
    print("\nUpdated row")

def delete_contact(conn, row_id):
    """deletes a row using DELETE FROM
    conn: connection object
    row_id: row ID number """
    
    sql = """ DELETE FROM contacts WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, (row_id,))
    conn.commit()
    print("\nDeleted row %d" % row_id)

def delete_all_contacts(conn):
    """deletes all rows using DELETE FROM 
    conn: connection object """
    
    sql = """ DELETE FROM contacts """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("\nDeleted all contacts")

def view_all_contacts(conn):
    """prints full contact list using SELECT 
    conn: connection object """
    
    sql = """ SELECT * FROM contacts """
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    
    print("\nPrinting all contacts: \n")
    for row in rows:
        print(row)

def view_contact(conn, row_id):
    """printing specific row using SELECT
    conn: connection object
    row_id: row ID number """
    
    sql = """ SELECT * FROM contacts WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, (row_id,))
    rows = cur.fetchall()
    
    print("\nPrinting contact #%d" % row_id)
    for row in rows:
        print(row)
    
def main():

    db_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'SQLite', 'demobase.db')
    new_table_sql = """ CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        address TEXT ); """
    conn = create_connection(db_path)      
    create_table(conn, new_table_sql)
    
    print("Welcome to your contact book! What would you like to do?\n")
    
    while True:
        print("\n---------------------------------------")
        print("\n1. View all contacts 2. View one contact 3. Add a contact 4. Update an entire contact 5. Update a value of a preexisting contact 6. Delete a contact 7. Delete all contacts\n")
        user_input = input("? ")
            
        if user_input == "1":
            view_all_contacts(conn)
                
            print("\nDone? (Y/N) ")
            user_done = input()
                
            if user_done == "Y" or user_done == "y":
               break
            else:
                continue
            
        if user_input == "2":
            print("\nWhich row would you like to see?")
            row_id = int(input("Row # "))
            view_contact(conn, row_id)

            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == "Y" or user_done == "y":
               break
            else:
                continue

        if user_input == "3":
            con_name = input("Name? ")
            con_email = input("Email? ")
            con_phone = input("Phone number? ")
            con_address = input("Address? ")
            
            contact_info = (con_name, con_email, con_phone, con_address)
            add_contact(conn, contact_info)
            
            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == 'Y' or user_done == 'y':
                break
            else:
                continue
                
        if user_input == "4":
            con_id = int(input("Contact ID? "))
            con_name = input("Name? ")
            con_email = input("Email? ")
            con_phone = input("Phone number? ")
            con_address = input("Address? ")
            
            contact_info = (con_name, con_email, con_phone, con_address, con_id)
            update_entire_contact(conn, contact_info)

            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == 'Y' or user_done == 'y':
                break
            else:
                continue
             
        if user_input == "5":
            con_id = int(input("Contact ID? "))
            column_name = input("Which column would you like to update? (name, phone, email, address) ") 
            new_value = input("New value? ")
            
            update_contact_column(conn, con_id, column_name, new_value)   
            
            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == 'Y' or user_done == 'y':
                break
            else:
                continue
        
        if user_input == "6":
            con_id = int(input("Contact ID? "))
            
            confirm = input("Are you sure you want to delete contact #%d? (Y/N)" % con_id)
            if confirm == "y" or confirm == "Y":
                delete_contact(conn, con_id)   
            
            else:
                print("Backing out.")
                  
            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == 'Y' or user_done == 'y':
                break
            else:
                continue  
                
        if user_input == "7":
            confirm = input("Are you sure you want to delete ALL contacts? (Y/N)")
            if confirm == "y" or confirm == "Y":
                delete_all_contacts(conn)
            
            else:
                print("Backing out.")
            
            print("\nDone? (Y/N) ")
            user_done = input()
            if user_done == 'Y' or user_done == 'y':
                break
            else:
                continue
    
    conn.close()                                                                         
if __name__ == "__main__":
    main()
