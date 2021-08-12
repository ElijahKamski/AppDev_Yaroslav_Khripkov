from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPicture, QPixmap
from PyQt5.Qt import QFont
import paramiko
import sys
import sqlalchemy
engine=sqlalchemy.create_engine('mysql+pymysql://ws2021:WorldSkills2021!@localhost:3306/wsdb')
engine.connect()
logged=0
class AddEdit(QDialog):
    def __init__(self):
        super(AddEdit, self).__init__()
        self.gbl = QGridLayout()
        self.cusL = QLabel('ID')
        self.IdIn = QLineEdit()
        self.NamL = QLabel('Name')
        self.NameIn = QLineEdit()
        self.adl = QLabel('Address')
        self.adIn = QLineEdit()
        self.zipl = QLabel('Zip/City')
        self.ZipIn = QLineEdit()
        self.CityIn = QLineEdit()
        self.PhL = QLabel('Phone')
        self.PhIn = QLineEdit()
        self.mail = QLabel('Email')
        self.EmIn = QLineEdit()
        self.savebtn = QPushButton('Save')
        self.Cancel = QPushButton('Cancel')
        #5x5
        self.gbl.addWidget(self.cusL, 0, 0)
        self.gbl.addWidget(self.IdIn,0,1,0,2)
        self.gbl.addWidget(self.NamL, 1,0)
        self.gbl.addWidget(self.NameIn,1,1,1,2)
        self.gbl.addWidget(self.adl, 2,0)
        self.gbl.addWidget(self.adIn, 2,1,2,2)
        self.gbl.addWidget(self.zipl, 3,0)
        self.gbl.addWidget(self.ZipIn, 3,1)
        self.gbl.addWidget(self.CityIn, 3,2)
        self.gbl.addWidget(self.PhL, 1,3)
        self.gbl.addWidget(self.PhIn, 1,4)
        self.gbl.addWidget(self.mail,2,3)
        self.gbl.addWidget(self.EmIn,2,4)
        self.gbl.addWidget(self.savebtn, 3, 3)
        self.gbl.addWidget(self.Cancel, 3, 4)
        self.setLayout(self.gbl)
        self.IdIn.setEnabled(False)
        self.savebtn.clicked.connect(self.savebtn)
        self.Cancel.clicked.connect(self.close)
        self.show()
    def cancel(self):
        self.close()
    def save(self):
        idd=self.IdIn.text()
        name=self.NameIn.text()
        address=self.adIn.text()
        zipp=self.ZipIn.text()
        city=self.CityIn.text()
        phone=self.PhIn.text()
        email=self.EmIn.text()
        engine.execute(f"Insert INTO `wsdb`.`Customers`(`ID`,`Name`,`Address`,`Zip`,`City`,`Phone`,`Email`)VALUES({idd},{name},{address},{zipp},{city},{phone},{email});")
        self.close()


class ManageWindow(QDialog) :
    def __init__(self):
        super(ManageWindow, self).__init__()
        self.gb=QGroupBox()
        self.gbl=QVBoxLayout()
        self.cusL=QLabel('Customer ID')
        self.IdIn=QLineEdit()
        self.NamL=QLabel('Name')
        self.NameIn=QLineEdit()
        self.searchbtn=QPushButton('Search')
        self.EditBtn=QPushButton('Edit..')
        self.Addbtn=QPushButton('Add...')
        self.gbl.addWidget(self.cusL)
        self.gbl.addWidget(self.IdIn)
        self.gbl.addWidget(self.NamL)
        self.gbl.addWidget(self.NameIn)
        self.gbl.addWidget(self.searchbtn)
        self.gbl.addWidget(self.EditBtn)
        self.gbl.addWidget(self.Addbtn)
        self.gb.setLayout(self.gbl)
        self.lay=QHBoxLayout(self)
        self.lay.addWidget(self.gb)
        self.tabt=QTableWidget()
        self.lay.addWidget(self.tabt)
        self.tabt.setColumnCount(7)
        self.tabt.setHorizontalHeaderLabels(['ID', 'Name', 'Address', 'Zip', 'City', 'Phone', 'Email'])
        self.setLayout(self.lay)
        self.show()
        self.searchbtn.clicked.connect(self.search)
        self.Addbtn.clicked.connect(self.add)
        self.EditBtn.clicked.connect(self.add)
    def search(self):
        strings=[]
        name=self.NameIn.text()
        Id = self.IdIn.text()
        if(Id):
            strings=engine.execute(f'select * from Customers where Customers.ID="{Id}";').fetchall()
            strings = list(map(list, strings))
        elif name:
            strings = engine.execute(f'select * from Customers where Customers.Name rlike "{name};"').fetchall()
            strings = list(map(list, strings))
        else:
            strings = engine.execute(f'select * from Customers;').fetchall()
            strings = list(map(list, strings))
        self.tabt.setRowCount(len(strings))
        for i in range(len(strings)):
            for j in range(7):
                self.tabt.setItem(i,j,QTableWidgetItem(str(strings[i][j])))
    def add(self):
        ae=AddEdit()
        ae.exec_()




