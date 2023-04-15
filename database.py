import pickle
import sqlite3
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

def insert_into_members(count,max_count):
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    for i in range(count, max_count):
        curs.execute("""INSERT INTO Members VALUES
        ('{:}')""".format(i))
        conn.commit()
    conn.close()

def insert_into_books(a,b,c,d,e,f):
    """
    THIS FUNCTION IS USED TO POPULATE THE Book_Info TABLES in 
    Library.db by passing the 6 paramaters as strings.

    The 6 paramaters a, b, c, d, e and f stands for:

    a -> ID (int)
    b -> Genre (string)
    c -> Title (string)
    d -> Author (string)
    e -> Purchase Price (int)
    f -> Purchase Date (string)
    """

    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()

    curs.execute("""INSERT OR IGNORE INTO Book_Info_1 VALUES
    ('{:}','{:}','{:}')""".format(a,c,f))

    curs.execute("""INSERT OR IGNORE INTO Book_Info_2 VALUES
    ('{:}','{:}','{:}','{:}')""".format(c,b,d,e))

    curs.execute("""INSERT OR IGNORE INTO Reservation_Status 
    VALUES('{:}','YES')""".format(a))

    conn.commit()
    conn.close()

def insert_into_loan_history(a,b,c,d,e):
    """
    THIS FUNCTION IS USED TO POPULATE THE Loan_History TABLE in 
    Library.db by passing the 5 paramaters as strings.

    The 6 paramaters a, b, c, d, e stands for:

    a -> Book_ID (int)
    b -> Reservation_Date (string)
    c -> Checkout_Date (string)
    d -> Return_Date (string)
    e -> Member_ID (int)
    """

    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()

    curs.execute("""INSERT INTO Loan_Record VALUES
    ('{:}','{:}','{:}','{:}','{:}')""".format(a,b,c,d,e))
    conn.commit()
    conn.close()

def update_into_loan_history(book_id,member_id,date):
    """
    THIS FUNCTION IS USED TO POPULATE THE Loan_History TABLE in 
    Library.db by passing the 3 paramaters.
    """

    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()

    curs.execute("""UPDATE Loan_Record 
    SET Return_Date = '{:}'
    WHERE (Book_ID = {:}) AND (Member_ID = {:}) 
    """.format(date,book_id,member_id))
    conn.commit()
    conn.close()


def update_into_loan_history_if_already_reserved(book_id,member_id,date):
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()

    curs.execute("""UPDATE Loan_Record 
    SET Checkout_Date = '{:}'
    WHERE (Book_ID = {:}) AND (Member_ID = {:})
    """.format(date,book_id,member_id))
    conn.commit()
    conn.close()

def start():

    """
    IMPORTANT, PLEASE READ THIS COMMENT

    This function start() is used only once and then 
    deleted or commented out because this function is 
    used to initially populate the database automatically
    from Book_Info.txt exactly once.
    """

    f = open('Book_info.txt', 'r')
    for x in f:
        r = x.rstrip('\n')
        t = r.split('|')

        for i in range(len(t)):
            t[i] = str(t[i])
            l = len(t[i])
            for j in range(l):
                j = j
                if t[i][l-1] != ' ':
                    t[i] = t[i][:l]
                    break
                else:
                    l = l-1

        if t[0][:2] != 'ID':
            insert_into_books(t[0], t[1], t[2], t[3], t[4], t[5])
        else:
            pass

def start2():

    """
    IMPORTANT, PLEASE READ THIS COMMENT

    This function start2() is used only once and then 
    deleted or commented out because this function is 
    used to initially populate the database automatically
    from Loan_Reservation_History.txt
    """

    f = open('Loan_Reservation_History.txt', 'r')
    for x in f:
        r = x.rstrip('\n')
        t = r.split(',')

        for i in range(len(t)):
            t[i] = str(t[i])
            l = len(t[i])
            for j in range(l):
                j = j
                if t[i][l-1] != ' ':
                    t[i] = t[i][:l]
                    break
                else:
                    l = l-1
        insert_into_loan_history(t[0], t[1], t[2], t[3], t[4])


def clear_table(Table_Name):
    """
    This function clears all data in a table
    How to?
    Pass table name in the function as string
    """

    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    curs.execute("""DELETE FROM {:}""".format(Table_Name))
    conn.commit()
    conn.close()   

def search_book(Title):
    
    #Returns a list of Books that is similar to the title parameter.
    
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """Select Book_ID, Genre, Book_Info_1.Title, Author, Purchase_Price, Purchase_Date
            FROM Book_Info_1 INNER JOIN Book_Info_2
            ON Book_Info_1.Title=Book_Info_2.Title 
            WHERE Book_Info_1.Title LIKE '%{:}%'""".format(str(Title))
    curs.execute(qu)
    rows = curs.fetchall()

    s = ''
    #print("""Index\tGenre\tTitle\tAuthor\tPurchase Price £\tPurchase Date""")

    for r in rows:
        for col in r:
            s = s + str(col) + '\t'
            #print(col,end='\t')
        s = s +'\n'
        #print()
    conn.close()
    return s

