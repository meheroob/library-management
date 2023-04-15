"""
 A Python module which contains functions used to
 ask the librarian for the ID of the book(s) they wish 
 to return and provide either an appropriate error 
 message, or a message letting them know they have 
 returned the book(s) successfully.
 """

from database import *

def checkreturn(book_id, member_id):

    """
    VALIDATES IF Book_ID and Member_ID are correct
    and returns a string.
    The string is used to display error on the screen.
    Else, if it is correct, we move to function finally_return()
    structured systematically in the Menu.py file
    """

    first = validate_bookID_return(book_id)
    second = validate_member(member_id)

    if(first==True and second==True):
        confirm = 'Return_Book'

    else:
        confirm = 'Invalid credentials!\n Please correct and try again!'

    return confirm

def finally_return(book_id,member_id,date):
    """
    1. Change the availability from NO to YES
    2. Increase the count of the book 
    as it is back in the Library (Books have multiple copies with unique ID)
    3. Update Loan_History table
    4. Log the result in log.txt
    """
    change_availability(book_id)
    t = get_bookname_from_bookID(book_id)
    increase_count(t)
    insert_into_loan_history(book_id,'',date,date,member_id)

    with open('log.txt', 'a') as f:
        f.write('\n{:} returned the book_ID {:} on {:}'.format(member_id, book_id, date))

##### TEST #####

# print(validate_bookID_return(1))
# print(validate_bookID_return(3432))