"""

A Python module which contains functions used to ask 
the librarian for borrower’s member-ID and the ID of 
the book(s) to be checked out. Then, after performing 
the validity checks and functionality described in the 
previous section, the program should return a message 
letting the librarian know whether they have checked 
out the book(s) successfully.

"""
from database import *

def checkcheckout(book_id, member_id):
    """
    VALIDATES IF Book_ID and Member_ID are correct
    and returns a string.
    The string is used to display error on the screen.
    Else, if it is correct, we move to function finally_checkout()
    structured systematically in the Menu.py file
    """
    first = validate_bookID_checkout(book_id)
    second = validate_member(member_id)
    print(first, second)
    confirm = True

    if(first==True and second==True):
        # CONFIRM CHECKOUT
        confirm = 'Checkout'

    elif(first==True and second==False):

        confirm = 'Invalid Member ID!\n Please correct and try again!'

    elif(first==False and second==True):
        """
        When both inputs are correct but Book is not available
        We ask the user to Reserve the book.
        """
        confirm = 'Reserve'
    
    elif(first==False and second==False):
        print("Incorrect Member ID!")
        confirm = False

    elif(first=='Wrong' and second==True):
        confirm = False

    elif(first=='Wrong' and second==False):
        print("both are wrong!")
        confirm = False
    
    return confirm

def finally_checkout(book_id, member_id, date):
    change_availability(book_id)
    t = get_bookname_from_bookID(book_id)
    decrease_count(t)
    insert_into_loan_history(book_id,'',date,'',member_id)

    with open('log.txt', 'a') as f:
        f.write('\n{:} checked out the book_ID {:} on {:}'.format(member_id, book_id, date))


def reserve_book(book_id, member_id, date):
    insert_into_loan_history(book_id,date,'','',member_id)
    with open('log.txt', 'a') as f:
        f.write('\n{:} reserved the book_ID {:} on {:}'.format(member_id, book_id, date))


# TEST
# finally_checkout()
# print(validate_bookID_checkout(25))
# print(validate_member(1500))
# checkcheckout(25, 1500)