def search_book2(Title):
    # Returns a dataframe of Books that is similar to the title parameter.
    conn = sqlite3.connect('Library.db')
    qu = """Select Book_Info_1.Book_ID, Genre, Book_Info_1.Title, Author, Purchase_Price, Available
            FROM Book_Info_1 INNER JOIN Book_Info_2
            ON Book_Info_1.Title = Book_Info_2.Title
            INNER JOIN Reservation_Status
            ON Book_Info_1.Book_ID = Reservation_Status.Book_ID  
            WHERE Book_Info_1.Title LIKE '%{:}%'""".format(str(Title))
    df = pd.read_sql_query(qu, conn)
    conn.close()
    if df.empty:
        s = "No result"
        return s
    else:
        return df


def print_all():
    # Prints every record based on the given SQL Query
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """Select Book_ID, Genre, Book_Info_1.Title, Author, Purchase_Price, Purchase_Date
            FROM Book_Info_1 INNER JOIN Book_Info_2
            ON Book_Info_1.Title=Book_Info_2.Title"""
    curs.execute(qu)
    rows = curs.fetchall()

    print("""Index\tGenre\tTitle\tAuthor\tPurchase Price £\tPurchase Date""")

    for row in rows:
        for col in row:
            print(col,end='\t\t\t\t')
        print()
    conn.close()


def storeMiscImage(Name, Image):

    #We store additional images like icons using this function.
    

    try:
        conn = sqlite3.connect('Library.db')
        curs = conn.cursor()
        blob_query = """
        INSERT INTO Misc_Images(Name, Image) VALUES (?,?)
        """
        img = mpimg.imread(Image)
        miscimg = pickle.dumps(img)

        data_tuple = (Name, miscimg)
        curs.execute(blob_query, data_tuple)
        conn.commit()
        curs.close()
        print('Sucessfully inserted')
        
    except sqlite3.Error as error:
        print("FAILED to insert image into Database")
    finally:
        if conn:
            conn.close()
            print('close')


def getMiscImage(imageName):
    
    #We retrieve additional images like icons using this function.
    
    try:
        conn = sqlite3.connect('Library.db')
        curs = conn.cursor()

        fetch_query_blob = """SELECT * FROM Misc_Images
        WHERE Name = ?
        """
        curs.execute(fetch_query_blob, (imageName,))
        record = curs.fetchall()
        for row in record:
            #print('Name = ', row[0])
            photo = pickle.loads(row[1])
            imgplot = plt.imshow(photo)
        curs.close()
        
        # plt.axes.get_xaxis().set_visible(False)
        # plt.axes.get_yaxis().set_visible(False)
        return photo
        #plt.show()
        

    except:
        print("Failed to read blob")
    finally:
        if conn:
            conn.close()


def validate_member(member_id):
    """
    This function is used to validate if
    member ID entered while borrowing or
    returning a book is correct.
    """
    if member_id>=1000 and member_id<=9999:
        return True
    else:
        return True


def validate_bookID_return(book_id):

    # Checks if book is not available in library to return by using book_id

    temp = False
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """
    SELECT *
    FROM Reservation_Status
    WHERE Book_ID = {:}
    """.format(book_id)
    curs.execute(qu)
    rows = curs.fetchall()
    if len(rows)==0:
        temp = 'Wrong'
    else:
        if rows[0][1]=='YES':
            temp = False
        elif rows[0][1] == 'NO':
            temp = True
    return temp


def validate_bookID_checkout(book_id):

    # Checks if book is available in library to borrow by using book_id
    temp1 = False
    temp2 = False
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()

    qu = """
    SELECT *
    FROM Reservation_Status
    WHERE Book_ID = {:}
    """.format(book_id)
    curs.execute(qu)
    rows = curs.fetchall()
    if len(rows)==0:
        temp1 = 'Wrong'
        return temp1
    else:
        if rows[0][1]=='YES':
            temp2 = True
            return temp2
        elif rows[0][1] == 'NO':
            temp2 = False
            return temp2


# Writing query to add count of books

"""conn = sqlite3.connect('Library.db')
curs = conn.cursor()
curs.execute("ALTER TABLE Book_Info_2 ADD Count INTEGER")

conn.commit()
conn.close()
"""

# Done

def insert_count():

    # USED to generate how many copies of one book do we have

    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    l1=[]
    l2=[]
    q1 = """
        SELECT Title 
        FROM Book_Info_2
        """
    curs.execute(q1)
    rows = curs.fetchall()
    for row in rows:
        for cols in row:
            l1.append(cols)
            q2 = "SELECT COUNT(*) FROM Book_Info_1 WHERE Title = '{:}'".format(cols)
            curs.execute(q2)
            l2.append(curs.fetchone())
  
    l3 = []
    for i in range(0,len(l2)):
        t=(l2[i][0])
        l3.append(t)

    for i in range(0, len(l3)):

        q3 = """
        UPDATE Book_Info_2
        SET Count = {:}
        WHERE Title = '{:}'
        """.format(l3[i],l1[i])

        curs.execute(q3)
        conn.commit()

    conn.close()

