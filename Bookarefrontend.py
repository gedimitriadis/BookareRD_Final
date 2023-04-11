import re
import sqlite3
#import tkinter as tk  # for combobox in reports
from datetime import date, datetime, timedelta
from tkinter import *
from tkinter import messagebox, ttk

from tkscrolledframe import ScrolledFrame

import Bookarebackend
import Reports

# _______________ Bookarefrontend.py creates the GUI of the application____________________________________-

window =Tk()
window.wm_title("Bookare RD")
# get the screen dimension___________________________
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#fulll screen window__________________________________
window.geometry(f'{screen_width}x{screen_height}')
#window.iconbitmap('./assets/bookareLogo.ico')

# create tabs
myNotebook = ttk.Notebook(window)
tab0 = ScrolledFrame(myNotebook)
tab1 = ScrolledFrame(myNotebook)
tab2 = ScrolledFrame(myNotebook)
tab3 = ScrolledFrame(myNotebook)


# Bind the arrow keys and scroll wheel
tab0.bind_arrow_keys(myNotebook)
tab0.bind_scroll_wheel(myNotebook)
tab1.bind_arrow_keys(myNotebook)
tab1.bind_scroll_wheel(myNotebook)
tab2.bind_arrow_keys(myNotebook)
tab2.bind_scroll_wheel(myNotebook)
tab3.bind_arrow_keys(myNotebook)
tab3.bind_scroll_wheel(myNotebook)


# Create a frame within the ScrolledFrame for each tab
inner_frame0 = tab0.display_widget(Frame)
inner_frame1 = tab1.display_widget(Frame)
inner_frame2 = tab2.display_widget(Frame)
inner_frame3 = tab3.display_widget(Frame)



myNotebook.add(tab0, text ='Αναζήτηση')  
myNotebook.add(tab1, text ='Βιβλίο')
myNotebook.add(tab2, text ='Μέλος')
myNotebook.add(tab3, text ='Αναφορές')
myNotebook.pack(expand = 1, fill ="both")



def publishsearchcriteria():  
    #____________Activates-Deactivates_search_criteria____________
    #______criteria for book search ______________________________
    if Search_choice.get() == 1:
        lblTitle0.config(state='normal')
        e_title0.config(state='normal')

        lblCategory0.config(state='normal')
        e_category0.config(state='normal')

        lblDewey0.config(state='normal')
        e_dewey0.config(state='normal')

        lblMember_code0.config(state='disabled')
        e_member_code0.config(state='disabled')
        
        lblMember_name0.config(state='disabled')
        e_member_name0.config(state='disabled')
       
        lblMember_surname0.config(state='disabled')
        e_member_surname0.config(state='disabled')
        
        lblWriter_surname0.config(state='disabled')
        e_writer_surname0.config(state='disabled')

        C_active_book0.config(state ='normal')
        C_active_member0.config(state='disabled')
    #______criteria for member search ______________________________    
    elif Search_choice.get() == 2:
        lblTitle0.config(state='disabled')
        e_title0.config(state='disabled')
       
        lblCategory0.config(state='disabled')
        e_category0.config(state='disabled')
        
        
        lblDewey0.config(state='disabled')
        e_dewey0.config(state='disabled')
        
        lblMember_code0.config(state='normal')
        e_member_code0.config(state='normal')

        lblMember_name0.config(state='normal')
        e_member_name0.config(state='normal')

        lblMember_surname0.config(state='normal')
        e_member_surname0.config(state='normal')

        lblWriter_surname0.config(state='disabled')
        e_writer_surname0.config(state='disabled')

        C_active_book0.config(state ='disabled')
        C_active_member0.config(state='normal')
    #______criteria for writer search ______________________________   
    else:
        lblTitle0.config(state='disabled')
        e_title0.config(state='disabled')
       
        lblCategory0.config(state='disabled')
        e_category0.config(state='disabled')
        
        lblDewey0.config(state='disabled')
        e_dewey0.config(state='disabled')
     
        lblMember_code0.config(state='disabled')
        e_member_code0.config(state='disabled')
        
        lblMember_name0.config(state='disabled')
        e_member_name0.config(state='disabled')

        lblMember_surname0.config(state='disabled')
        e_member_surname0.config(state='disabled')

        C_active_book0.config(state ='disabled')
        C_active_member0.config(state='disabled')
       
        lblWriter_surname0.config(state='normal')
        e_writer_surname0.config(state='normal')
    

def get_selected_row(event):
    #_________ gets the selected result of the search in the Search Tab__________________
    try:
        global selected_tuple
        index=listSearch.curselection()[0]
        selected_tuple=listSearch.get(index)
    except IndexError:
        pass

#_________________Category selection and edit___________________________
def get_selected_category(event):
    l=list(category_selected.get())
    #print(l) until 99 book categories
    book_categoryID = l[0] + l[1]
    category_selected.set (book_categoryID)
    
   

def open_add_new_category():
    #________ opens new book category window ___________________________
    global newCategoryWindow
    newCategoryWindow = Toplevel(window)
    newCategoryWindow.title("Προσθήκη νέας κατηγορίας βιβλίου")
    newCategoryWindow.geometry("700x400")
  
    lblcat_desc = Label(newCategoryWindow,text = "Περιγραφή κατηγορίας")
    lblcat_desc.grid(row = 1, column = 0, padx=20, pady=10)

    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book_category WHERE id= ? ",(category_selected.get(),))
    the_category= cur.fetchall()
    conn.close()

    global cat_desc_text
    cat_desc_text = StringVar()

    global e_cat_desc
    e_cat_desc= Entry(newCategoryWindow, textvariable= cat_desc_text)
    e_cat_desc.grid(row = 1, column = 1, columnspan =2, padx=20, pady=10)

    e_cat_desc.delete(0, END)
    e_cat_desc.insert(0,the_category[0][1])

    lblcat_abb = Label(newCategoryWindow,text = "Συντομογραφία")
    lblcat_abb.grid(row = 2, column = 0, padx=20, pady=10)
    
    global cat_abb_text
    cat_abb_text = StringVar()

    global e_cat_abb
    e_cat_abb= Entry(newCategoryWindow, textvariable= cat_abb_text)
    e_cat_abb.grid(row = 2, column = 1, columnspan =2, padx=20, pady=10)
    e_cat_abb.delete(0, END)
    e_cat_abb.insert(0,the_category[0][2])

    global b_new_category
    b_new_category=Button(newCategoryWindow, text = "Νέα κατηγορία", width =12, command= clear_category_entries_command )
    b_new_category.grid(row=3, column =0,  padx=20, pady=20)
    
    global b_save_category
    b_save_category=Button(newCategoryWindow, text = "Αποθήκευση", width =12, command= add_new_category_command )
    
    b_update_category=Button(newCategoryWindow, text = "Ενημέρωση", width =12,command=update_category_command) 
    b_update_category.grid(row=3, column =1, padx=20, pady=20)

    b_delete_category=Button(newCategoryWindow, text = "Διαγραφή", width =12,command=delete_category_command) 
    b_delete_category.grid(row=3, column =2, padx=20, pady=20)


#________________Book_category commands__________________________________________

def add_new_category_command():
    Bookarebackend.add_new_category(cat_desc_text.get(), cat_abb_text.get())
    list_category['values']= Bookarebackend.get_book_categories()
    newCategoryWindow.destroy()
    
    
def update_category_command():
    Bookarebackend.update_book_category(cat_desc_text.get(), cat_abb_text.get(),category_selected.get())
    list_category['values']= Bookarebackend.get_book_categories()
    newCategoryWindow.destroy()

def delete_category_command():
    #_check if there is a book linked to the category
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Count(id) FROM Books WHERE Category_id= ? ",(category_selected.get(),))
    cat_to_delete= cur.fetchall()
    conn.close()
    # if there is no book the category is deleted
    if cat_to_delete == 0:
        Bookarebackend.delete_book_category(category_selected.get())
        list_category['values']= Bookarebackend.get_book_categories()
        newCategoryWindow.destroy()
    else:
        messagebox.showwarning("Ουπς κάτι προέκυψε", "Δεν μπορείτε να διαγράψετε κατηγορία βιβλίου στην οποία υπάρχουν καταχωρισμένα βιβλία")
        newCategoryWindow.destroy()

def clear_category_entries_command():
    #___clears the fields for new category input__________________
    e_cat_desc.delete(0, END)
    e_cat_desc.insert(0, "")
    e_cat_abb.delete(0, END)
    e_cat_abb.insert(0, "")
    b_new_category.grid_forget()
    b_save_category.grid(row=3, column =0,  padx=20, pady=20)

#____________________Refresh data on listboxes on book tab___________________________
def listOn_bookRefreshBook():
    listOn_book.delete(0,END)
    today = datetime.now()
    for row in Bookarebackend.listOn_bookRefreshBook(selected_tuple[0]): 
        d1 = datetime.strptime(row[3], "%Y-%m-%d")
        delta = (today - d1).days
        listOn_book.insert("end", row)
        listOn_book.itemconfig("end", fg = "red" if delta > 15 else "green")

def listbooking_historyRefreshBook():
    listBooking_history.delete(0,END)
    for row in  Bookarebackend.listbooking_historyRefreshBook(selected_tuple[0]): 
        listBooking_history.insert(END,row)

def listReservationsRefreshBook():
    listReservations.delete(0,END)
    for row in  Bookarebackend.listReservationsRefreshBook(selected_tuple[0]): 
        listReservations.insert(END,row)

#__________Get selected row from Search______________________________   

