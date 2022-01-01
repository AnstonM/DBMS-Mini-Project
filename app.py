from flask import *
import sqlite3
import os
from forms import *



app = Flask(__name__) 
userid = 0
adminid = 0
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/index', methods=("GET","POST"))
def index():
    print('index opened')
    return render_template('index.html',userid=userid)

@app.route('/Adminindex', methods=("GET","POST"))
def Adminindex():
    return render_template('Adminindex.html',userid=userid)

@app.route('/CreateAccount', methods=("GET","POST"))
def CreateAccount():
    global userid
    form = CreateCustomerForm()
    if form.validate_on_submit():
        f = request.form
        name = f['firstname']+' '+f['lastname']
        phone = f['phone']
        if phone == '':
            phone = 'NULL'
        email = f['email']
        if email == '':
            email = 'NULL'
        username = f['username']
        password = f['password']
        confirmpassword = f['confirmpassword']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "INSERT INTO CUSTOMER(USERNAME,PWD,NAME,PH_NO,EMAIL) VALUES('"+username+"','"+password+"','"+name+"','"+phone+"','"+email+"')"
        cur.execute(query)
        con.commit()
        con.close()
        return redirect(url_for('login'))
    return render_template('AccountCreate.html',form=form)

@app.route('/AddAdmin', methods=("GET","POST"))
def AddAdmin():
    global userid
    form = CreateCustomerForm()
    if form.validate_on_submit():
        f = request.form
        name = f['firstname']+' '+f['lastname']
        phone = f['phone']
        if phone == '':
            phone = 'NULL'
        email = f['email']
        if email == '':
            email = 'NULL'
        username = f['username']
        password = f['password']
        confirmpassword = f['confirmpassword']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "INSERT INTO CUSTOMER(USERNAME,PWD,NAME,PH_NO,EMAIL) VALUES('"+username+"','"+password+"','"+name+"','"+phone+"','"+email+"')"
        cur.execute(query)
        con.commit()
        con.close()
        return redirect(url_for('Adminindex'))
    return render_template('AddAdmin.html',form=form)

@app.route('/')
@app.route('/login', methods=("GET","POST"))
def login():    
    global userid
    form = LoginForm()
    if form.validate_on_submit():
        userid = request.form
        userid = userid['username']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        for rowdata in rows: 
            if rowdata[1]==userid:
                userid=int(rowdata[0])        
        con.close()
        return redirect(url_for('index'))        
    else:       
        return render_template('login.html',form=form)

@app.route('/ManageAccount', methods=("GET","POST"))
def ManageAccount():
    form = LoginForm()
    return render_template('ManageAccount.html',form=form)


@app.route('/AdminLogin', methods=("GET","POST"))
def Adminlogin():
    global adminid;    
    form = AdminLoginForm()
    if form.validate_on_submit():
        adminid = request.form
        adminid = adminid['username']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        for rowdata in rows: 
            if rowdata[2]==adminid:
                adminid=int(rowdata[0])        
        con.close()
        print(adminid)
        return redirect(url_for('Adminindex')) 
    else:       
        return render_template('Adminlogin.html',form=form)
    






if __name__=='__main__':
    app.run(debug=True)