### COUNT
def increase_count(book_title):
    """
    Increase count is used to increase the quantity of a book.
    This is very useful when a book is returned to the Library
    """
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """
    SELECT Count
    FROM Book_Info_2
    WHERE Title = '{:}'
    """.format(book_title)
    curs.execute(qu)
    c = curs.fetchall()
    c = int(c[0][0])
    c+=1
    qu = """
    UPDATE Book_Info_2
    SET Count = {:}
    WHERE Title = '{:}'
    """.format(c, book_title)
    curs.execute(qu)
    conn.commit()
    conn.close()

def decrease_count(book_title):
    """
    Decrease count is used to decrease the quantity of a book.
    This is very useful when a book is withdrwan from the Library
    """
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    temp = True
    qu = """
    SELECT Count
    FROM Book_Info_2
    WHERE Title = '{:}'
    """.format(book_title)
    curs.execute(qu)
    c = curs.fetchall()
    c = int(c[0][0])
    if c>0:
        c = c - 1
        qu = """
        UPDATE Book_Info_2
        SET Count = {:}
        WHERE Title = '{:}'
        """.format(c, book_title)
        curs.execute(qu)
        conn.commit()
        t = True
    else:
        t = False
    conn.close()
    return t

def get_bookname_from_bookID(book_ID):
    #Just a simple function to get a book's name by the book's ID
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """
    SELECT Title
    FROM Book_Info_1
    WHERE Book_ID = {:}
    """.format(book_ID)
    curs.execute(qu)
    c = curs.fetchall()
    c = str(c[0][0])
    conn.close()
    return c


## AVAILABILITY
def change_availability(book_id):
    #Checks whether a book is available to checkout based on its ID
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    qu = """
    SELECT Available
    FROM Reservation_Status
    WHERE Book_ID = '{:}'
    """.format(book_id)
    curs.execute(qu)
    c = curs.fetchall()
    if(c[0][0]=='YES'):
        qu = """UPDATE Reservation_Status 
        SET Available='NO'
        WHERE Book_ID={:}""".format(book_id)
        curs.execute(qu)
        conn.commit()
    elif(c[0][0]):
        qu = """UPDATE Reservation_Status 
        SET Available='YES'
        WHERE Book_ID={:}""".format(book_id)
        curs.execute(qu)
        conn.commit()
    conn.close()


def trending_book():
    """
    Gives us the book that is in most demand.
    We retrieve the book_ID by calculating the 
    maximum number of time a single book
    has been borrowed or reserved.
    """
    max = 0
    b_id = 0
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    for i in range(1,51):
        qu = """SELECT COUNT(Book_ID)
        FROM Loan_Record
        WHERE Book_ID={:}""".format(i)
        curs.execute(qu)
        c = curs.fetchall()
        c = int(c[0][0])
        if c>max:
            max = c
            b_id = i
    return b_id

def get_price(book_id):
    # A simple function to get the price of a book based on its unique ID
    conn = sqlite3.connect('Library.db')
    curs = conn.cursor()
    temp = get_bookname_from_bookID(book_id)
    qu = """
    SELECT Purchase_Price from Book_Info_2
    WHERE Title = '{:}'
    """.format(temp)
    curs.execute(qu)
    c = curs.fetchall()
    c = int(c[0][0])
    return c



##### TEST #####


#get_price(1)
# Checkout BOOK Successful

# print(trending_book())
#change_availability(1)
#increase_count('Dune')
# print(get_bookname_from_bookID(1))
# insert_count()
# increase_count('Harry Potter')
#decrease_count('Harry Potter')
# print(validate_bookID_checkout(250))



# TEMPORARY EXECUTION ZONE
# df=pd.read_table('Loan_Reservation_History.txt')

# conn = sqlite3.connect('Library.db')
# curs = conn.cursor()
# curs.execute("""CREATE TABLE IF NOT EXISTS Loan_Record(
#     Book_ID INTEGER NOT NULL,
#     Reservation_Date TEXT,
#     Checkout_Date TEXT,
#     Return_Date TEXT,
#     Member_ID INTEGER)""")

# curs.execute("""CREATE TABLE IF NOT EXISTS Book_Info_2(
#     Title TEXT NOT NULL PRIMARY KEY,
#     Genre TEXT,
#     Author TEXT,
#     Purchase_Price INTEGER)""")

      


# clear_table('Book_Info_1')
# clear_table('Book_Info_2')
# clear_table('Loan_Record')
# print(search_book('Book_1'))
# print(search_book2('Dun'))
# print_all()
# drop_table('Book_Info')
# start()
# storeMiscImage('Icon', 'icon.ico')
# t = getMiscImage('Icon')
# print(t)
# start2()