def search_get_selected_row(event):
    try:
        global selected_tuple
        index=listSearch.curselection()[0]
        selected_tuple=listSearch.get(index)
        
        
        # _____ fetch book data from DB based on the user selection_____________________
        if Search_choice.get() == 1 or  Search_choice.get() == 3:
            conn = sqlite3.connect("BookareDB.db")
            cur = conn.cursor()
            cur.execute("SELECT Books.* , Book_category.Description FROM Books LEFT JOIN Book_category on Books.Category_id = Book_category.id WHERE Books.id= ? ",(selected_tuple[0],))
            rows = cur.fetchall()
            conn.close()
            e_ISBN.delete(0, END)
            e_ISBN.insert(0,rows[0][1])
            e_dewey.delete(0, END)
            e_dewey.insert(0, rows[0][2])
            e_title.delete(0, END)
            e_title.insert(0, rows[0][3])
            e_writer.delete(0, END)
            e_writer.insert(0, rows[0][6])
            e_desc.delete(0, END)
            e_desc.insert(0, rows[0][5])
            e_publications.delete(0, END)
            e_publications.insert(0, rows[0][7])
            e_year.delete(0, END)
            e_year.insert(0, rows[0][8])
            e_pub_num.delete(0, END)
            e_pub_num.insert(0, rows[0][9])
            e_write_date.delete(0, END)
            e_write_date.insert(0, rows[0][10])
            e_buy_date.delete(0, END)
            e_buy_date.insert(0, rows[0][11])
            e_price.delete(0, END)
            e_price.insert(0, rows[0][12])
            e_pages.delete(0, END)
            e_pages.insert(0, rows[0][13])
            e_self_num.delete(0, END)
            e_self_num.insert(0, rows[0][14])
            e_total_books.delete(0,END)
            e_total_books.insert(0,rows[0][16])
            e_available_books.delete(0,END)
            e_available_books.insert(0,rows[0][17])
            category_selected.set (rows[0][4])
            #_________________list on_book listbox data__________________________
            listOn_bookRefreshBook()
            #_________________list on_booking history listbox data__________________________
            listbooking_historyRefreshBook()
            #_________________list reservations listbox data__________________________
            listReservationsRefreshBook()
            myNotebook.tab(2, state="disabled")
            myNotebook.tab(1,state= 'normal')
            myNotebook.select(tab1)
        else:
            conn = sqlite3.connect("BookareDB.db")
            cur = conn.cursor()
            cur.execute("SELECT *  FROM Member WHERE id= ? ",(selected_tuple[2],))
            rows = cur.fetchall()
            conn.close()
            e_code.delete(0,END)
            e_code.insert(0,rows[0][0])
            e_name.delete(0,END)
            e_name.insert(0,rows[0][1])
            e_surname.delete(0,END)
            e_surname.insert(0,rows[0][2])
            e_birthDate.delete(0,END)
            e_birthDate.insert(0,rows[0][3])
            e_telephone.delete(0,END)
            e_telephone.insert(0,rows[0][4])
            e_mobile.delete(0,END)
            e_mobile.insert(0,rows[0][5])
            e_address.delete(0,END)
            e_address.insert(0,rows[0][6])
            e_city.delete(0,END)
            e_city.insert(0,rows[0][7])
            e_pobox.delete(0,END)
            e_pobox.insert(0,rows[0][8])
            e_email.delete(0,END)
            e_email.insert(0,rows[0][9])
            e_facebook.delete(0,END)
            e_facebook.insert(0,rows[0][10])
            e_insta.delete(0,END)
            e_insta.insert(0,rows[0][11])
            listOn_bookRefreshMember()
            listbooking_historyRefreshMember()
            listReservationsRefreshMember()
            myNotebook.tab(1, state="disabled")
            myNotebook.tab(2,state= 'normal')
            myNotebook.select(tab2)
        
            
    except IndexError:
        pass

#________________Book commands__________________________________________
def update_book_command():
    #_______ Update book data_________________
    if  (check_date(write_date_text.get())==True) and (check_date(buy_date_text.get())==True) :
        Bookarebackend.update_book(ISBN_text.get(), dewey_text.get(), title_text.get(), category_selected.get(), desc_text.get(), writer_text.get(), publications_text.get(),year_text.get(), pub_num_text.get(), write_date_text.get(), buy_date_text.get(), price_text.get(),pages_text.get(),self_num_text.get(), Check_active_book.get(), total_books.get(), available_books.get(),selected_tuple[0])
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Οι αλλαγές αποθηκεύτηκαν")
        b_save_book.grid_forget()
        b_new_book.grid(row=18, column =0,  padx=20, pady=20)
    else:
        messagebox.showinfo("Μήνυμα λάθους", "Το βιβλίο δεν αποθηκεύτηκε")

def delete_book_command():
    #_______ Delete book data_________________
    Delete_answer = messagebox.askquestion("Επιβεβαίωση διαγραφής", "Είστε σίγουροι για τη διαγραφή βιβλίου;")
    if Delete_answer == 'yes':
        Bookarebackend.delete_book(selected_tuple[0])  
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Το βιβλίο δεν διαγράφηκε οριστικά. Απλά απενεργοποιήθηκε! ")


def add_new_book_command():
    #_______ Add new book to DB_________________
    if  (check_date(write_date_text.get())==True) and (check_date(buy_date_text.get())==True) :
        Bookarebackend.add_new_book(ISBN_text.get(), dewey_text.get(), title_text.get(), category_selected.get(), desc_text.get(), writer_text.get(), publications_text.get(),year_text.get(), pub_num_text.get(), write_date_text.get(), buy_date_text.get(), int(price_text.get()),pages_text.get(),self_num_text.get(), Check_active_book.get(), total_books.get(), total_books.get())
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Το βιβλίο αποθηκεύτηκε")
        b_save_book.grid_forget()
        b_new_book.grid(row=18, column =0,  padx=20, pady=20)
        bookchoosen['values'] = Bookarebackend.get_all_books()
    else:
        messagebox.showinfo("Μήνυμα λάθους", "Το βιβλίο δεν αποθηκεύτηκε")


def check_date(date_text):
    #________- checks if date input from user is valid
    pattern = r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])'
    match = re.search(pattern, date_text)
    if match or len(date_text)== 0:
        return True
    else:
        messagebox.showinfo("Μήνυμα λάθους", "Εισάγατε λάθος ημερομηνία. Η ημερομηνία πρέπει να είναι της μορφής 2021-12-24")

#__________________Clear book entries for New book_________________________

def clear_book_entries_command():
      e_ISBN.delete(0, END)
      e_ISBN.insert(0, "")
      e_dewey.delete(0, END)
      e_dewey.insert(0, "")
      e_title.delete(0, END)
      e_title.insert(0, "")
      e_writer.delete(0, END)
      e_writer.insert(0, "")
      e_desc.delete(0, END)
      e_desc.insert(0, "")
      e_publications.delete(0, END)
      e_publications.insert(0, "")
      e_year.delete(0, END)
      e_year.insert(0, 1900)
      e_pub_num.delete(0, END)
      e_pub_num.insert(0, 1)
      e_write_date.delete(0, END)
      e_write_date.insert(0, "")
      e_buy_date.delete(0, END)
      e_buy_date.insert(0, "")
      e_price.delete(0, END)
      e_price.insert(0, 0)
      e_pages.delete(0, END)
      e_pages.insert(0, 0)
      e_self_num.delete(0, END)
      e_self_num.insert(0, "")
      e_total_books.delete(0,END)
      e_total_books.insert(0,"")
      e_available_books.delete(0,END)
      e_available_books.insert(0,"")
      category_selected.set(1)
      listOn_book.delete(0,END)
      listBooking_history.delete(0,END)
      listReservations.delete(0,END)
      b_new_book.grid_forget()
      b_save_book.grid(row=18, column =0,  padx=20, pady=20)

#___________________Search book -book- member -writer _________________________________

def search_book_command():
    listSearch.delete(0,END)
    if Search_choice.get() == 1:
        for row in Bookarebackend.search_book_bybook(title_text0.get(), category_text0.get(), dewey_text0.get(),Check_active_book0.get()): 
            listSearch.insert(END,(row[0],row[3],row[5],row[18],row[1],row[2]))       
    elif Search_choice.get() == 2 :
        for row in Bookarebackend.search_book_bymember(member_code_text0.get(), member_name_text0.get(), member_surname_text0.get(),Check_active_member0.get()):
            listSearch.insert(END,row)
    else:
        for row in Bookarebackend.search_book_bywriter(writer_surname_text0.get()):
            listSearch.insert(END,(row[0],row[6],row[3],row[5],row[18],row[1],row[2]))
  



#_____________________________ new bookings from Book TAB________________________________________________
def save_new_booking():
    
    index=listBooking_search_member.curselection()[0]
    selected_member=listBooking_search_member.get(index)
   
    
    #____________checks if there are any available books to book______________________________
    if int(e_available_books.get()) > 0 :
        avbooks=int(e_available_books.get())-1
        conn = sqlite3.connect("BookareDB.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Bookings (Member_id, Book_id, Start_date, END_Date )VALUES (?,?,?,?)",(selected_member[0],selected_tuple[0],date.today(),None ))
        cur.execute("UPDATE Books SET Available_books=? WHERE id = ? ", (avbooks,selected_tuple[0]))
        conn.commit()
        conn.close()  
        listOn_bookRefreshBook()
        e_available_books.delete(0,END)
        e_available_books.insert(0,avbooks)
        messagebox.showinfo("Νέος Δανεισμός", "Ο δανεισμός του βιβλίου ολοκληρώθηκε. Εμπρόθεσμη ημερομηνία επιστροφής μέχρι: " + str (date.today() + timedelta(days=15)))    
    else:
        messagebox.showwarning("Έλεγχος διαθεσιμότητας","Δεν υπάρχουν διαθέσιμα βιβλία για δανεισμό")
    newBookingWindow.destroy()

def close_new_booking_window():
    newBookingWindow.destroy()

def search_member_in_newbooking():
    #________search_member_in_new booking__________________
    listBooking_search_member.delete(0, END)
    for row in Bookarebackend.search_member_by_surname(booking_member_surname.get()):
        listBooking_search_member.insert(END,row)

