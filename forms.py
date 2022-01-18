from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from wtforms.validators import email_validator
import sqlite3
import re

driverList = [(101,101),(102,102),(103,103),(104,104),(105,105),(106,106),(107,107),(108,108)]

class LoginForm(FlaskForm):

    def user_in(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data != rowdata[1]:
                count += 1
        if count == len(rows):
            raise ValidationError('UserName does not exist !!!')
        con.close()

    def valid_pass(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if rowdata[1]==form.username.data:
                if rowdata[2]!=field.data:                    
                    raise ValidationError('Invalid Password !!!')        
        con.close()

    username = StringField('User Name',[DataRequired(),user_in])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    submit = SubmitField(label='SIGN IN',)



class AdminLoginForm(FlaskForm):

    def user_in(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        count = 0
        username1 = field.data
        for rowdata in rows: 
            if field.data != rowdata[2]:
                count += 1
        if count == len(rows):
            raise ValidationError(message='UserName does not exist !!!')
        con.close()

    def valid_pass(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        for rowdata in rows: 
            if rowdata[2]==form.username.data:
                if rowdata[3]!=field.data:                    
                     raise ValidationError(message='Invalid Password !!!')        
            con.close()

    username = StringField('User Name',[DataRequired(),user_in])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    submit = SubmitField(label='SIGN IN')

class CreateCustomerForm(FlaskForm):

    def validname(form,field):
        if not field.data.isalpha():
            raise ValidationError('Name should contain alphabets only !!!') 
    
    def username_nottaken(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data == rowdata[1]:
                raise ValidationError(message='UserName is Taken !!!')
        con.close()
        
    def valid_phone(form,field):
        if len(field.data) != 10:
            raise ValidationError(message='Invalid Phone Number !!!')
        elif not field.data.isdecimal():
            raise ValidationError(message='Invalid Phone Number !!!')

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
    
    def valid_email(form,field):
        regex = re.compile(r'''(
            [a-zA-Z0-9._%+-]+
            @
            [a-zA-Z0-9.-]+
            (\.[a-zA-Z]{2,4})
            )''',re.VERBOSE
        )
        list = regex.findall(field.data)
        if list == []:
            raise ValidationError(message='Invalid Email')



            
        

    firstname = StringField('First Name',[DataRequired(),validname])
    lastname = StringField('Last Name',[DataRequired(),validname])
    phone = StringField('Phone No',[valid_phone])
    email = EmailField('Email',[valid_email])
    username = StringField('User Name',[DataRequired(),username_nottaken])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    confirmpassword = PasswordField('Confirm\nPassword',[DataRequired(),EqualTo('password',message="Password doesn't match")])
    submit = SubmitField(label='CREATE ACCOUNT')
   
class EditCustomerForm(FlaskForm):  

    def validname(form,field):
        if not field.data.isalpha():
            raise ValidationError('Name should contain alphabets only !!!') 
        
    def valid_phone(form,field):
        if len(field.data) != 10:
            raise ValidationError(message='Invalid Phone Number !!!')
        elif not field.data.isdecimal():
            raise ValidationError(message='Invalid Phone Number !!!')

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
    
    def valid_email(form,field):
        regex = re.compile(r'''(
            [a-zA-Z0-9._%+-]+
            @
            [a-zA-Z0-9.-]+
            (\.[a-zA-Z]{2,4})
            )''',re.VERBOSE
        )
        list = regex.findall(field.data)
        if list == []:
            raise ValidationError(message='Invalid Email')
           
        

    firstname = StringField('First Name',[DataRequired(),validname])
    lastname = StringField('Last Name',[DataRequired(),validname])
    phone = StringField('Phone No',[valid_phone])
    email = EmailField('Email',[valid_email])
    username = StringField('User Name',[DataRequired()],render_kw={"readonly": True})
    submit = SubmitField(label='SAVE CHANGES')

class AddAdminForm(FlaskForm):

    def validname(form,field):
        DataList = field.data.split(' ')
        for i in DataList:
            if not i.isalpha():
                raise ValidationError('Name should contain alphabets only !!!') 
    
    def username_nottaken1(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data == rowdata[2]:
                raise ValidationError(message='UserName is Taken !!!')
        con.close()
        
    def valid_phone(form,field):
        if len(field.data) != 10:
            raise ValidationError(message='Invalid Phone Number !!!')
        elif not field.data.isdecimal():
            raise ValidationError(message='Invalid Phone Number !!!')

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
              
        

    name = StringField('Full Name',[DataRequired(),validname])
    username = StringField('User Name',[DataRequired(),username_nottaken1])
    password = PasswordField('Password',[DataRequired(),valid_pass])
    confirmpassword = PasswordField('Confirm\nPassword',[DataRequired(),EqualTo('password',message="Password doesn't match")])
    submit = SubmitField(label='CREATE ACCOUNT')

class ChangePasswordForm(FlaskForm):
    
    def user_in(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if field.data != rowdata[1]:
                count += 1
        if count == len(rows):
            raise ValidationError('UserName does not exist !!!')
        con.close()

    def valid_oldPass(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from customer")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if rowdata[1]==form.username.data:
                if rowdata[2]!=field.data:                    
                    raise ValidationError('Invalid Password !!!')        
        con.close()

    

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
            
        

    username = StringField('User Name',[DataRequired()])
    password = PasswordField('Old Password',[DataRequired(),valid_oldPass])
    newpassword = PasswordField('New Password',[DataRequired(),valid_pass])
    confirmpassword = PasswordField('Confirm\nPassword',[DataRequired(),EqualTo('newpassword',message="Password doesn't match")])
    submit = SubmitField(label='CHANGE PASSWORD')

    

class ChangeAdminPasswordForm(FlaskForm):    
   
    def validname(form,field):
        DataList = field.data.split(' ')
        for i in DataList:
            if not i.isalpha():
                raise ValidationError('Name should contain alphabets only !!!') 

    def valid_oldPass(form,field):
        con = sqlite3.connect("DBMS.db")
        print("Database successfully opened")
        cur = con.cursor()
        cur.execute("Select * from admin")
        rows = cur.fetchall()
        count = 0
        for rowdata in rows: 
            if rowdata[2]==form.username.data:
                if rowdata[3]!=field.data:                    
                    raise ValidationError('Invalid Password !!!')        
        con.close()

    

    def valid_pass(form,field):
        count = 0
        if len(field.data) >= 8:
            count += 1
        if not field.data.isalnum() and not field.data.isupper() and not field.data.islower() and not field.data.isdecimal():
            count += 1
        if count != 2:
            raise ValidationError(message='>= 8 characters, must contain \nA-Z or a-Z ,0-9 ,\na special character( !,@,#,$,%,^,&,* )')
            
        

    username = StringField('User Name',[DataRequired()],render_kw={"readonly": True})
    name = StringField('Full Name',[DataRequired(),validname])
    password = PasswordField('Old Password',[DataRequired(),valid_oldPass])
    newpassword = PasswordField('New Password',[DataRequired(),valid_pass])
    confirmpassword = PasswordField('Confirm\nPassword',[DataRequired(),EqualTo('newpassword',message="Password doesn't match")])
    submit = SubmitField(label='UPDATE PROFILE')



class ReplaceDriverForm(FlaskForm):

    def validname(form,field):
        DataList = field.data.split(' ')
        for i in DataList:
            if not i.isalpha():
                raise ValidationError('Name should contain alphabets only !!!')
    
    def validDL(form,field):
        if not field.data.isupper() or not field.data.isalnum() or field.data.isdecimal() or field.data.isalpha():
            raise ValidationError("Invalid License Number !!!") 

    def valid_phone(form,field):
        if len(field.data) != 10:
            raise ValidationError(message='Invalid Phone Number !!!')
        elif not field.data.isdecimal():
            raise ValidationError(message='Invalid Phone Number !!!')

    def validAge(form,field):
        if field.data < 18 or field.data >70:
            raise ValidationError("Age should be between 20 and 70 years")
    
    driverId = SelectField('Driver ID of the Driver to be Replaced:',[DataRequired()],choices=driverList)
    name = StringField("Driver Name : ",[DataRequired(),validname])
    DL_no = StringField("Driving License No. :",[DataRequired(),validDL])
    dph_no = StringField("Phone Number : ",[DataRequired(),valid_phone])
    age = IntegerField("Driver's Age : ",[DataRequired(),validAge]) 
    submit = SubmitField(label='REPLACE DRIVER')