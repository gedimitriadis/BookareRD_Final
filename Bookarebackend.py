import sqlite3

# _______________ Bookarebackend.py creates the backend functions of the applicatio, mostly database transactions____________________________________-

def connect():
    # create and connect to SQlite database. 
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Book_category (id INTEGER NOT NULL,Description TEXT(100),Abbreviation VARCHAR(25),PRIMARY KEY (id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Bookings (Member_id INTEGER, Book_id INTEGER, Start_date TEXT(25), End_date TEXT(25), Booking_id INTEGER NOT NULL, PRIMARY KEY (Booking_id) FOREIGN KEY (Member_id) REFERENCES Member(id), FOREIGN KEY (Book_id) REFERENCES Books(id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Books (id INTEGER NOT NULL, ISBN VARCHAR(25), Dewey_number VARCHAR(25),Title TEXT(200),Category_id INTEGER,Description TEXT(500),Writer TEXT(200), Publications TEXT(200),Year INTEGER,Publication_number INTEGER,Write_date TEXT(25),Buy_date TEXT(25),Price REAL, Pages INTEGER, Shelf_code VARCHAR(25),Active INTEGER,Total_books INTEGER DEFAULT 1, Available_books INTEGER DEFAULT 1, PRIMARY KEY (id),FOREIGN KEY(Category_id) REFERENCES Book_category(id) )")
    cur.execute("CREATE TABLE IF NOT EXISTS Member (id INTEGER NOT NULL, Name VARCHAR(25), Surname VARCHAR(50), Birthdate TEXT(25), Telephone_number VARCHAR(25), Mobile_number VARCHAR(25), Address VARCHAR(50), City VARCHAR(25), Po_box VARCHAR(10), Email VARCHAR(50), Facebook VARCHAR(50), Instagram VARCHAR(50), Active INTEGER, PRIMARY KEY (id))")
    cur.execute("CREATE TABLE IF NOT EXISTS Reservations (Reservation_id INTEGER NOT NULL, Member_id INTEGER, Book_id INTEGER, Reserve_date TEXT(25), PRIMARY KEY (Reservation_id) FOREIGN KEY (Member_id) REFERENCES Member(id), FOREIGN KEY (Book_id) REFERENCES Books(id))")
    conn.commit()
    conn.close()



def view():
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Books")
    rows = cur.fetchall()
    conn.close()
    return rows

#______________Book Functions_______________________

def add_new_book(isbn, dewey, title, category, desc, writer, publications, year, pubnumber, writedate, buydate, price, pages, selfnum, activebook, totalbooks, availablebooks):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Books (ISBN , Dewey_number ,Title ,Category_id ,Description ,Writer, Publications ,Year ,Publication_number ,Write_date ,Buy_date ,Price ,pages, Shelf_code ,Active, Total_books, Available_books )VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(isbn, dewey, title, category, desc, writer, publications, year, pubnumber, writedate, buydate, price, pages, selfnum, activebook,totalbooks, availablebooks))
    conn.commit()
    conn.close()  

def update_book(isbn, dewey, title, category, desc, writer, publications, year, pubnumber, writedate, buydate, price, pages, selfnum, activebook, totalbooks, availablebooks,id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Books SET ISBN =? , Dewey_number=? ,Title=? ,Category_id=? ,Description=? ,Writer=?, Publications=? ,Year=? ,Publication_number=? ,Write_date=? ,Buy_date=? ,Price=? ,pages=?, Shelf_code=? ,Active=?, Total_books=?, Available_books=? WHERE id = ? ", (isbn, dewey, title, category, desc, writer, publications, year, pubnumber, writedate, buydate, price, pages, selfnum, activebook, totalbooks, availablebooks,id))
    conn.commit()
    conn.close()  

def delete_book(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Books SET Active = 0 where id = ?", (id,))
    conn.commit()
    conn.close()

#_______________Member Functions____________________

def add_new_member(name, surname, birthdate, telephone, mobile, address, city, pobox, email, facebook, insta, active):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Member (Name, Surname, Birthdate, Telephone_number, Mobile_number, Address, City, Po_box, Email, Facebook, Instagram, Active )VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(name, surname, birthdate, telephone, mobile, address, city, pobox, email, facebook, insta, active))
    conn.commit()
    conn.close() 

def update_member(name, surname, birthdate, telephone, mobile, address, city, pobox, email, facebook, insta, active, id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Member SET Name =? , Surname=? , Birthdate =? , Telephone_number =? ,Mobile_number=? , Address=?, City =? ,Po_box=? , Email =? , Facebook =? , Instagram=?, Active =? WHERE id = ? ", (name, surname, birthdate, telephone, mobile, address, city, pobox, email, facebook, insta, active, id))
    conn.commit()
    conn.close()

def delete_member(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Member SET Active = 0 where id = ?", (id,))
    conn.commit()
    conn.close()


#______________ Search Functions________________________
def search_book_bybook(title="", category="", dewey="",activebook =1):
        if title != "":
            title = '%'+ title + '%'
        if category!= "":
            category = '%'+ category + '%'
        if dewey != "":
            dewey = '%'+ dewey + '%'
        conn = sqlite3.connect("BookareDB.db")
        cur = conn.cursor()
        cur.execute("SELECT Books.* , Book_category.Description FROM Books LEFT JOIN Book_category on Books.Category_id = Book_category.id WHERE (Title LIKE ? OR Book_category.Description LIKE ? OR Dewey_number LIKE ? ) and Active=?",(title,category,dewey, activebook))
        #cur.execute("SELECT * FROM Books WHERE Title LIKE ? OR Category_id LIKE ? OR Dewey_number LIKE ?",(title,category,dewey))
        rows = cur.fetchall()
        conn.close()
        return rows 

def search_book_bymember( membercode="",membername="", membersurname="", activemember=1):
        if membercode != "":
            membercode= '%'+ membercode + '%'
        if membername != "":
            membername = '%'+ membername + '%'
        if membersurname != "":
            membersurname = '%'+ membersurname + '%'
        conn = sqlite3.connect("BookareDB.db")
        cur = conn.cursor()
        cur.execute("SELECT Name, Surname, id, Telephone_number, Mobile_number, Email FROM Member WHERE (id LIKE ? OR Name LIKE ? OR Surname LIKE ?) and Active =?",(membercode, membername,membersurname,activemember))
        rows = cur.fetchall()
        conn.close()
        return rows 


def search_book_bywriter(writersurname=""):
        if writersurname != "":
            writersurname = '%'+ writersurname + '%'
        conn = sqlite3.connect("BookareDB.db")
        #conn.set_trace_callback(print)
        cur = conn.cursor()
        cur.execute("SELECT Books.*, Book_category.Description FROM Books INNER JOIN Book_category on Books.Category_id = Book_category.id WHERE Writer LIKE ? and Active=1",(writersurname,))
        rows = cur.fetchall()
        conn.close()
        return rows 

#__________________Search member in new booking_____________________________________________
def search_member_by_surname(membersurname=""):   
    if membersurname != "":
            membersurname = '%'+ membersurname + '%'    
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT id, Name, Surname, Mobile_number FROM Member WHERE Surname LIKE ? and Active =1",(membersurname,))
    membersinfo = cur.fetchall()
    conn.close()
    return membersinfo

#_______________Search book in new booking__________________________________________________
def search_book_byTitle(bookTitle=""):
    if bookTitle != "":
        bookTitle = '%'+ bookTitle + '%'  
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT id, Title, ISBN, Writer FROM Books WHERE Title LIKE ? and Active =1",(bookTitle,))
    bookbasicinfo = cur.fetchall()
    conn.close()
    return bookbasicinfo
#____________________Book categories Functions____________________

def get_book_categories():
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT  DISTINCT id, Description FROM Book_category")
    data = []
    for row in cur.fetchall():
        data.append(row)
    conn.close()
    return data
   
def add_new_category(cat_desc, cat_abb):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Book_category (Description, Abbreviation )VALUES (?,?)",(cat_desc, cat_abb))
    conn.commit()
    conn.close()  

def update_book_category(cat_desc, cat_abb,id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("UPDATE Book_category SET  Description =?, Abbreviation=? WHERE id = ? ", (cat_desc, cat_abb,id))
    conn.commit()
    conn.close()  

def delete_book_category(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Book_category where id = ?", (id,))
    conn.commit()
    conn.close()

#____________Refresh listboxes on Book TAB________________________
def listOn_bookRefreshBook(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT member.id, member.Surname, member.Name,Bookings.Start_date FROM Member INNER JOIN  Bookings ON  Member.id = Bookings.Member_id where Bookings.End_date is NULL and Bookings.Book_id =? ",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def listbooking_historyRefreshBook(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT member.id, member.Surname, member.Name,Bookings.Start_date, Bookings.End_date FROM Member INNER JOIN  Bookings ON  Member.id = Bookings.Member_id where Bookings.End_date is NOT NULL and Bookings.Book_id =? ",(id,))
    rows = cur.fetchall()
    conn.close() 
    return rows   

def listReservationsRefreshBook(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT member.id, member.Surname, member.Name, Reservations.Reserve_date FROM Member INNER JOIN  Reservations ON  Member.id = Reservations.Member_id where Reservations.Book_id =? ",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows
#________________Refresh listboxes on Member TAB______________________

def listOn_bookRefreshMember(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Books.id, Books.Title, Books.ISBN,Bookings.Start_date FROM Books INNER JOIN  Bookings ON  Books.id = Bookings.Book_id where Bookings.End_date is NULL and Bookings.Member_id =? ",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def listbooking_historyRefreshMember(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Books.id, Books.Title, Books.ISBN, Bookings.Start_date, Bookings.End_date FROM Books INNER JOIN  Bookings ON Books.id = Bookings.Book_id where Bookings.End_date is NOT NULL and Bookings.Member_id =? ",(id,))
    rows = cur.fetchall()
    conn.close() 
    return rows   

def listReservationsRefreshMember(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Books.id, Books.Title, Books.ISBN, Reservations.Reserve_date FROM Books INNER JOIN  Reservations ON  Books.id = Reservations.Book_id where Reservations.Member_id =? ",(id,))
    rows = cur.fetchall()
    conn.close()
    return rows
#__________________________________________________________________

#_____________Basic info for newbooking, new reservation windows_____________________________

def get_basic_book_info(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT Title, Writer, ISBN FROM Books WHERE id= ? ",(id,))
    basic_book_info= cur.fetchall()
    conn.close()
    return basic_book_info


def get_basic_member_info(id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT id, Name, Surname, Mobile_number FROM Member WHERE id= ? ",(id,))
    basic_member_info= cur.fetchall()
    conn.close()
    return basic_member_info

def add_new_reservation(member,id,date):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Reservations (Member_id, Book_id, Reserve_date)VALUES (?,?,?)",(member,id,date))
    conn.commit()
    conn.close()  

def delete_reservation(reservation, id):
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM Reservations where Member_id = ? AND Book_id = ?", (reservation, id))
    conn.commit()
    conn.close()  

#____________________________ Report Comboboxes data_______________________________________________

def get_all_members():
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT id, Surname, Name, Mobile_Number FROM Member ORDER by Surname")
    data = []
    for row in cur.fetchall():
        data.append(row)
    conn.close()
    return data

def get_all_books():
    conn = sqlite3.connect("BookareDB.db")
    cur = conn.cursor()
    cur.execute("SELECT id, Title, ISBN, Writer FROM Books ORDER by Title")
    data = []
    for row in cur.fetchall():
        data.append(row)
    conn.close()
    return data

connect()