def open_add_new_booking():
    #________add_new booking__________________
    global newBookingWindow
    newBookingWindow = Toplevel(window)
    newBookingWindow.title("Δανεισμός βιβλίου")
    newBookingWindow.geometry("500x600")
  
    lblbooking_book_title= Label(newBookingWindow,text = "Τίτλος βιβλίου")
    lblbooking_book_title.grid(row = 1, column = 0, padx=20, pady=10)
    
    booking_book_title= StringVar()
    e_booking_book_title = Entry(newBookingWindow, textvariable= booking_book_title)
    e_booking_book_title.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_writers= Label(newBookingWindow,text = "Συγγραφέας")
    lblbooking_writers.grid(row = 2, column = 0, padx=20, pady=10)
    
    booking_writers= StringVar()
    e_booking_writers = Entry(newBookingWindow, textvariable= booking_writers)
    e_booking_writers.grid(row = 2, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_ISBN= Label(newBookingWindow,text = "ISBN")
    lblbooking_ISBN.grid(row = 3, column = 0, padx=20, pady=10)
    
    booking_ISBN= StringVar()
    e_booking_ISBN= Entry(newBookingWindow, textvariable= booking_ISBN)
    e_booking_ISBN.grid(row = 3, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_search_member= Label(newBookingWindow,text = "Αναζήτηση μέλους",font=(None, 24), fg='orange')
    lblbooking_search_member.grid(row = 4, column = 0, columnspan =2, padx=20, pady=10)

    lblbooking_member_surname= Label(newBookingWindow,text = "Επώνυμο μέλους")
    lblbooking_member_surname.grid(row = 5, column = 0, padx=20, pady=10)

    global booking_member_surname
    booking_member_surname= StringVar()
    e_booking_member_surname = Entry(newBookingWindow, textvariable= booking_member_surname)
    e_booking_member_surname.grid(row = 5, column = 1,columnspan=2, padx=20, pady=10)

    b_search_member=Button(newBookingWindow, text = "Αναζήτηση", width =12, command=search_member_in_newbooking) 
    b_search_member.grid(row=6, column =0, columnspan =2, padx=20, pady=20)

    global listBooking_search_member
    listBooking_search_member = Listbox(newBookingWindow, height=10,width=50, bg='light grey',bd=0)
    listBooking_search_member.grid(row =7, column =0, padx=20, pady=10,columnspan=2,sticky='e')

    sbBooking_search_member = Scrollbar(newBookingWindow)
    sbBooking_search_member.grid(row =7, column = 0,columnspan=2,padx=20, pady=10, sticky='nse')

    listBooking_search_member.configure(yscrollcommand = sbBooking_search_member.set)
    sbBooking_search_member.configure(command=listBooking_search_member.yview)

    b_save_new_booking=Button(newBookingWindow, text = "Ολοκλήρωση", width =12, command = save_new_booking) 
    b_save_new_booking.grid(row=8, column =0, padx=20, pady=20)

    b_cancel_new_booking=Button(newBookingWindow, text = "Ακύρωση", width =12, command=close_new_booking_window) 
    b_cancel_new_booking.grid(row=8, column =1, padx=20, pady=20)

    bookinfo = Bookarebackend.get_basic_book_info(selected_tuple[0])
    e_booking_book_title.delete(0, END)
    e_booking_book_title.insert(0, bookinfo[0][0])

    e_booking_writers.delete(0, END)
    e_booking_writers.insert(0, bookinfo[0][1])

    e_booking_ISBN.delete(0, END)
    e_booking_ISBN.insert(0, bookinfo[0][2])


#_____________New bookings from Member TAB_________________________________________________

def open_add_new_booking_fromMember():
    global newBookingWindowMember
    newBookingWindowMember = Toplevel(window)
    newBookingWindowMember.title("Δανεισμός βιβλίου")
    newBookingWindowMember.geometry("500x600")
  
    lblbooking_member_id= Label(newBookingWindowMember,text = "Κωδικός μέλους")
    lblbooking_member_id.grid(row = 1, column = 0, padx=20, pady=10)
    global booking_member_id
    booking_member_id= StringVar()
    e_booking_member_id = Entry(newBookingWindowMember, textvariable= booking_member_id)
    e_booking_member_id.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_Name= Label(newBookingWindowMember,text = "Όνομα")
    lblbooking_Name.grid(row = 2, column = 0, padx=20, pady=10)
    
    booking_name= StringVar()
    e_booking_name = Entry(newBookingWindowMember, textvariable= booking_name)
    e_booking_name.grid(row = 2, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_surname= Label(newBookingWindowMember,text = "Επώνυμο")
    lblbooking_surname.grid(row = 3, column = 0, padx=20, pady=10)
    
    booking_surname= StringVar()
    e_booking_surname= Entry(newBookingWindowMember, textvariable= booking_surname)
    e_booking_surname.grid(row = 3, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_mobile=  Label(newBookingWindowMember,text = "Κινητό τηλέφωνο")
    lblbooking_mobile.grid(row = 4, column = 0, padx=20, pady=10)
    
    booking_mobile = StringVar()
    e_booking_mobile= Entry(newBookingWindowMember, textvariable= booking_mobile)
    e_booking_mobile.grid(row = 4, column = 1,columnspan=2, padx=20, pady=10)


    lblbooking_search_book= Label(newBookingWindowMember,text = "Αναζήτηση βιβλίου",font=(None, 24), fg='orange')
    lblbooking_search_book.grid(row = 5, column = 0, columnspan =2, padx=20, pady=10)

    lblbooking_book_title= Label(newBookingWindowMember,text = "Τίτλος βιβλίου")
    lblbooking_book_title.grid(row = 6, column = 0, padx=20, pady=10)

    global booking_book_title
    booking_book_title= StringVar()
    e_booking_book_title = Entry(newBookingWindowMember, textvariable= booking_book_title)
    e_booking_book_title.grid(row = 6, column = 1,columnspan=2, padx=20, pady=10)

    b_search_book=Button(newBookingWindowMember, text = "Αναζήτηση", width =12,command = search_book_in_newbooking) 
    b_search_book.grid(row=7, column =0, columnspan =2, padx=20, pady=20)

    global listBooking_search_book
    listBooking_search_book = Listbox(newBookingWindowMember, height=10,width=50, bg='light grey',bd=0)
    listBooking_search_book.grid(row =8, column =0, padx=20, pady=10,columnspan=2,sticky='e')

    sbBooking_search_book = Scrollbar(newBookingWindowMember)
    sbBooking_search_book.grid(row =8, column = 0,columnspan=2,padx=20, pady=10, sticky='nse')

    listBooking_search_book.configure(yscrollcommand = sbBooking_search_book.set)
    sbBooking_search_book.configure(command=listBooking_search_book.yview)

    b_save_new_bookingMember=Button(newBookingWindowMember, text = "Ολοκλήρωση", width =12, command =save_new_bookingFromMember) 
    b_save_new_bookingMember.grid(row=9, column =0, padx=20, pady=20)

    b_cancel_new_bookingMember=Button(newBookingWindowMember, text = "Ακύρωση", width =12, command = close_new_booking_FromMember) 
    b_cancel_new_bookingMember.grid(row=9, column =1, padx=20, pady=20)

    Memberinfo = Bookarebackend.get_basic_member_info(selected_tuple[2])
    e_booking_member_id.delete(0, END)
    e_booking_member_id.insert(0, Memberinfo[0][0])

    e_booking_name.delete(0, END)
    e_booking_name.insert(0, Memberinfo[0][1])

    e_booking_surname.delete(0, END)
    e_booking_surname.insert(0, Memberinfo[0][2])

    e_booking_mobile.delete(0, END)
    e_booking_mobile.insert(0, Memberinfo[0][3])

def search_book_in_newbooking():
    listBooking_search_book.delete(0, END)
    for row in Bookarebackend.search_book_byTitle(booking_book_title.get()):
        listBooking_search_book.insert(END,row)

def save_new_bookingFromMember():
    index=listBooking_search_book.curselection()[0]
    selected_book=listBooking_search_book.get(index)
    
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Available_books FROM Books where id=?",(selected_book[0],))
    avbooks = cur.fetchall()
    conn.close()
    availablebooks= (avbooks[0][0])
    if availablebooks > 0 :
        availablebooks -= 1
        conn = sqlite3.connect("BookareDB.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO Bookings (Member_id, Book_id, Start_date, END_Date )VALUES (?,?,?,?)",(booking_member_id.get(),selected_book[0],date.today(),None ))
        cur.execute("UPDATE Books SET Available_books=? WHERE id = ? ", (availablebooks,selected_book[0]))
        conn.commit()
        conn.close()  
        listOn_bookRefreshMember()
        messagebox.showinfo("Νέος Δανεισμός", "Ο δανεισμός του βιβλίου ολοκληρώθηκε. Εμπρόθεσμη ημερομηνία επιστροφής μέχρι: " + str (date.today() + timedelta(days=15)))    
    else:
        messagebox.showwarning("Έλεγχος διαθεσιμότητας","Δεν υπάρχουν διαθέσιμα βιβλία για δανεισμό")
    newBookingWindowMember.destroy()

def close_new_booking_FromMember():
    newBookingWindowMember.destroy()


#______________________Return book from Member_________________________________________________________

def get_selected_book_lstOnBook_member(event):
    try:
        index=listOn_book_member.curselection()[0]
        global selected_booking
        selected_booking= listOn_book_member.get(index)
        global ReturnBookingWindowMember
        ReturnBookingWindowMember = Toplevel(window)
        ReturnBookingWindowMember.title("Επιστροφή βιβλίου")
        ReturnBookingWindowMember.geometry("500x150")
    
        lblreturn_book_dateMember= Label(ReturnBookingWindowMember,text = "Ημ/νία επιστροφής (ΕΕΕΕ-ΜΜ-ΗΗ)")
        lblreturn_book_dateMember.grid(row = 1, column = 0, padx=20, pady=10)
        
        global return_book_dateMember
        return_book_dateMember= StringVar()
        e_return_book_dateMember = Entry(ReturnBookingWindowMember, textvariable= return_book_dateMember)
        e_return_book_dateMember.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)
        e_return_book_dateMember.delete(0,END)
        e_return_book_dateMember.insert(0,date.today())

        b_ok_return_bookingMember=Button(ReturnBookingWindowMember, text = "Επιστροφή", width =12, command = ok_return_bookingMember) 
        b_ok_return_bookingMember.grid(row=2, column =0, padx=20, pady=20)

        b_cancel_return_bookingMember=Button(ReturnBookingWindowMember, text = "Ακύρωση", width =12,command= close_return_booking_windowMember) 
        b_cancel_return_bookingMember.grid(row=2, column =1, padx=20, pady=20)  
    except IndexError:
        pass  

def ok_return_bookingMember():
    #_______ update DB after book return__________________
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Available_books FROM Books where id=?",(selected_booking[0],))
    avbooks = cur.fetchall()
    conn.close()
    availablebooks= (avbooks[0][0]) + 1
    
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Bookings SET End_date=? WHERE Member_id = ? AND Book_id=? AND Start_date =? ", (return_book_dateMember.get(), selected_tuple[2],selected_booking[0],selected_booking[3]))
    cur.execute("UPDATE Books SET Available_books=? WHERE id=?", (availablebooks,selected_booking[0]))
    conn.commit()
    conn.close()  
    listOn_bookRefreshMember()
    listbooking_historyRefreshMember()
    messagebox.showinfo("Επιστροφή βιβλίου", "Η επιστροφή του βιβλίου ολοκληρώθηκε")
    close_return_booking_windowMember()
    
def close_return_booking_windowMember():
    ReturnBookingWindowMember.destroy()    
#______________________Return book_________________________________________________________

def get_selected_book_lstOnBook(event):
    # ___gets the data for the book is going to be returned_______________
    try:
        index=listOn_book.curselection()[0]
        global selected_booking
        selected_booking= listOn_book.get(index)
        global ReturnBookingWindow
        ReturnBookingWindow = Toplevel(window)
        ReturnBookingWindow.title("Επιστροφή βιβλίου")
        ReturnBookingWindow.geometry("500x150")
    
        lblreturn_book_date= Label(ReturnBookingWindow,text = "Ημ/νία επιστροφής (ΕΕΕΕ-ΜΜ-ΗΗ)")
        lblreturn_book_date.grid(row = 1, column = 0, padx=20, pady=10)
        
        global return_book_date
        return_book_date= StringVar()
        e_return_book_date = Entry(ReturnBookingWindow, textvariable= return_book_date)
        e_return_book_date.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)
        e_return_book_date.delete(0,END)
        e_return_book_date.insert(0,date.today())

        b_ok_return_booking=Button(ReturnBookingWindow, text = "Επιστροφή", width =12, command = ok_return_booking) 
        b_ok_return_booking.grid(row=2, column =0, padx=20, pady=20)

        b_cancel_return_booking=Button(ReturnBookingWindow, text = "Ακύρωση", width =12, command=close_return_booking_window) 
        b_cancel_return_booking.grid(row=2, column =1, padx=20, pady=20)
    except IndexError:
        pass

def ok_return_booking():
    #_____update DB after book return__________
    avbooks=int(e_available_books.get())+1
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Bookings SET End_date=? WHERE Member_id = ? AND Book_id=? AND Start_date =? ", (return_book_date.get(),selected_booking[0],selected_tuple[0],selected_booking[3]))
    cur.execute("UPDATE Books SET Available_books=? WHERE id=?", (avbooks,selected_tuple[0]))
    conn.commit()
    conn.close()  
    #_____update listboxes_____________________
    listOn_bookRefreshBook()
    listbooking_historyRefreshBook()
    e_available_books.delete(0,END)
    e_available_books.insert(0,avbooks)
    messagebox.showinfo("Επιστροφή βιβλίου", "Η επιστροφή του βιβλίου ολοκληρώθηκε")
    close_return_booking_window()
    
   

def close_return_booking_window():
    ReturnBookingWindow.destroy()    

#______________________________Reservations________________________________________________
def close_new_reservation_window():
    newreservationWindow.destroy()

def search_member_in_newreservation():
    listreservation_search_member.delete(0, END)
    for row in Bookarebackend.search_member_by_surname(reservation_member_surname.get()):
        listreservation_search_member.insert(END,row)

def save_new_reservation():
    index=listreservation_search_member.curselection()[0]
    selected_member=listreservation_search_member.get(index)
    Bookarebackend.add_new_reservation(selected_member[0],selected_tuple[0],date.today())
    listReservationsRefreshBook()
    messagebox.showinfo("Νέα Κράτηση", "Η κράτηση του βιβλίου ολοκληρώθηκε")
    close_new_reservation_window()
        
    

def open_add_new_reservation():
    #________ opens add new reservation window_______________________
    global newreservationWindow
    newreservationWindow = Toplevel(window)
    newreservationWindow.title("Κράτηση βιβλίου")
    newreservationWindow.geometry("500x600")
  
    lblreservation_book_title= Label(newreservationWindow,text = "Τίτλος βιβλίου")
    lblreservation_book_title.grid(row = 1, column = 0, padx=20, pady=10)
    
    reservation_book_title= StringVar()
    e_reservation_book_title = Entry(newreservationWindow, textvariable= reservation_book_title)
    e_reservation_book_title.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)

    lblreservation_writers= Label(newreservationWindow,text = "Συγγραφέας")
    lblreservation_writers.grid(row = 2, column = 0, padx=20, pady=10)
    
    reservation_writers= StringVar()
    e_reservation_writers = Entry(newreservationWindow, textvariable= reservation_writers)
    e_reservation_writers.grid(row = 2, column = 1,columnspan=2, padx=20, pady=10)

    lblreservation_ISBN= Label(newreservationWindow,text = "ISBN")
    lblreservation_ISBN.grid(row = 3, column = 0, padx=20, pady=10)
    
    reservation_ISBN= StringVar()
    e_reservation_ISBN= Entry(newreservationWindow, textvariable= reservation_ISBN)
    e_reservation_ISBN.grid(row = 3, column = 1,columnspan=2, padx=20, pady=10)

    lblreservation_search_member= Label(newreservationWindow,text = "Αναζήτηση μέλους",font=(None, 24), fg='orange')
    lblreservation_search_member.grid(row = 4, column = 0, columnspan =2, padx=20, pady=10)

    lblreservation_member_surname= Label(newreservationWindow,text = "Επώνυμο μέλους")
    lblreservation_member_surname.grid(row = 5, column = 0, padx=20, pady=10)

    global reservation_member_surname
    reservation_member_surname= StringVar()
    e_reservation_member_surname = Entry(newreservationWindow, textvariable= reservation_member_surname)
    e_reservation_member_surname.grid(row = 5, column = 1,columnspan=2, padx=20, pady=10)

    b_search_member=Button(newreservationWindow, text = "Αναζήτηση", width =12, command=search_member_in_newreservation) 
    b_search_member.grid(row=6, column =0, columnspan =2, padx=20, pady=20)

    global listreservation_search_member
    listreservation_search_member = Listbox(newreservationWindow, height=10,width=50, bg='light grey',bd=0)
    listreservation_search_member.grid(row =7, column =0, padx=20, pady=10,columnspan=2,sticky='e')

    sbreservation_search_member = Scrollbar(newreservationWindow)
    sbreservation_search_member.grid(row =7, column = 0,columnspan=2,padx=20, pady=10, sticky='nse')

    listreservation_search_member.configure(yscrollcommand = sbreservation_search_member.set)
    sbreservation_search_member.configure(command=listreservation_search_member.yview)

    b_save_new_reservation=Button(newreservationWindow, text = "Ολοκλήρωση", width =12, command = save_new_reservation) 
    b_save_new_reservation.grid(row=8, column =0, padx=20, pady=20)

    b_cancel_new_reservation=Button(newreservationWindow, text = "Ακύρωση", width =12, command=close_new_reservation_window) 
    b_cancel_new_reservation.grid(row=8, column =1, padx=20, pady=20)

    #____ gets basic prefilled data_________________
    reservinfo =Bookarebackend.get_basic_book_info(selected_tuple[0])

    e_reservation_book_title.delete(0, END)
    e_reservation_book_title.insert(0, reservinfo[0][0])

    e_reservation_writers.delete(0, END)
    e_reservation_writers.insert(0, reservinfo[0][1])

    e_reservation_ISBN.delete(0, END)
    e_reservation_ISBN.insert(0, reservinfo[0][2])

#__________________Add  new  reservation from Member TAB ____________________________________________

def open_add_new_reservationFromMember():
    global newReservationWindowMember
    newReservationWindowMember = Toplevel(window)
    newReservationWindowMember.title("Κράτηση βιβλίου")
    newReservationWindowMember.geometry("500x600")
  
    lblbooking_member_id= Label(newReservationWindowMember,text = "Κωδικός μέλους")
    lblbooking_member_id.grid(row = 1, column = 0, padx=20, pady=10)
    
    global booking_member_id
    booking_member_id= StringVar()
    e_booking_member_id = Entry(newReservationWindowMember, textvariable= booking_member_id)
    e_booking_member_id.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_Name= Label(newReservationWindowMember,text = "Όνομα")
    lblbooking_Name.grid(row = 2, column = 0, padx=20, pady=10)
    
    booking_name= StringVar()
    e_booking_name = Entry(newReservationWindowMember, textvariable= booking_name)
    e_booking_name.grid(row = 2, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_surname= Label(newReservationWindowMember,text = "Επώνυμο")
    lblbooking_surname.grid(row = 3, column = 0, padx=20, pady=10)
    
    booking_surname= StringVar()
    e_booking_surname= Entry(newReservationWindowMember, textvariable= booking_surname)
    e_booking_surname.grid(row = 3, column = 1,columnspan=2, padx=20, pady=10)

    lblbooking_mobile=  Label(newReservationWindowMember,text = "Κινητό τηλέφωνο")
    lblbooking_mobile.grid(row = 4, column = 0, padx=20, pady=10)
    
    booking_mobile = StringVar()
    e_booking_mobile= Entry(newReservationWindowMember, textvariable= booking_mobile)
    e_booking_mobile.grid(row = 4, column = 1,columnspan=2, padx=20, pady=10)


    lblbooking_search_book= Label(newReservationWindowMember,text = "Αναζήτηση βιβλίου",font=(None, 24), fg='orange')
    lblbooking_search_book.grid(row = 5, column = 0, columnspan =2, padx=20, pady=10)

    lblbooking_book_title= Label(newReservationWindowMember,text = "Τίτλος βιβλίου")
    lblbooking_book_title.grid(row = 6, column = 0, padx=20, pady=10)

    global booking_book_title
    booking_book_title= StringVar()
    e_booking_book_title = Entry(newReservationWindowMember, textvariable= booking_book_title)
    e_booking_book_title.grid(row = 6, column = 1,columnspan=2, padx=20, pady=10)

    b_search_book=Button(newReservationWindowMember, text = "Αναζήτηση", width =12,command = search_book_in_newbooking) 
    b_search_book.grid(row=7, column =0, columnspan =2, padx=20, pady=20)

    global listBooking_search_book
    listBooking_search_book = Listbox(newReservationWindowMember, height=10,width=50, bg='light grey',bd=0)
    listBooking_search_book.grid(row =8, column =0, padx=20, pady=10,columnspan=2,sticky='e')

    sbBooking_search_book = Scrollbar(newReservationWindowMember)
    sbBooking_search_book.grid(row =8, column = 0,columnspan=2,padx=20, pady=10, sticky='nse')

    listBooking_search_book.configure(yscrollcommand = sbBooking_search_book.set)
    sbBooking_search_book.configure(command=listBooking_search_book.yview)

    b_save_new_bookingMember=Button(newReservationWindowMember, text = "Ολοκλήρωση", width =12, command =save_new_ReservationFromMember) 
    b_save_new_bookingMember.grid(row=9, column =0, padx=20, pady=20)

    b_cancel_new_bookingMember=Button(newReservationWindowMember, text = "Ακύρωση", width =12, command = close_new_Reservation_FromMember) 
    b_cancel_new_bookingMember.grid(row=9, column =1, padx=20, pady=20)

    Memberinfo = Bookarebackend.get_basic_member_info(selected_tuple[2])
    e_booking_member_id.delete(0, END)
    e_booking_member_id.insert(0, Memberinfo[0][0])

    e_booking_name.delete(0, END)
    e_booking_name.insert(0, Memberinfo[0][1])

    e_booking_surname.delete(0, END)
    e_booking_surname.insert(0, Memberinfo[0][2])

    e_booking_mobile.delete(0, END)
    e_booking_mobile.insert(0, Memberinfo[0][3])

def save_new_ReservationFromMember():
    index=listBooking_search_book.curselection()[0]
    selected_book=listBooking_search_book.get(index)
    Bookarebackend.add_new_reservation(selected_tuple[2],selected_book[0],date.today())
    listReservationsRefreshMember()
    messagebox.showinfo("Νέα Κράτηση", "Η κράτηση του βιβλίου ολοκληρώθηκε")
    close_new_Reservation_FromMember()

def close_new_Reservation_FromMember():
    newReservationWindowMember.destroy()  

#_____________________________Delete Reservation from Member TAB _________________________________

def get_selected_rowlstReservationsMember(event):
    try:
        index=listReservations_member.curselection()[0]
        global selected_reservation
        selected_reservation= listReservations_member.get(index)
        global DeleteReservationWindowMember
        DeleteReservationWindowMember = Toplevel(window)
        DeleteReservationWindowMember.title("Διαγραφή κράτησης")
        DeleteReservationWindowMember.geometry("500x150")
    
        lbldelete_reserve_date= Label(DeleteReservationWindowMember,text = "Ημ/νία διαγραφής (ΕΕΕΕ-ΜΜ-ΗΗ)")
        lbldelete_reserve_date.grid(row = 1, column = 0, padx=20, pady=10)
        
        global delete_reserve_date
        delete_reserve_date= StringVar()
        e_delete_reserve_date = Entry(DeleteReservationWindowMember, textvariable= delete_reserve_date)
        e_delete_reserve_date.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)
        e_delete_reserve_date.delete(0,END)
        e_delete_reserve_date.insert(0,date.today())

        b_ok_delete_reservationMember=Button(DeleteReservationWindowMember, text = "Διαγραφή", width =12, command = ok_delete_reservationMember) 
        b_ok_delete_reservationMember.grid(row=2, column =0, padx=20, pady=20)

        b_cancel_delete_reservationMember=Button(DeleteReservationWindowMember, text = "Ακύρωση", width =12, command=close_delete_reservation_windowMember) 
        b_cancel_delete_reservationMember.grid(row=2, column =1, padx=20, pady=20)
    except IndexError:
        pass

def ok_delete_reservationMember():
    Bookarebackend.delete_reservation(selected_tuple[2],selected_reservation[0])
    listReservationsRefreshMember()
    messagebox.showinfo("Κράτηση βιβλίου", "Η κράτηση του βιβλίου διαγράφηκε")
    close_delete_reservation_windowMember()

def close_delete_reservation_windowMember():
    DeleteReservationWindowMember.destroy()

#______________________________Delete Reservation from Book TAB___________________________________________

def get_selected_rowlstReservations(event):
    try:
        index=listReservations.curselection()[0]
        global selected_reservation
        selected_reservation= listReservations.get(index)
        global DeleteReservationWindow
        DeleteReservationWindow = Toplevel(window)
        DeleteReservationWindow.title("Διαγραφή κράτησης")
        DeleteReservationWindow.geometry("500x150")
    
        lbldelete_reserve_date= Label(DeleteReservationWindow,text = "Ημ/νία διαγραφής (ΕΕΕΕ-ΜΜ-ΗΗ)")
        lbldelete_reserve_date.grid(row = 1, column = 0, padx=20, pady=10)
        
        global delete_reserve_date
        delete_reserve_date= StringVar()
        e_delete_reserve_date = Entry(DeleteReservationWindow, textvariable= delete_reserve_date)
        e_delete_reserve_date.grid(row = 1, column = 1,columnspan=2, padx=20, pady=10)
        e_delete_reserve_date.delete(0,END)
        e_delete_reserve_date.insert(0,date.today())

        b_ok_delete_reservation=Button(DeleteReservationWindow, text = "Διαγραφή", width =12, command = ok_delete_reservation) 
        b_ok_delete_reservation.grid(row=2, column =0, padx=20, pady=20)

        b_cancel_delete_reservation=Button(DeleteReservationWindow, text = "Ακύρωση", width =12, command=close_delete_reservation_window) 
        b_cancel_delete_reservation.grid(row=2, column =1, padx=20, pady=20)
    except IndexError:
        pass

def ok_delete_reservation():
    Bookarebackend.delete_reservation(selected_reservation[0],selected_tuple[0])
    listReservationsRefreshBook()
    messagebox.showinfo("Κράτηση βιβλίου", "Η κράτηση του βιβλίου διαγράφηκε")
    close_delete_reservation_window()
    
def close_delete_reservation_window():
    DeleteReservationWindow.destroy()    


#________________________Member Functions__________________________________________________

#_________________clear member entries for new member_____________________
def clear_member_entries_command():
    #____ Clear fields for adding a new member ___________________________
    e_code.delete(0,END)
    e_code.insert(0,"Δίνεται αυτόματα")
    e_name.delete(0,END)
    e_name.insert(0,"")
    e_surname.delete(0,END)
    e_surname.insert(0,"")
    e_birthDate.delete(0,END)
    e_birthDate.insert(0,"")
    e_telephone.delete(0,END)
    e_telephone.insert(0,"")
    e_mobile.delete(0,END)
    e_mobile.insert(0,"")
    e_address.delete(0,END)
    e_address.insert(0,"")
    e_city.delete(0,END)
    e_city.insert(0,"")
    e_pobox.delete(0,END)
    e_pobox.insert(0,"")
    e_email.delete(0,END)
    e_email.insert(0,"")
    e_facebook.delete(0,END)
    e_facebook.insert(0,"")
    e_insta.delete(0,END)
    e_insta.insert(0,"") 
    listOn_book_member.delete(0,END)
    listBooking_history_member.delete(0,END)
    listReservations_member.delete(0,END)      
    
    b_new_member.grid_forget()
    b_save_member.grid(row=16, column =0,  padx=20, pady=20)    

def add_new_member_command():
    if  (check_date(birthDate_text.get())==True) : 
        Bookarebackend.add_new_member(name_text.get(), surname_text.get(), birthDate_text.get(), telephone_text.get(), mobile_text.get(), address_text.get(), city_text.get(), pobox_text.get(), email_text.get(), facebook_text.get(), insta_text.get(), Check_active_member.get())
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Το νέο μέλος αποθηκεύτηκε")
        listOn_bookRefreshMember()
        listbooking_historyRefreshMember()
        listReservationsRefreshMember()
        memberchoosen['values'] = ' '
        memberchoosen['values'] = Bookarebackend.get_all_members()
        b_save_member.grid_forget()
        b_new_member.grid(row=16, column =0,  padx=20, pady=20)
    else:
        messagebox.showinfo("Μήνυμα λάθους", "Το βιβλίο δεν αποθηκεύτηκε")


def update_member_command():
    if  (check_date(birthDate_text.get())==True) : 
        Bookarebackend.update_member(name_text.get(), surname_text.get(), birthDate_text.get(), telephone_text.get(), mobile_text.get(), address_text.get(), city_text.get(), pobox_text.get(), email_text.get(), facebook_text.get(), insta_text.get(), Check_active_member.get(),selected_tuple[2])
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Οι αλλαγές αποθηκεύτηκαν")
        b_save_member.grid_forget()
        b_new_member.grid(row=16, column =0,  padx=20, pady=20)
    else:
        messagebox.showinfo("Μήνυμα λάθους", "Το βιβλίο δεν αποθηκεύτηκε")

def delete_member_command():
    Delete_answer = messagebox.askquestion("Επιβεβαίωση διαγραφής", "Είστε σίγουροι για τη διαγραφή του μέλους;")
    if Delete_answer == 'yes':
        Bookarebackend.delete_member(selected_tuple[2])  
        messagebox.showinfo("Μήνυμα επιβεβαίωσης", "Το μέλος δεν διαγράφηκε οριστικά. Απλά απενεργοποιήθηκε! ")


def listOn_bookRefreshMember():
    listOn_book_member.delete(0,END)
    today = datetime.now()
    for row in Bookarebackend.listOn_bookRefreshMember(selected_tuple[2]): 
        d1 = datetime.strptime(row[3], "%Y-%m-%d")
        delta = (today - d1).days
        listOn_book_member.insert("end",row)
        listOn_book_member.itemconfig("end", fg = "red" if delta > 15 else "green")


   

def listbooking_historyRefreshMember():
    listBooking_history_member.delete(0,END)
    for row in  Bookarebackend.listbooking_historyRefreshMember(selected_tuple[2]): 
        listBooking_history_member.insert(END,row)

def listReservationsRefreshMember():
    listReservations_member.delete(0,END)
    for row in  Bookarebackend.listReservationsRefreshMember(selected_tuple[2]): 
        listReservations_member.insert(END,row)    

#_______________________________Report Functions___________________________________________

def Report_get_selected_book(event):
    res= bookchoosen.get()
    l=list(res.split(" "))
    global bookid_selected
    global bookCredentials_selected
    bookid_selected = l[0]
    bookCredentials_selected = res
    
    


def Report_get_selected_member(event):
    Bookarebackend.get_all_members()
    res= memberchoosen.get()
    l=list(res.split(" "))
    global memberid_selected
    global memberCredentials_selected
    memberid_selected = l[0]
    memberCredentials_selected = l
   
    
    
def getSelectedReport(event):
    global r
    r=reportchoosen.get()
    if r == 'Μέλη βιβλιοθήκης':
        memberchoosen.grid_forget() 
        bookchoosen.grid_forget()
        lblBook_report.grid_forget()  
        lblMember_report.grid_forget() 
    elif r == 'Βιβλία':
        memberchoosen.grid_forget() 
        bookchoosen.grid_forget() 
        lblBook_report.grid_forget() 
        lblMember_report.grid_forget()   
    elif r == 'Ιστορικό δανεισμού βιβλίου':
        memberchoosen.grid_forget() 
        bookchoosen.grid(column=1 ,row= 7 ) 
        lblBook_report.grid(column=0,row= 7)  
        lblMember_report.grid_forget() 
    elif r == 'Ιστορικό δανεισμού μέλους':
        memberchoosen.grid(column = 1, row = 7) 
        bookchoosen.grid_forget()
        lblBook_report.grid_forget() 
        lblMember_report.grid(column = 0, row = 7) 
    elif r == 'Μέλη με ληξιπρόθεσμους δανεισμούς βιβλίων':
        memberchoosen.grid_forget()
        bookchoosen.grid_forget()
        lblBook_report.grid_forget() 
        lblMember_report.grid_forget() 
        
    


def generateReport():
    if reportchoosen.get() == 'Μέλη βιβλιοθήκης':
        Reports.reportAllMembers()
    elif reportchoosen.get() == 'Βιβλία':
        Reports.reportAllBooks()
    elif reportchoosen.get() == 'Ιστορικό δανεισμού βιβλίου':
        Reports.reportBookHistory(bookid_selected,bookCredentials_selected)
    elif reportchoosen.get() == 'Ιστορικό δανεισμού μέλους':
        Reports.reportMemberHistory(memberid_selected,memberCredentials_selected)
    elif reportchoosen.get() == 'Μέλη με ληξιπρόθεσμους δανεισμούς βιβλίων':
        Reports.reportBooksNotReturned()

#_______________________________SEARCH TAB_________________________________________________
left_frame_search=Frame(inner_frame0)
left_frame_search.grid(row=0, column=0,sticky="nesw")


lblSearch_criteria = Label(left_frame_search, text = "Κριτήριο αναζήτησης", font=(None, 24), fg='orange' )
lblSearch_criteria.grid(row = 0, column = 0,columnspan = 3, padx=20, pady=20)

#__________________Radio buttons for search criteria_________________________
Search_choice = IntVar()
R_book = Radiobutton(left_frame_search, text="Βιβλίο" , variable=Search_choice, value=1,command=publishsearchcriteria)
R_book.grid(row = 1, column = 0, padx=20, pady=10)

R_member = Radiobutton(left_frame_search, text="Μέλος", variable=Search_choice, value=2,command=publishsearchcriteria)
R_member.grid(row = 1, column = 1, padx=20, pady=10)

R_writer = Radiobutton(left_frame_search, text="Συγγραφέας", variable=Search_choice, value=3, command=publishsearchcriteria)
R_writer.grid(row = 1, column = 2, padx=20, pady=10)



#_________________Search Criteria____________________________________________________
lblSearch_parameters = Label(left_frame_search, text = "Παράμετροι αναζήτησης", font=(None, 16) )
lblSearch_parameters.grid(row = 2, column = 0,columnspan = 3, padx=20, pady=20)

lblTitle0 = Label(left_frame_search,text = "Τίτλος βιβλίου",state='disabled')
lblTitle0.grid(row = 3, column = 0, padx=20, pady=10)

title_text0 = StringVar()
e_title0 = Entry(left_frame_search, textvariable= title_text0,state='disabled')
e_title0.grid(row =3 , column = 1, columnspan =2, padx=20, pady=10)

lblCategory0 = Label(left_frame_search,text = "Είδος βιβλίου",state='disabled')
lblCategory0.grid(row = 4, column = 0, padx=20, pady=10)

category_text0 = StringVar()
e_category0 = Entry(left_frame_search, textvariable= category_text0,state='disabled')
e_category0.grid(row = 4, column = 1, columnspan =2, padx=20, pady=10)

lblDewey0 = Label(left_frame_search,text = "Αριθμός DEWEY",state='disabled')
lblDewey0.grid(row = 5, column = 0, padx=20, pady=10)

dewey_text0 = StringVar()
e_dewey0 = Entry(left_frame_search, textvariable= dewey_text0,state='disabled')
e_dewey0.grid(row = 5, column = 1, columnspan =2, padx=20, pady=10)


Check_active_book0= IntVar(value=1)
C_active_book0 = Checkbutton(left_frame_search, text = "Ενεργό βιβλίο", variable = Check_active_book0, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C_active_book0.grid(row = 6, column = 0, columnspan =2)


lblMember_code0 = Label(left_frame_search,text = "Κωδικός μέλους",state='disabled')
lblMember_code0.grid(row = 7, column = 0, padx=20, pady=10)

member_code_text0 = StringVar()
e_member_code0 = Entry(left_frame_search, textvariable= member_code_text0,state='disabled')
e_member_code0.grid(row = 7, column = 1, columnspan =2, padx=20, pady=10)

lblMember_name0 = Label(left_frame_search,text = "Όνομα μέλους",state='disabled')
lblMember_name0.grid(row = 8, column = 0, padx=20, pady=10)

member_name_text0 = StringVar()
e_member_name0 = Entry(left_frame_search, textvariable= member_name_text0,state='disabled')
e_member_name0.grid(row = 8, column = 1, columnspan =2, padx=20, pady=10)

lblMember_surname0 = Label(left_frame_search,text = "Επώνυμο μέλους",state='disabled')
lblMember_surname0.grid(row = 9, column = 0, padx=20, pady=10)

member_surname_text0 = StringVar()
e_member_surname0 = Entry(left_frame_search, textvariable= member_surname_text0,state='disabled')
e_member_surname0.grid(row = 9, column = 1, columnspan =2, padx=20, pady=10)

Check_active_member0= IntVar(value=1)
C_active_member0 = Checkbutton(left_frame_search, text = "Ενεργό μέλος", variable = Check_active_member0, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C_active_member0.grid(row = 10, column = 0, columnspan =2)

lblWriter_surname0 = Label(left_frame_search,text = "Επώνυμο συγγραφέα",state='disabled')
lblWriter_surname0.grid(row = 11, column = 0, padx=20, pady=10)

writer_surname_text0 = StringVar()
e_writer_surname0 = Entry(left_frame_search, textvariable= writer_surname_text0,state='disabled')
e_writer_surname0.grid(row = 11, column = 1, columnspan =2, padx=20, pady=10)



right_frame_search=Frame(inner_frame0)
right_frame_search.grid(row=0, column=1,sticky="nesw")

lblSearch_results = Label(right_frame_search,text = "Επιλέξτε αποτέλεσμα αναζήτησης")
lblSearch_results.grid(row =0, column = 3, padx=20, pady=10,columnspan =3)

listSearch = Listbox(right_frame_search, height=30,width=70, bg='light grey',bd=0)
listSearch.grid(row =1, column = 3,rowspan =12, columnspan =3, sticky='e')

sbSearch = Scrollbar(right_frame_search)
sbSearch.grid(row =1, column = 3,rowspan =12, columnspan =3,sticky='nse')

listSearch.configure(yscrollcommand = sbSearch.set)
sbSearch.configure(command=listSearch.yview)

listSearch.bind('<<ListboxSelect>>', search_get_selected_row)

b_search=Button(right_frame_search, text = "Αναζήτηση", width =12, command = search_book_command)
b_search.grid(row=20, column =3, rowspan=25, columnspan =3, padx=20, pady=10)



#_______________________________SEARCH TAB_________________________________________________

     

#_______________________________BOOK TAB___________________________________________________
left_frame_book=Frame(inner_frame1)
left_frame_book.grid(row=0, column=0,sticky="nsew")


# add book info labels___________________________________________________
lblBookinfo = Label(left_frame_book,text = "Στοιχεία βιβλίου", font=(None, 24),fg='orange' )
lblBookinfo.grid(row = 0, column = 0,columnspan = 3, padx=20, pady=20)

lblISBN = Label(left_frame_book,text = "ISBN")
lblISBN.grid(row = 1, column = 0, padx=20, pady=10)

ISBN_text = StringVar()
e_ISBN = Entry(left_frame_book, textvariable= ISBN_text)
e_ISBN.grid(row = 1, column = 1, columnspan =2, padx=20, pady=10)

lblDewey = Label(left_frame_book,text = "Αριθμός DEWEY")
lblDewey.grid(row = 2, column = 0, padx=20, pady=10)

dewey_text = StringVar()
e_dewey = Entry(left_frame_book, textvariable= dewey_text)
e_dewey.grid(row = 2, column = 1, columnspan =2, padx=20, pady=10)

lblTitle = Label(left_frame_book,text = "Τίτλος βιβλίου *")
lblTitle.grid(row = 3, column = 0, padx=20, pady=10)

title_text = StringVar()
e_title = Entry(left_frame_book, textvariable= title_text)
e_title.grid(row =3 , column = 1, columnspan =2, padx=20, pady=10)

lblWriter= Label(left_frame_book,text = "Συγγραφέας *")
lblWriter.grid(row = 4, column = 0, padx=20, pady=10)

writer_text = StringVar()
e_writer = Entry(left_frame_book, textvariable= writer_text)
e_writer.grid(row =4 , column = 1, columnspan =2, padx=20, pady=10)

lblCategory = Label(left_frame_book,text = "Κατηγορία βιβλίου * ")
lblCategory.grid(row = 5, column = 0, padx=20, pady=10)

category_selected = StringVar()
list_category = ttk.Combobox(left_frame_book, width=20, height=20, textvariable = category_selected, state='readonly')
list_category['values']= Bookarebackend.get_book_categories()
list_category.grid(row = 5, column = 1, padx=20, pady=10)

list_category.bind('<<ComboboxSelected>>', get_selected_category)

b_new_category=Button(left_frame_book, text = "Επεξεργασία", width =10, command= open_add_new_category )
b_new_category.grid(row=5, column =2,  padx=20, pady=10)

lblDesc = Label(left_frame_book,text = "Περιγραφή βιβλίου")
lblDesc.grid(row = 6, column = 0, padx=20, pady=10)

desc_text = StringVar()
e_desc = Entry(left_frame_book, textvariable= desc_text)
e_desc.grid(row = 6, column = 1, columnspan =2, padx=20, pady=10)

lblPublications = Label(left_frame_book,text = "Εκδοτικός οίκος")
lblPublications.grid(row = 7, column = 0, padx=20, pady=10)

publications_text = StringVar()
e_publications = Entry(left_frame_book, textvariable= publications_text)
e_publications.grid(row = 7, column = 1, columnspan =2, padx=20, pady=10)

lblYear = Label(left_frame_book,text = "Έτος έκδοσης")
lblYear.grid(row = 8, column = 0, padx=20, pady=10)

year_text = IntVar()
e_year = Entry(left_frame_book, textvariable= year_text)
e_year.grid(row =8 , column = 1, columnspan =2, padx=20, pady=10)

lblPubNum = Label(left_frame_book,text = "Νούμερο έκδοσης")
lblPubNum.grid(row = 9, column = 0, padx=20, pady=10)

pub_num_text = IntVar()
e_pub_num = Entry(left_frame_book, textvariable= pub_num_text)
e_pub_num.grid(row = 9, column = 1, columnspan =2, padx=20, pady=10)

lblWriteDate = Label(left_frame_book,text = "Ημ/νία συγγραφής (ΕΕΕΕ-ΜΜ-ΗΗ)")
lblWriteDate.grid(row = 10, column = 0, padx=20, pady=10)

write_date_text = StringVar()
e_write_date = Entry(left_frame_book, textvariable= write_date_text)
e_write_date.grid(row = 10, column = 1, columnspan =2, padx=20, pady=10)

lblBuyDate = Label(left_frame_book,text = "Ημ/νία αγοράς (ΕΕΕΕ-ΜΜ-ΗΗ)")
lblBuyDate.grid(row = 11, column = 0, padx=20, pady=10)

buy_date_text = StringVar()
e_buy_date = Entry(left_frame_book, textvariable= buy_date_text)
e_buy_date.grid(row = 11, column = 1, columnspan =2, padx=20, pady=10)

lblPrice = Label(left_frame_book,text = "Τιμή αγοράς")
lblPrice.grid(row = 12, column = 0, padx=20, pady=10)

price_text = StringVar()
e_price = Entry(left_frame_book, textvariable= price_text)
e_price.grid(row = 12, column = 1, columnspan =2, padx=20, pady=10)

lblPages = Label(left_frame_book,text = "Σελίδες βιβλίου")
lblPages.grid(row = 13, column = 0, padx=20, pady=10)

pages_text = IntVar()
e_pages = Entry(left_frame_book, textvariable= pages_text)
e_pages.grid(row = 13, column = 1, columnspan =2, padx=20, pady=10)

lblSelfNum = Label(left_frame_book,text = "Τοποθέτηση ραφιού")
lblSelfNum.grid(row = 14, column = 0, padx=20, pady=10)

self_num_text = StringVar()
e_self_num = Entry(left_frame_book, textvariable= self_num_text)
e_self_num.grid(row = 14, column = 1, columnspan =2, padx=20, pady=10)


lbltotal_books = Label(left_frame_book,text = "Συνολικά αντίτυπα" )
lbltotal_books .grid(row = 15, column = 0, padx=20, pady=10)

total_books = StringVar()
e_total_books = Entry(left_frame_book, textvariable= total_books)
e_total_books.grid(row = 15, column = 1, columnspan=2, padx=20, pady=10)


Check_active_book= IntVar(value=1)
C_active_book = Checkbutton(left_frame_book, text = "Ενεργό βιβλίο", variable = Check_active_book, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C_active_book.grid(row = 16, column = 0, columnspan =2)

# add book info buttons save, update, delete_____________________________________________

b_new_book=Button(left_frame_book, text = "Νέο βιβλίο", width =12, command= clear_book_entries_command )
b_new_book.grid(row=18, column =0,  padx=20, pady=20)

b_save_book=Button(left_frame_book, text = "Αποθήκευση", width =12, command= add_new_book_command )
#b_save_book.grid(row=16, column =0,  padx=20, pady=20)

b_update_book=Button(left_frame_book, text = "Ενημέρωση", width =12,command=update_book_command) 
b_update_book.grid(row=18, column =1, padx=20, pady=20)

b_delete_book=Button(left_frame_book, text = "Διαγραφή", width =12,command=delete_book_command) 
b_delete_book.grid(row=18, column =2, padx=20, pady=20)

#_____________________RightPanel_Book______________________________________________
right_frame_book=Frame(inner_frame1)
right_frame_book.grid(row=0, column=1,sticky="nsew")

lblAvailablity = Label(right_frame_book,text = "Διαθεσιμότητα", font=(None, 20),fg='orange' )
lblAvailablity.grid(row = 0, column = 3,padx=20, pady=20)

lblavailable_books = Label(right_frame_book,text = "Διαθέσιμα αντίτυπα")
lblavailable_books .grid(row = 1, column = 3, padx=20, pady=10)

available_books = StringVar()
e_available_books = Entry(right_frame_book, textvariable= available_books)
e_available_books.grid(row = 1, column = 4,columnspan=2, padx=20, pady=10)


lblOn_book = Label(right_frame_book,text = "Βιβλία σε δανεισμό", font=(None, 20),fg='orange' )
lblOn_book.grid(row = 3, column = 3, padx=20, pady=10)

listOn_book = Listbox(right_frame_book, height=10,width=50, bg='light grey',bd=0)
listOn_book.grid(row =4, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbOn_book = Scrollbar(right_frame_book)
sbOn_book.grid(row =4, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listOn_book.configure(yscrollcommand = sbOn_book.set)
sbOn_book.configure(command=listOn_book.yview)

listOn_book.bind('<<ListboxSelect>>', get_selected_book_lstOnBook)

lblBooking_history = Label(right_frame_book,text = "Ιστορικό δανεισμού", font=(None, 20),fg='orange' )
lblBooking_history.grid(row = 5, column = 3, padx=20, pady=10)

b_new_booking = Button(right_frame_book, text = "Νέος δανεισμός", width =12, command= open_add_new_booking) 
b_new_booking.grid(row=5, column =4, padx=20, pady=20)

listBooking_history = Listbox(right_frame_book, height=10,width=50, bg='light grey',bd=0)
listBooking_history.grid(row =6, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbBooking_history = Scrollbar(right_frame_book)
sbBooking_history.grid(row =6, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listBooking_history.configure(yscrollcommand = sbBooking_history.set)
sbBooking_history.configure(command=listBooking_history.yview)

#listBooking_history.bind('<<ListboxSelect>>', get_selected_row)

lblReservations = Label(right_frame_book,text = "Κρατήσεις βιβλίου", font=(None, 20),fg='orange' )
lblReservations.grid(row =7, column = 3, padx=20, pady=10)

b_new_reservation = Button(right_frame_book, text = "Νέα κράτηση", width =12, command= open_add_new_reservation) 
b_new_reservation.grid(row=7, column =4, padx=20, pady=20)

listReservations = Listbox(right_frame_book, height=10,width=50, bg='light grey',bd=0)
listReservations.grid(row =8, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbReservations = Scrollbar(right_frame_book)
sbReservations.grid(row =8, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listReservations.configure(yscrollcommand = sbReservations.set)
sbReservations.configure(command=listReservations.yview)

listReservations.bind('<<ListboxSelect>>', get_selected_rowlstReservations)





#_______________________________BOOK TAB___________________________________________________


#________________________________MEMBER TAB________________________________________________

left_frame_member=Frame(inner_frame2)
left_frame_member.grid(row=0, column=0,sticky="nsew")

# add member info labels___________________________________________________
lblMemberinfo = Label(left_frame_member,text = "Στοιχεία μέλους", font=(None, 24),fg='orange' )
lblMemberinfo.grid(row = 0, column = 0,columnspan = 3, padx=20, pady=20)

lblCode = Label(left_frame_member,text = "Κωδικός μέλους")
lblCode.grid(row = 1, column = 0, padx=20, pady=10)

code_text = StringVar()
e_code = Entry(left_frame_member, textvariable= code_text)
e_code.grid(row =1 , column = 1, columnspan =2, padx=20, pady=10)

lblName = Label(left_frame_member,text = "Όνομα")
lblName.grid(row = 2, column = 0, padx=20, pady=10)

name_text = StringVar()
e_name = Entry(left_frame_member, textvariable= name_text)
e_name.grid(row = 2, column = 1, columnspan =2, padx=20, pady=10)

lblSurname = Label(left_frame_member,text = "Επώνυμο")
lblSurname.grid(row = 3, column = 0, padx=20, pady=10)

surname_text = StringVar()
e_surname = Entry(left_frame_member, textvariable= surname_text)
e_surname.grid(row = 3, column = 1, columnspan =2, padx=20, pady=10)

lblBirthDate= Label(left_frame_member,text = "Ημ/νία γέννησης (ΕΕΕΕ-ΜΜ-ΗΗ)")
lblBirthDate.grid(row = 4, column = 0, padx=20, pady=10)

birthDate_text = StringVar()
e_birthDate = Entry(left_frame_member, textvariable= birthDate_text)
e_birthDate.grid(row =4 , column = 1, columnspan =2, padx=20, pady=10)

lblTelephone = Label(left_frame_member,text = "Σταθερό τηλέφωνο")
lblTelephone.grid(row = 5, column = 0, padx=20, pady=10)

telephone_text = StringVar()
e_telephone = Entry(left_frame_member, textvariable= telephone_text)
e_telephone.grid(row = 5, column = 1, columnspan =2, padx=20, pady=10)

lblMobile = Label(left_frame_member,text = "Κινητό τηλέφωνο")
lblMobile.grid(row = 6, column = 0, padx=20, pady=10)

mobile_text = StringVar()
e_mobile = Entry(left_frame_member, textvariable= mobile_text)
e_mobile.grid(row = 6, column = 1, columnspan =2, padx=20, pady=10)

lblAddress = Label(left_frame_member,text = "Διεύθυνση")
lblAddress.grid(row = 7, column = 0, padx=20, pady=10)

address_text = StringVar()
e_address = Entry(left_frame_member, textvariable= address_text)
e_address.grid(row = 7, column = 1, columnspan =2, padx=20, pady=10)

lblCity= Label(left_frame_member,text = "Πόλη")
lblCity.grid(row = 8, column = 0, padx=20, pady=10)

city_text = StringVar()
e_city = Entry(left_frame_member, textvariable= city_text)
e_city.grid(row =8 , column = 1, columnspan =2, padx=20, pady=10)

lblPobox= Label(left_frame_member,text = "Ταχυδρομικός κώδικας")
lblPobox.grid(row = 9, column = 0, padx=20, pady=10)

pobox_text = StringVar()
e_pobox = Entry(left_frame_member, textvariable= pobox_text)
e_pobox.grid(row = 9, column = 1, columnspan =2, padx=20, pady=10)

lblEmail= Label(left_frame_member,text = "E-mail")
lblEmail.grid(row = 10, column = 0, padx=20, pady=10)

email_text = StringVar()
e_email = Entry(left_frame_member, textvariable= email_text)
e_email.grid(row = 10, column = 1, columnspan =2, padx=20, pady=10)

lblFacebook = Label(left_frame_member,text = "Facebook")
lblFacebook.grid(row = 11, column = 0, padx=20, pady=10)

facebook_text = StringVar()
e_facebook = Entry(left_frame_member, textvariable= facebook_text)
e_facebook.grid(row = 11, column = 1, columnspan =2, padx=20, pady=10)

lblInsta = Label(left_frame_member,text = "Instagram")
lblInsta.grid(row = 12, column = 0, padx=20, pady=10)

insta_text = StringVar()
e_insta = Entry(left_frame_member, textvariable= insta_text)
e_insta.grid(row = 12, column = 1, columnspan =2, padx=20, pady=10)

Check_active_member= IntVar(value=1)
C_active_member = Checkbutton(left_frame_member, text = "Ενεργό μέλος", variable = Check_active_member, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20)
C_active_member.grid(row = 15, column = 0, columnspan =2)

# __________________-add member info buttons save, update, delete_____________________________________________

b_save_member=Button(left_frame_member, text = "Αποθήκευση", width =12 , command = add_new_member_command)
#b_save_member.grid(row=16, column =0,  padx=20, pady=20)

b_new_member=Button(left_frame_member, text = "Νέο μέλος", width =12 , command = clear_member_entries_command)
b_new_member.grid(row=16, column =0,  padx=20, pady=20)

b_update_member=Button(left_frame_member, text = "Ενημέρωση", width =12, command = update_member_command) 
b_update_member.grid(row=16, column =1, padx=20, pady=20)

b_delete_member=Button(left_frame_member, text = "Διαγραφή", width =12,command = delete_member_command) 
b_delete_member.grid(row=16, column =2, padx=20, pady=20)


#___________________Right panel Member___________________________________________________

right_frame_member=Frame(inner_frame2)
right_frame_member.grid(row=0, column=1,sticky="nsew")

lblOn_book_member = Label(right_frame_member,text = "Βιβλία σε δανεισμό", font=(None, 20),fg='orange' )
lblOn_book_member.grid(row = 3, column = 3, padx=20, pady=10)

listOn_book_member = Listbox(right_frame_member, height=10,width=50, bg='light grey',bd=0)
listOn_book_member.grid(row =4, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbOn_book_member = Scrollbar(right_frame_member)
sbOn_book_member.grid(row =4, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listOn_book_member.configure(yscrollcommand = sbOn_book.set)
sbOn_book_member.configure(command=listOn_book.yview)

listOn_book_member.bind('<<ListboxSelect>>', get_selected_book_lstOnBook_member)

lblBooking_history_member = Label(right_frame_member,text = "Ιστορικό δανεισμού", font=(None, 20),fg='orange' )
lblBooking_history_member.grid(row = 5, column = 3, padx=20, pady=10)

b_new_booking_member = Button(right_frame_member, text = "Νέος δανεισμός", width =12, command = open_add_new_booking_fromMember) 
b_new_booking_member.grid(row=5, column =4, padx=20, pady=20)

listBooking_history_member = Listbox(right_frame_member, height=10,width=50, bg='light grey',bd=0)
listBooking_history_member.grid(row =6, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbBooking_history_member = Scrollbar(right_frame_member)
sbBooking_history_member.grid(row =6, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listBooking_history_member.configure(yscrollcommand = sbBooking_history.set)
sbBooking_history_member.configure(command=listBooking_history.yview)

#listBooking_history_member.bind('<<ListboxSelect>>', get_selected_row)

lblReservations_member = Label(right_frame_member,text = "Κρατήσεις βιβλίου", font=(None, 20),fg='orange' )
lblReservations_member.grid(row =7, column = 3, padx=20, pady=10)

b_new_reservation_member = Button(right_frame_member, text = "Νέα κράτηση", width =12, command = open_add_new_reservationFromMember) 
b_new_reservation_member.grid(row=7, column =4, padx=20, pady=20)

listReservations_member = Listbox(right_frame_member, height=10,width=50, bg='light grey',bd=0)
listReservations_member.grid(row =8, column = 3, padx=20, pady=10,columnspan=3,sticky='e')

sbReservations_member = Scrollbar(right_frame_member)
sbReservations_member.grid(row =8, column = 3,columnspan=3,padx=20, pady=10, sticky='nse')

listReservations_member.configure(yscrollcommand = sbReservations.set)
sbReservations_member.configure(command=listReservations.yview)

listReservations_member.bind('<<ListboxSelect>>', get_selected_rowlstReservationsMember)


#________________________________MEMBER TAB________________________________________________

#____________________________Report TAB____________________________________________________

Report_frame=Frame(inner_frame3)
Report_frame.grid(row=0, column=0,sticky="nesw")

# label
lblReports = Label(inner_frame3 ,text = "Επιλέξτε αναφορά", font=(None, 20),fg='orange' )
lblReports.grid(column = 0,row = 5, padx = 10, pady = 25)          
          

# Combobox creation
report = StringVar()
reportchoosen = ttk.Combobox(inner_frame3, width = 30, textvariable = report, state = 'readonly')
  
# Adding combobox drop down list
reportchoosen['values'] = ('Μέλη βιβλιοθήκης', 
                          'Βιβλία',
                          'Ιστορικό δανεισμού βιβλίου',
                          'Ιστορικό δανεισμού μέλους',
                          'Μέλη με ληξιπρόθεσμους δανεισμούς βιβλίων',
                          )
  
reportchoosen.grid(column = 1, row = 5)
reportchoosen.bind('<<ComboboxSelected>>', getSelectedReport)


#_____________All members Combobox_________________________________________________________

lblMember_report= Label(inner_frame3,text = "Επιλέξτε Mέλος")
member = StringVar()
memberchoosen = ttk.Combobox(inner_frame3, width = 35, textvariable = member,state = 'readonly')

# Adding combobox drop down list
memberchoosen['values'] = Bookarebackend.get_all_members()
memberchoosen.bind('<<ComboboxSelected>>', Report_get_selected_member)


#_____________All books Combobox_________________________________________________________

lblBook_report= Label(inner_frame3,text = "Επιλέξτε βιβλίο")
book = StringVar()
bookchoosen = ttk.Combobox(inner_frame3, width = 40, textvariable = book,state = 'readonly')
 
# Adding combobox drop down list
bookchoosen['values'] = Bookarebackend.get_all_books()
bookchoosen.bind('<<ComboboxSelected>>', Report_get_selected_book)

b_generate_report = Button(inner_frame3, text = "Δημιουργία αναφοράς", width =20, command = generateReport) 
b_generate_report.grid(row=8, column =0, padx=20, pady=20)



window.mainloop()