class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.userIn=QLineEdit()
        self.passIn=QLineEdit()
        self.passIn.setEchoMode(QLineEdit.Password)
        self.loginL=QLabel('Username')
        self.passL=QLabel('Password')
        self.logbtn=QPushButton('Login')
        self.cancelbtn=QPushButton('Cancel')
        layout=QGridLayout(self)
        layout.addWidget(self.loginL, 0,0)
        layout.addWidget(self.userIn, 0,1)
        layout.addWidget(self.passL, 1,0)
        layout.addWidget(self.passIn, 1,1)
        layout.addWidget(self.logbtn, 2,0)
        layout.addWidget(self.cancelbtn,2,1)
        self.setLayout(layout)
        self.logbtn.clicked.connect(self.login)
        self.cancelbtn.clicked.connect(self.cancel)
        self.show()
    def cancel(self):
        self.close()
    def login(self):
        if(self.userIn.text()=='administrator' and self.passIn.text()=='admin123'):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

class MainWindow(QWidget) :
    def __init__(self):
        super().__init__()
        self.setFont(QFont('Tahoma'))
        self.setGeometry(100,100,700,600)
        self.menu=QMenuBar()
        self.mfile = self.menu.addMenu('File')
        self.mlib= self.menu.addMenu('Library')
        self.login_action=QAction('Login', self)
        self.logout_action=QAction('Logout', self)
        self.logout_action.setEnabled(False)
        self.manage_act = QAction('Manage Customers', self)
        self.circul_act = QAction('Circulation', self)
        self.reports_act = QAction('Reports', self)
        self.exit_action=QAction('Exit', self)
        self.mfile.addAction(self.login_action)
        self.mfile.addAction(self.logout_action)
        self.mfile.addAction(self.exit_action)
        self.mlib.addAction(self.manage_act)
        self.mlib.addAction(self.circul_act)
        self.mlib.addAction(self.reports_act)
        self.setWindowTitle("BookMaster3000. Browse Catalog")
        self.lay=QGridLayout(self)
        self.gb1=QGroupBox()
        self.gb1l=QGridLayout(self.gb1)
        self.logo=QLabel()
        px=QPixmap('Logo.png')
        self.logo.setPixmap(px)
        self.gb1l.addWidget(self.logo, 0,0)
        self.labelTitle = QLabel("Title")
        self.gb1l.addWidget(self.labelTitle,1,0)
        self.titleInput=QLineEdit()
        self.gb1l.addWidget(self.titleInput,1,1)
        self.authLabel=QLabel("Author")
        self.authInput=QLineEdit()
        self.subjlab=QLabel("Subject")
        self.subjIn=QLineEdit()
        self.gb1l.addWidget(self.authLabel, 2,0)
        self.gb1l.addWidget(self.authInput, 2, 1)
        self.gb1l.addWidget(self.subjlab, 3, 0)
        self.gb1l.addWidget(self.subjIn, 3, 1)
        self.btn=QPushButton("Search")
        self.gb1l.addWidget(self.btn, 4,1)
        self.lstv=QTableWidget()
        self.lstv.setColumnCount(2)
        self.lstv.setHorizontalHeaderLabels(['Ttile', 'Author'])
        self.gb2=QGroupBox()
        self.gb2l=QGridLayout(self.gb2)
        self.BookTitle=QLabel("")
        self.gb2l.addWidget(self.BookTitle, 0,0)
        self.Authors = QLabel("")
        self.gb2l.addWidget(self.Authors, 1, 0)
        self.Publ = QLabel("")
        self.gb2l.addWidget(self.Publ, 2, 0)
        self.Desc = QLabel("")
        self.gb2l.addWidget(self.Desc, 3, 0)
        self.Subj = QLabel("")
        self.gb2l.addWidget(self.Subj, 4, 0)
        self.Obl = QLabel("")
        #self.mlib.setEnabled(False)
        # px1=QPixmap('Oblozhka.jpg')
        # self.Obl.setPixmap(px1)
        # self.Obl.setGeometry(0,0,5,5)
        # self.gb2l.addWidget(self.Obl, 4,1)
        self.lay.addWidget(self.lstv, 0,1)
        self.gb2.setLayout(self.gb2l)
        self.lay.addWidget(self.gb2, 1,1)
        self.gb1.setLayout(self.gb1l)
        self.lay.addWidget(self.gb1,0,0)
        self.lay.setMenuBar(self.menu)
        self.setLayout(self.lay)
        self.lstv.itemClicked.connect(self.draw_info)
        self.btn.clicked.connect(self.search_clicked)
        self.login_action.triggered.connect(self.login)
        self.manage_act.triggered.connect(self.showManage)
        self.show()
    def showManage(self):
        mg=ManageWindow()
        print(1)
        mg.exec_()
    def logout(self):
        global logged
        logged=0
        self.login_action.setEnabled(True)
        self.logout_action.setEnabled(False)
        self.mlib.setEnabled(False)
    def login(self):
        lg=LoginWindow()
        a=lg.exec_()
        if a:
            self.login_action.setEnabled(False)
            self.logout_action.setEnabled(True)
            global logged
            logged=1
            self.mlib.setEnabled(True)
    def draw_info(self):
        self.BookTitle.setText("Some selected book")
        self.Authors.setText("Some authors from selected book")

    def search_clicked(self):
        title=self.titleInput.text()
        author=self.authInput.text()
        subject=self.subjIn.text()
        res=self.find_the_book(title,author,subject)
        titles=[engine.execute(f'select Title from Books where Books.Key="{i}"').fetchall()[0] for i in res]
        titles=list(map(lambda x:x[0], titles))
        authors=[]
        for i in res:
            authors_id=list(map(lambda x:x[0], engine.execute(f'select AuthorKey from BookAuthors where BookKey="{i}"').fetchall()))
            auts = []
            for j in authors_id:
                au=engine.execute(f'select Authors.Name from Authors where Authors.Key="{j}"').fetchall()[0][0]
                auts.append(au)
            authors.append(', '.join(auts))
        self.lstv.setRowCount(len(titles))
        for i in range(len(titles)):
            self.lstv.setItem(i, 0, QTableWidgetItem(titles[i]))
            self.lstv.setItem(i, 1, QTableWidgetItem(authors[i]))
    def find_the_book(self, title, author, subject):
        res=set()
        a=engine.execute('select Books.Key from Books;').fetchall()
        res=set(map(lambda x:x[0], a))
        if(title):
            a = engine.execute(f'select Books.Key from Books where Title rlike "{title}";').fetchall()
            res=res.intersection(set(map(lambda x:x[0], a)))
        if (author):
            a=engine.execute(f'select BookKey from BookAuthors where AuthorKey in (select Authors.Key from Authors where Name rlike "{author}");').fetchall()
            res = res.intersection(
                set(map(lambda x:x[0], a)))
        if (subject):
            a=engine.execute(
                    f'select BookKey from BookSubjects where Subject rlike "{subject}";').fetchall()
            res = res.intersection(set(map(lambda x:x[0], a)))
        if len(res)>=49:
            return list(res)[:50]
        return res

if __name__=="__main__":

    app=QApplication([])
    wind=MainWindow()
    sys.exit(app.exec_())


