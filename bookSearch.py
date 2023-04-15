"""

Your program should include functionality to search for a book based on its title. Given a search term (e.g.: “Treasure Island”), your program should 
return a complete list of books with all their associated information (e.g., title, author, genre and loan availability, etc.). 

This module allows librarian to search for any book.

Upon a succesful search, the output will return a complete list of books with all their associated information (e.g., title, author, genre and loan 
availability, etc.)

"""
from database import *

def search_result(k):
    return search_book2(k)

#     frame1 = Frame(window, bg = 'red')
#     entry1 = Entry(frame1, padx = 40, pady = 20)
#     label1 = Label(frame1, text = 'Enter Book Name')
#     e = entry1.get()
#     search = Button(frame1, text = 'Search', command=search_book(e), padx=30, pady=10)
