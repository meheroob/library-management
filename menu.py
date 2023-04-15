from tkinter import *
from tkinter import ttk
from bookSearch import *
from bookReturn import *
from bookCheckout import *
from bookSelect import *

class Library_Management_App(Tk):
    """
    This is the class to create the main app.
    Here, we specify how to navigate among different
    screens like searchBook, returnBook, etc. 
    """

    def __init__(self, *args, **kwargs) -> None:
        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self, default="icon.ico")
        Tk.title(self, "Library Management System")
        Tk.geometry(self, "1280x720")
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}
        """
        This is the most important step in constructing the app.
        We iterate through the frames by looping F in all the possible frames.
        If we create a new frame, we just have to add it to the tuple!
        """
        for F in (MainMenu, Search_Window, Return_Window, Checkout_Window, Suggest_Window):

            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainMenu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class MainMenu(Frame):

    """
    This is the main menu of the application.
    All the main actions are performed through here.
    We need to get back to the main menu to perform some other task.
    """

    def __init__(self, parent, controller):
        Frame.__init__(self,parent,bg='black',height=720,width=1280)
    
        l = Label(self, text="THE LIBRARY", bg='red',font=('Arial', 25))
        l.pack(padx=10, pady=10)

        button_search = Button(self, text="Search Book",width=1280,height=10,bg='green',command=lambda: controller.show_frame(Search_Window))
        button_search.pack()

        button_return = Button(self, text="Return Book",width=1280, height=10,bg='red',command=lambda: controller.show_frame(Return_Window))
        button_return.pack()

        button_checkout = Button(self, text="Checkout Book",width=1280,bg='aqua', height=10, command=lambda: controller.show_frame(Checkout_Window))
        button_checkout.pack()

        button_suggest = Button(self, text="Suggest Book",width=1280, height =10,bg='black',fg='white',command=lambda: controller.show_frame(Suggest_Window))
        button_suggest.pack()



class Search_Window(Frame):

    """
    This is the search window Frame.
    We display a dataframe of the search input.
    Results are shown even if Book Title is partially entered.
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent,bg='green')

        self.e = Entry(self)
        self.e.pack()
        
        l = Label(self, text='Enter partial/complete book name')
        l.pack()

        submit_button = ttk.Button(self, text='Submit',command=self.submit_click)
        submit_button.pack()

        button_mainmenu = ttk.Button(self, text='Main Menu', command = lambda: controller.show_frame(MainMenu))
        button_mainmenu.pack()

        self.l2 = Label(self, text='RESULT')
        self.l2.pack()
    
    def submit_click(self):
        if(self.e.get()==''):
            self.l2.configure(text = 'Empty. Please type something.')
        else:
            res = search_result(self.e.get())
            self.e.delete(0,END)
            self.l2.configure(text=res)


class Return_Window(Frame):
    """
    This is the return frame. 
    If a book is with a member, it can be entered back in the library database.
    Furthermore, a log is recorded on book checkout.
    """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='red')

        self.e1 = Entry(self)
        self.e1.pack()
        l1 = Label(self, text='Enter book ID')
        l1.pack()

        self.e2 = Entry(self)
        self.e2.pack()
        l2 = Label(self, text='Enter Member ID')
        l2.pack()

        self.e3 = Entry(self)
        self.e3.pack()
        self.l3 = Label(self, text='Enter Date in DD/MM/YYYY')
        self.l3.pack()

        self.l4 = Label(self, text='')
        self.l4.pack()

        submit_button1 = Button(self, text='Submit', command=self.submit_button)
        submit_button1.pack()

        button_mainmenu = Button(self, text='Main Menu', command = lambda: controller.show_frame(MainMenu))
        button_mainmenu.pack()

    def submit_button(self):
        correct = checkreturn(int(self.e1.get()), int(self.e2.get()))
        if correct=='Return_Book':
            finally_return(int(self.e1.get()), int(self.e2.get()), self.e3.get())
            self.l4.config(text="Book returned successfully!")
        else:
            self.l4.config(text=correct)

class Checkout_Window(Frame):

    """
    This is the checkout frame. 
    If a book is available, it can be checked out.
    Furthermore, a log is recorded on book checkout.
    """


    def __init__(self, parent, controller):
        Frame.__init__(self, parent,bg='aqua')

        self.e1 = Entry(self)
        self.e1.pack()
        self.l1 = Label(self, text='Enter book ID')
        self.l1.pack()

        self.e2 = Entry(self)
        self.e2.pack()
        self.l2 = Label(self, text='Enter Member ID')
        self.l2.pack()

        self.e3 = Entry(self)
        self.e3.pack()
        self.l3 = Label(self, text='Enter Date in DD/MM/YYYY')
        self.l3.pack()

        submit_button = Button(self, text='Submit',command=self.submit_click)
        submit_button.pack()

        self.l4 = Label(self, text='')
        self.l4.pack()

        button_mainmenu = Button(self, text='Main Menu', command = lambda: controller.show_frame(MainMenu))
        button_mainmenu.pack()

        self.tempButton = Button(self, text="Reserve Book",command=self.res)

    
    def submit_click(self):
        correct = checkcheckout(int(self.e1.get()), int(self.e2.get()))
        if(correct == 'Checkout'):
            finally_checkout(int(self.e1.get()), int(self.e2.get()), self.e3.get())
            self.l4.config(text="Book checked out successfully!")
        elif(correct == 'Reserve'):
            self.l4.config(text="Sorry, the book is currently on loan! You can still make a reservation!")
            self.tempButton.pack()
        else:
            self.l4.config(text="Invalid credentials, please try again.")

    def res(self):
        reserve_book(int(self.e1.get()), int(self.e2.get()), self.e3.get())
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        self.tempButton.pack_forget()
        self.l4.config(text='')


class Suggest_Window(Frame):

    """
    If you have a budget to buy books and you need some suggestion,
    then just enter the budget in this window and submit
    """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent,bg ='black')

        self.e1 = Entry(self)
        self.e1.pack()
        self.l1 = Label(self, text='Enter budget')
        self.l1.pack()
        self.button_submit = Button(self,text='Submit',command=self.suggest_click)
        self.button_submit.pack()

        self.l2 = Label(self)
        self.l2.pack()

        button_mainmenu = ttk.Button(self, text='Main Menu', command = lambda: controller.show_frame(MainMenu))
        button_mainmenu.pack()
    
    def suggest_click(self):
        s = suggestBooktoBuy(int(self.e1.get()))
        self.l2.config(text=s)



#####################################
##########Application runs###########

app = Library_Management_App()
app.mainloop()

######### Application stop ##########
#####################################
