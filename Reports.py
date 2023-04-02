# python code creating reports
import pandas as pd
import sqlite3
import numpy as np
from jinja2 import Environment, FileSystemLoader, PackageLoader
from weasyprint import HTML,CSS
import webbrowser
import os
import sys
#import logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger

css = CSS(string='''
    @page {size: A4 landscape; margin: 1cm;} 
    th, td {border: 1px solid black;}
    ''')

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def resource_path(relative_path, file_name):
    """ Get absolute path to resource, works for both in IDE and for PyInstaller """
    # PyInstaller creates a temp folder and stores path in sys._MEIPASS
    # In IDE, the path is os.path.join(base_path, relative_path, file_name)
    # Search in Dev path first, then MEIPASS
    #base_path = os.path.abspath(".")
    base_path = os.getcwd()
    dev_file_path = os.path.join(base_path, relative_path, file_name)
    if os.path.exists(dev_file_path):
        return dev_file_path
    else:
        base_path = sys.executable
        file_path = os.path.join(base_path, file_name)
        if not os.path.exists(file_path):
            msg = "\nError finding resource in either {} or {}".format(dev_file_path, file_path)
            print(msg)
            return None
        return file_path

def reportAllMembers():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT id, Name, Surname, Address, City, Po_box, Telephone_number, Mobile_number, Email FROM Member", con)
    df = df.rename(columns={'id': 'Κωδικός μέλους', 'Name': 'Όνομα','Surname': 'Επώνυμο','Address': 'Διεύθυνση','City': 'Πόλη','Po_box': 'Τ.Κ.','Telephone_number': 'Σταθερό τηλέφωνο','Mobile_number': 'Κινητό τηλέφωνο', 'Email':'Email'})
    #-----
    template_file_name = 'ReportTemplate.html'
    template_file_path = resource_path('templates', template_file_name)
    template_file_directory = os.path.dirname(template_file_path)
    print(template_file_directory)
    template_loader = FileSystemLoader(searchpath=template_file_directory)
    env = Environment(loader=template_loader)  # Jinja2 template environment
    template = env.get_template(template_file_name)

   #------
   
    # Template handling
    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template("ReportTemplate.html")

    html = template.render(ReportTitle = 'Μέλη βιβλιοθήκης',
                            data= df.head(10000)
                        )
    

    with open('AllMembers.html', 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("AllMembers.pdf", stylesheets=[css])
    # Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'AllMembers.html'),new=2)

    
def reportAllBooks():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT id, Title, ISBN, Dewey_number, Writer, Total_books, Available_books, Shelf_code FROM Books", con)
    df = df.rename(columns={'id': 'Κωδικός βιβλίου', 'Title': 'Τίτλος','Dewey_number': 'Αριθμός Dewey','Writer': 'Συγγραφέας','Total_books': 'Συνολικά Αντίτυπα','Available_books': 'Διαθέσιμα βιβλία','Shelf_code': 'Τοποθέτηση ραφιού'})
    
    template_file_name = 'ReportTemplate.html'
    template_file_path = resource_path('templates', template_file_name)
    template_file_directory = os.path.dirname(template_file_path)
    print(template_file_directory)
    template_loader = FileSystemLoader(searchpath=template_file_directory)
    env = Environment(loader=template_loader)  # Jinja2 template environment
    template = env.get_template(template_file_name)
    # Template handling
    # env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template("ReportTemplate.html")

    html = template.render(ReportTitle =  'Βιβλία',
                        data= df.head(10000)
                        )

    with open('AllBooks.html', 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("AllBooks.pdf", stylesheets=[css])
    # Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'AllBooks.html'),new=2)

def reportAllBooksB():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT id, Title, ISBN, Dewey_number, Writer, Total_books, Available_books, Shelf_code FROM Books", con)
    df = df.rename(columns={'id': 'Κωδικός βιβλίου', 'Title': 'Τίτλος','Dewey_number': 'Αριθμός Dewey','Writer': 'Συγγραφέας','Total_books': 'Συνολικά Αντίτυπα','Available_books': 'Διαθέσιμα βιβλία','Shelf_code': 'Τοποθέτηση ραφιού'})
    
    path = os.getcwd()
    if getattr(sys, 'frozen', False):
        #logger.debug("We are running in a bundle!")
        path = getattr(sys, '_MEIPASS', os.getcwd())
        #logger.debug("Bundle path" + path)

    file_loader = FileSystemLoader(os.path.join(path, 'templates'))
    env = Environment(loader=file_loader)
    template = env.get_template('ReportTemplate.html')    
    
    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template('ReportTemplate.html')

    html = template.render(ReportTitle =  'Βιβλία',
                        data= df.head(10000)
                        )
    filename = 'AllBooksB.html'
    with open(filename, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("AllBooksB.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'AllBooksB.html'),new=2)
    

def reportBookHistory(bookid,bookCredentials):
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df1 = pd.read_sql_query("SELECT Member.Name, Member.Surname, Bookings.Start_date, Bookings.End_date ,Books.Title, Books.ISBN FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id  INNER JOIN Books On Books.id = Bookings.Book_id where Bookings.Book_id = ? ", con, params=(bookid,))
    df = pd.read_sql_query("SELECT Member.Name, Member.Surname, Bookings.Start_date, Bookings.End_date FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id where Bookings.Book_id = ? ", con, params=(bookid,))
    df = df.rename(columns={'Name': 'Όνομα', 'Surname': 'Επώνυμο','Start_date': 'Ημ/νία δανεισμού','End_date': 'Ημ/νία επιστροφής'})
    
    # Template handling
    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template("ReportTemplate.html")
    template_file_name = 'ReportTemplate.html'
    template_file_path = resource_path('templates', template_file_name)
    template_file_directory = os.path.dirname(template_file_path)
    print(template_file_directory)
    template_loader = FileSystemLoader(searchpath=template_file_directory)
    env = Environment(loader=template_loader)  # Jinja2 template environment
    template = env.get_template(template_file_name)

    
    bookitle = df1.iloc[0]['Title']
    ISBN = df1.iloc[0]['ISBN'] 
    html = template.render(ReportTitle = 'Ιστορικό δανεισμού βιβλίου',
                           SecondTitle = 'Κωδικός βιβλίου: ' + bookCredentials[0]+ ' / ' + 'Τίτλος: ' + bookitle + ' / ' + 'ISBN: '+ ISBN ,
                           data= df.head(10000)
                        )

    with open('Book_BookingHistory.html', 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("Book_BookingHistory.pdf", stylesheets=[css])
    # Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'Book_BookingHistory.html'),new=2)


def reportMemberHistory(memberid, memberCredentials):
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT Bookings.Book_id, Books.Title, Bookings.Start_date, Bookings.End_date  FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id INNER JOIN  Books ON Bookings.Book_id = Books.id where Member.id= ? ", con, params=(memberid,))
    df = df.rename(columns={'Book_id': 'Κωδικός βιβλίου', 'Title': 'Τίτλος','Start_date': 'Ημ/νία δανεισμού','End_date': 'Ημ/νία επιστροφής'})
    
    # Template handling
    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template("ReportTemplate.html")
    template_file_name = 'ReportTemplate.html'
    template_file_path = resource_path('templates', template_file_name)
    template_file_directory = os.path.dirname(template_file_path)
    print(template_file_directory)
    template_loader = FileSystemLoader(searchpath=template_file_directory)
    env = Environment(loader=template_loader)  # Jinja2 template environment
    template = env.get_template(template_file_name)

    html = template.render(ReportTitle = 'Ιστορικό δανεισμού μέλους',
                           SecondTitle = 'Κωδικός μέλους: ' + memberCredentials[0]+ ' / ' + 'Όνοματεπώνυμο: ' + memberCredentials[2] + ' ' +  memberCredentials[1] + ' / ' + 'Κινητό: ' + memberCredentials[3],
                            data= df.head(10000)
                        )

    with open('Member_BookingHistory.html', 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("Member_BookingHistory.pdf", stylesheets=[css])  
    # Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'Member_BookingHistory.html'),new=2)
 

        
def reportBooksNotReturned():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT  Member.Surname, Member.Name,Member.Mobile_number, Member.Email, Books.Title, Books.ISBN, Bookings.Start_date from Bookings INNER JOIN Member ON Bookings.Member_id = Member.id INNER JOIN Books ON Bookings.Book_id = Books.id where  date(Start_date, '+15 day') < Date() and End_date ISNULL", con)
    df = df.rename(columns={'Surname': 'Επώνυμο', 'Name': 'Όνομα','Mobile_number': 'Κινητό τηλέφωνο','Title': 'Τίτλος','Start_date': 'Ημ/νία Δανεισμού'})

    # Template handling
    #env = Environment(loader=FileSystemLoader('templates'))
    #template = env.get_template("ReportTemplate.html")
    template_file_name = 'ReportTemplate.html'
    template_file_path = resource_path('templates', template_file_name)
    template_file_directory = os.path.dirname(template_file_path)
    print(template_file_directory)
    template_loader = FileSystemLoader(searchpath=template_file_directory)
    env = Environment(loader=template_loader)  # Jinja2 template environment
    template = env.get_template(template_file_name)

    html = template.render(ReportTitle = 'Μέλη με ληξιπρόθεσμους δανεισμούς βιβλίων',
                            data= df.head(10000)
                        )

    with open('BooksNotReturned.html', 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("BooksNotReturned.pdf", stylesheets=[css]) 
    # Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'BooksNotReturned.html'),new=2)


