from database import *


def suggestBooktoBuy(budget):
    """
    Suggest books to librarian based on budget.
    """

    trendingBook = trending_book()
    trendingBookPrice = get_price(trendingBook)
    cost = 0
    count = 0

    while(cost<=budget):
        cost += trendingBookPrice
        count += 1
    
    count = count - 1

    s1 = """Based on the current book withdrawal trends,
    book_ID {:} is on high demand.
    
    According to the budget, you can buy {:} copies
    at £{:} per unit.""".format(trendingBook, count, trendingBookPrice)

    return s1

##### TEST #####

# print(suggestBooktoBuy(49))