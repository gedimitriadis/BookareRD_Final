# python code creating reports
import pandas as pd
import sqlite3
import numpy as np
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML,CSS
import webbrowser
import os
import sys
import pkg_resources


css = CSS(string='''
    @page {size: A4 landscape; margin: 1cm;} 
    th, td {border: 1px solid black;}
    ''')

def reportAllMembers():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT id, Name, Surname, Address, City, Po_box, Telephone_number, Mobile_number, Email FROM Member", con)
    df = df.rename(columns={'id': 'Κωδικός μέλους', 'Name': 'Όνομα','Surname': 'Επώνυμο','Address': 'Διεύθυνση','City': 'Πόλη','Po_box': 'Τ.Κ.','Telephone_number': 'Σταθερό τηλέφωνο','Mobile_number': 'Κινητό τηλέφωνο', 'Email':'Email'})
    #-----
   #  Set up the Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template file
    template = jinja_env.get_template('ReportTemplate.html')


    html = template.render(ReportTitle =  'Μέλη',
                        data= df.head(10000)
                        )
    report_path = os.path.join(template_dir, "Allmembers.html")
    
    with open(report_path, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("Allmembers.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print (os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'templates', 'Allmembers.html'),new=2)
    print ('file://' + os.path.join(BASE_DIR, 'templates', 'Allmembers.html'))

    


def reportAllBooks():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT id, Title, ISBN, Dewey_number, Writer, Total_books, Available_books, Shelf_code FROM Books", con)
    df = df.rename(columns={'id': 'Κωδικός βιβλίου', 'Title': 'Τίτλος','Dewey_number': 'Αριθμός Dewey','Writer': 'Συγγραφέας','Total_books': 'Συνολικά Αντίτυπα','Available_books': 'Διαθέσιμα βιβλία','Shelf_code': 'Τοποθέτηση ραφιού'})
    
    
    #  Set up the Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template file
    template = jinja_env.get_template('ReportTemplate.html')


    html = template.render(ReportTitle =  'Βιβλία',
                        data= df.head(10000)
                        )
    report_path = os.path.join(template_dir, "AllBooks.html")
    
    with open(report_path, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("AllBooks.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print (os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'templates', 'AllBooks.html'),new=2)
    print ('file://' + os.path.join(BASE_DIR, 'templates', 'AllBooks.html'))

def reportBookHistory(bookid,bookCredentials):
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df1 = pd.read_sql_query("SELECT Member.Name, Member.Surname, Bookings.Start_date, Bookings.End_date ,Books.Title, Books.ISBN FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id  INNER JOIN Books On Books.id = Bookings.Book_id where Bookings.Book_id = ? ", con, params=(bookid,))
    df = pd.read_sql_query("SELECT Member.Name, Member.Surname, Bookings.Start_date, Bookings.End_date FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id where Bookings.Book_id = ? ", con, params=(bookid,))
    df = df.rename(columns={'Name': 'Όνομα', 'Surname': 'Επώνυμο','Start_date': 'Ημ/νία δανεισμού','End_date': 'Ημ/νία επιστροφής'})
    
   #  Set up the Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template file
    template = jinja_env.get_template('ReportTemplate.html')
    
    bookitle = df1.iloc[0]['Title']
    ISBN = df1.iloc[0]['ISBN'] 
    html = template.render(ReportTitle = 'Ιστορικό δανεισμού βιβλίου',
                           SecondTitle = 'Κωδικός βιβλίου: ' + bookCredentials[0]+ ' / ' + 'Τίτλος: ' + bookitle + ' / ' + 'ISBN: '+ ISBN ,
                           data= df.head(10000)
                        )
 

    report_path = os.path.join(template_dir, "ReportBookingHistory.html")
    
    with open(report_path, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("ReportBookingHistory.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print (os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'templates', 'ReportBookingHistory.html'),new=2)
    print ('file://' + os.path.join(BASE_DIR, 'templates', 'ReportBookingHistory.html'))

def reportMemberHistory(memberid, memberCredentials):
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT Bookings.Book_id, Books.Title, Bookings.Start_date, Bookings.End_date  FROM  Member INNER join Bookings ON Member.id = Bookings.Member_id INNER JOIN  Books ON Bookings.Book_id = Books.id where Member.id= ? ", con, params=(memberid,))
    df = df.rename(columns={'Book_id': 'Κωδικός βιβλίου', 'Title': 'Τίτλος','Start_date': 'Ημ/νία δανεισμού','End_date': 'Ημ/νία επιστροφής'})
    
     #Set up the Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template file
    template = jinja_env.get_template('ReportTemplate.html')

    html = template.render(ReportTitle = 'Ιστορικό δανεισμού μέλους',
                           SecondTitle = 'Κωδικός μέλους: ' + memberCredentials[0]+ ' / ' + 'Όνοματεπώνυμο: ' + memberCredentials[2] + ' ' +  memberCredentials[1] + ' / ' + 'Κινητό: ' + memberCredentials[3],
                            data= df.head(10000)
                        )

    report_path = os.path.join(template_dir, "ReportMemberHistory.html")
    
    with open(report_path, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("ReportMemberHistory.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print (os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'templates', 'ReportMemberHistory.html'),new=2)
    print ('file://' + os.path.join(BASE_DIR, 'templates', 'ReportMemberHistory.html'))
 

        
def reportBooksNotReturned():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("BookareDB.db")
    df = pd.read_sql_query("SELECT  Member.Surname, Member.Name,Member.Mobile_number, Member.Email, Books.Title, Books.ISBN, Bookings.Start_date from Bookings INNER JOIN Member ON Bookings.Member_id = Member.id INNER JOIN Books ON Bookings.Book_id = Books.id where  date(Start_date, '+15 day') < Date() and End_date ISNULL", con)
    df = df.rename(columns={'Surname': 'Επώνυμο', 'Name': 'Όνομα','Mobile_number': 'Κινητό τηλέφωνο','Title': 'Τίτλος','Start_date': 'Ημ/νία Δανεισμού'})

    #Set up the Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template file
    template = jinja_env.get_template('ReportTemplate.html')

    html = template.render(ReportTitle = 'Μέλη με ληξιπρόθεσμους δανεισμούς βιβλίων',
                            data= df.head(10000)
                        )

    report_path = os.path.join(template_dir, "BooksNotReturned.html")
    
    with open(report_path, 'w') as f:
        f.write(html)
    HTML(string=html).write_pdf("BooksNotReturned.pdf", stylesheets=[css])
    #Open browser to show report
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print (os.path.abspath(__file__))
    webbrowser.open('file://' + os.path.join(BASE_DIR, 'templates', 'BooksNotReturned.html'),new=2)
    print ('file://' + os.path.join(BASE_DIR, 'templates', 'BooksNotReturned.html'))


