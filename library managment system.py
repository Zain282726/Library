import pickle
import datetime
import random

class LibraryDatabase:
    def __init__(self):
        self.books = []
        self.users = []

    def add(self, book):
        self.books.append(book)
    
    def remove(self, book_title):
        for book in self.books:
            if book.title == book_title:
                self.books.remove(book)
                return
        print("Book not found")

    def search(self, book_title):
        for book in self.books:
            if book.title == book_title:
                return book
        return None
    
    def display(self):
        for book in self.books:
            print(book.title)

class LibraryMangment:
    def __init__(self,username,passw):
        self.user_name = username
        self.password = passw
        
class Librarian(LibraryMangment):
    def __init__(self, username, passw,name,id, database):
        super().__init__(username, passw)
        self.Name = name
        self.Id = id
        self.database = database
    
    def add_book(self, book):
        self.database.add(book)
        print("Book added")
    
    def remove_book(self, book_title):
        book = self.search_book(book_title)
        if book:
            self.database.remove(book.title)
            print("Book removed")
        else:
            print("Book not found")
    
    def search_book(self, book_title):
        book = self.database.search(book_title)
        if book:
            return book
        else:
            print("Book not found")
            return None
    
    def issue_book(self, book_title):
        book = self.search_book(book_title)
        if book:
            if book.issued:
                print("Book already issued")
                return False
            book.issued = True
            return (book, Transection(random.randint(32235, 15124125), book.Book_id, str(datetime.datetime.now()), random.randint(60, 80)))

        else:
            return False

    def return_book(self, book_title):
        book = self.search_book(book_title)
        if book:
            if not book.issued:
                print("Book already returned")
                return False
            book.issued = False
            return book
        else:
            return False


    def create_account(self, username, passw, name, id, address, account_type):
        for i in self.database.users:
            if i.user_name == username:
                print("User already exists")
                return False
        if account_type.lower() == "teacher":
            self.database.users.append(Teacher(username, passw, name, id, address))
        elif account_type.lower() == "student":
            self.database.users.append(Student(username, passw, name, id, address))

        print("Account created")

class Teacher(LibraryMangment):
    def __init__(self, username, passw,name,id,address):
        super().__init__(username, passw)
        self.Name = name
        self.Id = id
        self.Address = address
        self.Max_book_limit = float('inf')
        self.books = []
        self.transactions = []
        
    def issue_book(self, book_title, librarian):
        book = librarian.issue_book(book_title)
        if book:
            self.books.append(book[0])
            self.transactions.append(book[1])
            print("Book issued")
            return True
        else:
            return False
    
    def return_book(self, book_title, librarian):
        book = librarian.return_book(book_title)
        if book:
            self.books.remove(book)
            print("Book returned")
            return True
        else:
            return False

    def total_checked_books(self):
        return len(self.books)

    def check_transaction(self):
        for transaction in self.transactions:
            transaction.display()
            print('\n')

class Student(LibraryMangment):
    def __init__(self, username, passw,name,id,address):
        super().__init__(username, passw)        
        self.Name = name
        self.Id = id
        self.Address = address
        self.max_book_limit = 3
        self.books = []
        self.transactions = []
    
    def issue_book(self, book_title, librarian):
        book = librarian.issue_book(book_title)
        if book:
            if len(self.books) < self.max_book_limit:
                self.books.append(book[0])
                self.transactions.append(book[1])
                print("Book issued")
                return True
            else:
                print("Book limit reached")
                return False
            
    def return_book(self, book_title, librarian):
        book = librarian.return_book(book_title)
        if book:
            self.books.remove(book)
            print("Book returned")
            return True
        else:
            return False
    
    def total_checked_books(self):
        return len(self.books)
    
    def check_transaction(self):
        for transaction in self.transactions:
            transaction.display()
            print('\n')

class Books:
    def __init__(self,title,bookid,author,edition,publication, location):
        self.title = title
        self.Book_id = bookid 
        self.Author = author
        self.Edition = edition 
        self.Publication = publication
        self.Location = BookLocation(location[0], location[1], location[2], location[3])
        self.issued = False
        
    def get_location(self):
        self.Location.display()

class Bill:
    def __init__(self,amount):
        self.Amount = amount
    
    def display(self):
        print('Amount:',self.Amount)

        
