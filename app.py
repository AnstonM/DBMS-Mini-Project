from flask import *
import sqlite3
import os
from forms import *
from flask import flash 



app = Flask(__name__) 
userid = 0
adminid = 0
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY



@app.route('/index', methods=("GET","POST"))
def index():
    print('index opened')
    return render_template('index.html',userid=userid)

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
        flash("New Account has been successfully created ...")
        return redirect(url_for('login'))
    return render_template('AccountCreate.html',form=form)

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
        flash("Successfully Logged In")
        return redirect(url_for('index'))        
    else:       
        return render_template('login.html',form=form)

@app.route('/EditProfile', methods=("GET","POST"))
def EditProfile():
    global userid
    userName = '';Name = ''; FName ='';LName ='' ;ph = 0;emailId = ''
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from customer where customer_id = "+str(userid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[1]
            Name = rowdata[3]
            NameData = Name.split(' ')
            max = len(NameData)
            FName = ' '.join(NameData[0:max-1])
            LName = NameData[max-1]
            ph = rowdata[4]
            emailId = rowdata[5]
            break
    con.close()
    form = EditCustomerForm(username = userName, firstname = FName, lastname = LName, phone = ph, email= emailId)
    if form.validate_on_submit():
        f = request.form
        name = f['firstname']+' '+f['lastname']
        phone = f['phone']
        if phone == '':
            phone = 'NULL'
        email = f['email']
        if email == '':
            email = 'NULL'
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE CUSTOMER SET NAME = '"+name+"', PH_NO = '"+phone+"', EMAIL = '"+emailId+"' WHERE CUSTOMER_ID = "+str(userid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Your profile has been successfully updated.... ")
        return redirect(url_for('index'))
    return render_template('EditProfile.html',form=form)

@app.route('/ChangePassword', methods=("GET","POST"))
def ChangePassword():
    global userid
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from customer where customer_id = "+str(userid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[1]
            break
    con.close()
    form = ChangePasswordForm(username = userName)
    if form.validate_on_submit():
        f = request.form
        pwd = f['newpassword']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE CUSTOMER SET PWD = '"+pwd+"' WHERE CUSTOMER_ID = "+str(userid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Password changed Successfully.... ")
        return redirect(url_for('index'))
    return render_template('ChangePassword.html',form=form)

@app.route('/Delete', methods=("GET","POST"))
def Delete():
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "DELETE FROM CUSTOMER WHERE CUSTOMER_ID = "+str(userid)+";"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Account Deleted Successfully, You will be missed !!")
    form = LoginForm()
    return render_template('login.html',form=form)

@app.route('/DeleteAccount', methods=("GET","POST"))
def DeleteAccount():
    return render_template('DeleteAccount.html')




########################################################################################################################



@app.route('/AddAdmin', methods=("GET","POST"))
def AddAdmin():
    global userid
    form = AddAdminForm()
    if form.validate_on_submit():
        f = request.form
        name = f['name']
        username = f['username']
        password = f['password']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "INSERT INTO ADMIN(ANAME,AUSERNAME,APWD) VALUES('"+name+"','"+username+"','"+password+"')"
        cur.execute(query)
        con.commit()
        con.close()
        flash("New Admin added successfully....")
        return redirect(url_for('Adminindex'))
    return render_template('AddAdmin.html',form=form)

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
        flash("Successfully Logged In")
        return redirect(url_for('Adminindex')) 
    else:       
        return render_template('Adminlogin.html',form=form)
    
@app.route('/Adminindex', methods=("GET","POST"))
def Adminindex():
    return render_template('Adminindex.html',userid=userid)


@app.route('/ChangePasswordAdmin', methods=("GET","POST"))
def ChangePasswordAdmin():
    global adminid
    userName = '';Name = ''
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    cur.execute("Select * from admin where admin_id = "+str(adminid))
    rows = cur.fetchall()
    for rowdata in rows:
            userName = rowdata[2]
            Name = rowdata[1]
            break
    con.close()
    form = ChangeAdminPasswordForm(username = userName,name = Name)
    if form.validate_on_submit():
        f = request.form
        pwd = f['newpassword']
        newName = f['name']
        con = sqlite3.connect("DBMS.db")
        cur = con.cursor()
        query = "UPDATE ADMIN SET APWD = '"+pwd+"', ANAME ='"+newName+"' WHERE ADMIN_ID = "+str(adminid)+";" 
        cur.execute(query)
        con.commit()
        con.close()
        flash("Profile/Password Updated Successfully.... ")
        return redirect(url_for('Adminindex'))
    return render_template('ChangePasswordAdmin.html',form=form)

@app.route('/DeleteAdmin', methods=("GET","POST"))
def DeleteAdmin():
    global adminid
    con = sqlite3.connect("DBMS.db")
    cur = con.cursor()
    query = "DELETE FROM ADMIN WHERE ADMIN_ID = "+str(adminid)+";"
    cur.execute(query)
    con.commit()
    con.close()
    flash("Admin Account Deleted Successfully, You will be missed !!")
    form = LoginForm()
    return render_template('Adminlogin.html',form=form)

@app.route('/DeleteAccountAdmin', methods=("GET","POST"))
def DeleteAccountAdmin():
    return render_template('DeleteAccountAdmin.html')




if __name__=='__main__':
    app.run(debug=True)