class Transection:
    def __init__(self,id,bookid,dateofi,amount):
        self.Id = id
        self.Book_id = bookid
        self.Date_of_Issue = dateofi
        self.bill = Bill(amount)
    
    def display(self):
        print("Id:",self.Id)
        print("Book_id:",self.Book_id)
        print("Date_of_Issue:",self.Date_of_Issue)
        self.bill.display()
                
class BookLocation:
    def __init__(self,room,section,rac,row):
        self.Room = room
        self.Section = section
        self.Rac = rac
        self.Row = row
    
    def display(self):
        print("Room:",self.Room,"Section:",self.Section,"Rack:",self.Rac,"Row:",self.Row)
        


def save_data(database):
    with open("database.pickle", "wb") as f:
        pickle.dump(database, f)

def load_data():
    with open("database.pickle", "rb") as f:
        return pickle.load(f)

def main():
    
    try:
        database = load_data()
    except FileNotFoundError:
        database = LibraryDatabase()
        save_data(database)

    librarian = Librarian('admin','admin','Librarian','1',database)


    while True:
        print("1. Login as Librarian")
        print("2. Login as Teacher")
        print("3. Login as Student")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if librarian.user_name == username and librarian.password == password:
                print("Login successful")
                while True:
                    print("1. Add Book")
                    print("2. Remove Book")
                    print("3. Search Book")
                    print("4. Create Account")
                    print("5. Logout")
                    choice = input("Enter your choice: ")
                    if choice == '1':
                        title = input("Enter title: ")
                        bookid = input("Enter bookid: ")
                        author = input("Enter author: ")
                        edition = input("Enter edition: ")
                        publication = input("Enter publication: ")
                        location = input("Enter location (Format: Room,section,rac,row): ")
                        location = location.split(',')

                        librarian.add_book(Books(title,bookid,author,edition,publication,location))
                        save_data(database)

                    elif choice == '2':
                        title = input("Enter title: ")
                        librarian.remove_book(title)
                        save_data(database)
                    
                    elif choice == '3':
                        title = input("Enter title: ")
                        book = librarian.search_book(title)
                        if book:
                            print("Book present at:")
                            book.get_location()
                    
                    elif choice == '4':
                        account_type = input("Enter account type (Teacher/Student): ")
                        username = input("Enter username: ")
                        password = input("Enter password: ")
                        name = input("Enter name: ")
                        id = input("Enter id: ")
                        address = input("Enter address: ")
                        
                        librarian.create_account(username, password, name, id, address, account_type)
                        save_data(database)
                    
                    elif choice == '5':
                        print("Logged out")
                        break
                    
                    else:
                        print("Invalid choice")

            else:
                print("Login failed")
            
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")

            user = None
            for i in database.users:
                if i.user_name == username and i.password == password:
                    print("Login successful")
                    user = i
                    break

            if not user:
                print("Login failed")
                continue

            while True:
                print("1. Issue Book")
                print("2. Return Book")
                print("3. Total Checked Books")
                print("4. Check Transaction")
                print("5. Logout")
                choice = input("Enter your choice: ")
                if choice == '1':
                    title = input("Enter title: ")
                    user.issue_book(title, librarian)
                    save_data(database)
                elif choice == '2':
                    title = input("Enter title: ")
                    user.return_book(title, librarian)
                    save_data(database)
                elif choice == '3':
                    print("Total checked books:",user.total_checked_books())
                elif choice == '4':
                    print("Transaction History:")
                    user.check_transaction()
                elif choice == '5':
                    print("Logged out")
                    break
                else:
                    print("Invalid choice")
        
        elif choice == '3':
            username = input("Enter username: ")
            password = input("Enter password: ")

            user = None
            for i in database.users:
                if i.user_name == username and i.password == password:
                    print("Login successful")
                    user = i
                    break

            if not user:
                print("Login failed")
                continue

            while True:
                print("1. Issue Book")
                print("2. Return Book")
                print("3. Total Checked Books")
                print("4. Check Transaction")
                print("5. Logout")
                choice = input("Enter your choice: ")
                if choice == '1':
                    title = input("Enter title: ")
                    user.issue_book(title, librarian)
                    save_data(database)
                elif choice == '2':
                    title = input("Enter title: ")
                    user.return_book(title, librarian)
                    save_data(database)
                elif choice == '3':
                    print("Total checked books:",user.total_checked_books())
                elif choice == '4':
                    print("Transaction History:")
                    user.check_transaction()
                elif choice == '5':
                    print("Logged out")
                    break
                else:
                    print("Invalid choice")
        
        elif choice == '4':
            print("Exiting")
            break
        else:
            print("Invalid choice")

main()

