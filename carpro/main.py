from flask import Flask, render_template, request, url_for, redirect, flash, session, Response
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import mysql.connector
import os
import pdfkit
from flaskext.mysql import MySQL
import pymysql
from fpdf import FPDF

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

app = Flask(__name__)

sql = MySQL()

conn = mysql.connector.connect(
    host="localhost", user="Nithin", password="NITHIN1141121", database="user")
cursor = conn.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['MYSQL_DATABASE_USER'] = 'Nithin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'NITHIN1141121'
app.config['MYSQL_DATABASE_DB'] = 'user'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


sql.init_app(app)
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)




class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Subject = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Checkout(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.String(80), nullable=False)
    to_date = db.Column(db.String(20), nullable=False)
    From_time = db.Column(db.String(50), nullable=False)
    to_time = db.Column(db.String(120), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    vechiles = db.Column(db.String(50), nullable=False)
    Payments = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Cancled(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    from_date = db.Column(db.String(80), nullable=False)
    From_time = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    vechiles = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Subscribe(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Register(db.Model):
    id_no = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    confirm_password = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)




class Login(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    return render_template('home.html', params=params)


@app.route("/subscribehome", methods=['GET', 'POST'])
def subscribehome():
    if (request.method == 'POST'):
        email = request.form.get('email')
        entry = Subscribe(email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('home.html', params=params)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        if (email == params['admin_email'] and password == params['admin_password']):
            session['email'] = email
            print(session)
            return redirect(url_for('all_checkout_json_data'))

        else:
            return render_template('adminlogin.html')
    return render_template('adminlogin.html')


@app.route('/adminlogout')
def adminlogout():
    session.pop('email')
    return redirect(url_for('adminlogin'))



@app.route("/printAallcheck", methods=['GET', 'POST'])
def printAallcheck():
    conn = None
    cursor = None
    try:
        conn = sql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""SELECT * FROM `cancled` """)
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times', 'B', 14)
        pdf.cell(page_width, 0.0, 'Checkout', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 9)

        col_width = page_width/4

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['sno']), border=1)
            pdf.cell(col_width, th, str(row['from_date']), border=1)
            pdf.cell(col_width, th, str(row['Email']), border=1)
            pdf.cell(col_width, th, str(row['vechiles']), border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)
        pdf.cell(page_width, 0.0, '-end of report-', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=check_report.pdf'})


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()









@app.route("/Aallcheck")
def Aallcheck():
    return render_template('Aallcheck.html', params=params)


@app.route("/Aallcontacts", methods=['GET', 'POST'])
def Aallcontacts():
    return render_template('Aallcontacts.html', params=params)

@app.route("/printAallcontacts", methods=['GET', 'POST'])
def printAallcontacts():
    conn = None
    cursor = None
    try:
        conn = sql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""SELECT * FROM `contacts` """)
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times', 'B', 14)
        pdf.cell(page_width, 0.0, 'contacts', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 9)

        col_width = page_width/4

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['sno']), border=1)
            pdf.cell(col_width, th, str(row['Name']), border=1)
            pdf.cell(col_width, th, str(row['Email']), border=1)
            pdf.cell(col_width, th, str(row['date']), border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)
        pdf.cell(page_width, 0.0, '-end of report-', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=contacts_report.pdf'})


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()




@app.route("/Aallregister", methods=['GET', 'POST'])
def Aallregister():
    return render_template('Aallregister.html', params=params)

@app.route("/printAallregister", methods=['GET', 'POST'])
def printAallregister():
    conn = None
    cursor = None
    try:
        conn = sql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""SELECT * FROM `register` """)
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times', 'B', 14)
        pdf.cell(page_width, 0.0, 'register', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 9)

        col_width = page_width/4

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['id_no']), border=1)
            pdf.cell(col_width, th, str(row['username']), border=1)
            pdf.cell(col_width, th, str(row['email']), border=1)
            pdf.cell(col_width, th, str(row['gender']), border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)
        pdf.cell(page_width, 0.0, '-end of report-', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=reg_report.pdf'})


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.route("/Aallsubscribe", methods=['GET', 'POST'])
def Aallsubscribe():
    return render_template('Aallsubscribe.html', params=params)



@app.route("/printAallsubscribe", methods=['GET', 'POST'])
def printAallsubscriber():
    conn = None
    cursor = None
    try:
        conn = sql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""SELECT * FROM `subscribe` """)
        result = cursor.fetchall()

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin
        pdf.set_font('Times', 'B', 14)
        pdf.cell(page_width, 0.0, 'subscribe', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 9)

        col_width = page_width/3

        pdf.ln(1)

        th = pdf.font_size

        for row in result:
            pdf.cell(col_width, th, str(row['sno']), border=1)
            pdf.cell(col_width, th, str(row['email']), border=1)
            pdf.cell(col_width, th, str(row['date']), border=1)
            pdf.ln(th)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)
        pdf.cell(page_width, 0.0, '-end of report-', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=subscribe_report.pdf'})


    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.route("/homecontact", methods=['GET', 'POST'])
def homecontact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(Name=name, Email=email, Subject=subject,
                         Message=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('homecontact.html', params=params)


@app.route("/homeabout")
def homeabout():
    return render_template('homeabout.html', params=params)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == 'POST'):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        gender = request.form.get('gender')
        cursor.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' """
                       .format(email))
        register = cursor.fetchall()
        if len(register) > 0:
            flash("email already exists")
            return render_template('register.html')
        elif password == confirm:
            entry = Register(username=username, email=email, password=password,
                             confirm_password=confirm, gender=gender, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            flash("you have registered")
            return redirect(url_for('login'))
        else:
            flash("password does not match")
            return render_template('register.html')
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route("/login_validation", methods=['GET', 'POST'])
def login_validation():
    if (request.method == 'POST'):
        session.pop('email', None)
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                       .format(email, password))
        register = cursor.fetchall()
        if len(register) > 0:
            print(register[0][1])
            session['sno'] = register[0][0]
            session['username'] = register[0][1]
            session['email'] = register[0][2]
            entry = Login(email=email, password=password, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('userlogin'))
            # return render_template('userlogin.html', name=session['email'])
        else:
            flash("email or password is incorrect")
            return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route("/forgot", methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')


@app.route("/forgot_validation", methods=['GET', 'POST'])
def forgot_validation():
    if (request.method == 'POST'):
        email = request.form.get('email')
        post = Register.query.filter_by(email=email).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('reset'))

@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if (request.method == 'POST'):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        gender = request.form.get('gender')
        cursor.execute("""SELECT * FROM `register` WHERE `email` LIKE '{}' """
                       .format(email))
        register = cursor.fetchall()
        if len(register) > 0:
            flash("email already exists")
            return render_template('reset.html')
        elif password == confirm:
            entry = Register(username=username, email=email, password=password,
                             confirm_password=confirm, gender=gender, date=datetime.now())
            db.session.add(entry)
            db.session.commit()
            flash("you have reset successfully")
            return redirect(url_for('login'))
        else:
            flash("password does not match")
            return render_template('reset.html')
    return render_template('reset.html')





@app.route("/userlogin")
def userlogin():
    if 'sno' in session:
        return render_template('userlogin.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/subscribe", methods=['POST'])
def subscribe():
    if (request.method == 'POST'):
        email = request.form.get('email')
        entry = Subscribe(email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('userlogin.html', params=params, logged_in_user=session['username'])


@app.route("/vehicles")
def vehicles():
    if 'sno' in session:
        return render_template('vehicles.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/vehiclescheckout", methods=['GET', 'POST'])
def vehiclescheckout():
    if (request.method == 'POST'):
        From = request.form.get('From')
        To = request.form.get('To')
        Start = request.form.get('Start')
        End = request.form.get('End')
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        paymentMethod = request.form.get('paymentMethod')
        if Start == End:
            flash("same time can't be given")
            return render_template('vehiclescheckout.html', params=params)

        else:
            entry = Checkout(from_date=From, to_date=To, From_time=Start, to_time=End, Email=email, vechiles=user_type,
                             Payments=paymentMethod, date=datetime.now())
            double = Cancled(from_date=From, From_time=Start,
                             Email=email, vechiles=user_type, date=datetime.now())
            db.session.add(entry)
            db.session.add(double)
            db.session.commit()
            flash("Rented successful")
    return render_template('vehiclescheckout.html', params=params)


@app.route("/services")
def services():
    if 'sno' in session:
        return render_template('services.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/featured")
def featured():
    if 'sno' in session:
        return render_template('featured.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/featuredcheckout", methods=['GET', 'POST'])
def featuredcheckout():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        From = request.form.get('From')
        To = request.form.get('To')
        Start = request.form.get('Start')
        End = request.form.get('End')
        email = request.form.get('email')
        user_type = request.form.get('user_type')
        paymentMethod = request.form.get('paymentMethod')
        entry = Checkout(from_date=From, to_date=To, From_time=Start, to_time=End, Email=email, vechiles=user_type,
                         Payments=paymentMethod, date=datetime.now())
        double = Cancled(from_date=From, From_time=Start,
                         Email=email, vechiles=user_type, date=datetime.now())
        db.session.add(entry)
        db.session.add(double)
        db.session.commit()
        flash("Rented successful")
    return render_template('featuredcheckout.html', params=params)


@app.route("/reviews")
def reviews():
    if 'sno' in session:
        return render_template('reviews.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if 'sno' in session:
        if (request.method == 'POST'):
            '''Add entry to the database'''
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            entry = Contacts(Name=name, Email=email, Subject=subject,
                             Message=message, date=datetime.now())
            db.session.add(entry)
            db.session.commit()

        return render_template('contact.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route("/aboutus")
def aboutus():
    if 'sno' in session:
        return render_template('aboutus.html', params=params, logged_in_user=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/checkout_json_data', methods=['GET', 'POST'])
def checkout_json_data():
    checkout = []
    current_user = session['email']
    cursor.execute("""SELECT * FROM `checkout` WHERE `Email` LIKE '{}' """
                   .format(current_user))
    checkout_data = cursor.fetchall()

    for i in checkout_data:
        checkout.append(i)
    return render_template('booking.html', params=params, checkoutdata=checkout, logged_in_user=session['username'])


@app.route('/all_checkout_json_data', methods=['GET', 'POST'])
def all_checkout_json_data():
    cursor.execute("""SELECT * FROM `cancled` """)
    all_checkout_data = cursor.fetchall()
    all_checkout = []
    for i in all_checkout_data:
        all_checkout.append(i)
    return render_template('Aallcheck.html', params=params, checkout=all_checkout)


@app.route('/all_contacts_json_data', methods=['GET', 'POST'])
def all_contacts_json_data():
    cursor.execute("""SELECT * FROM `contacts` """)
    all_checkout_data = cursor.fetchall()
    all_checkout = []
    for i in all_checkout_data:
        all_checkout.append(i)
    return render_template('Aallcontacts.html', params=params, checkout=all_checkout)


@app.route('/all_register_json_data', methods=['GET', 'POST'])
def all_register_json_data():
    cursor.execute("""SELECT * FROM `register` """)
    all_checkout_data = cursor.fetchall()
    all_checkout = []
    for i in all_checkout_data:
        all_checkout.append(i)
    return render_template('Aallregister.html', params=params, checkout=all_checkout)


@app.route('/all_subscribe_json_data', methods=['GET', 'POST'])
def all_subscribe_json_data():
    cursor.execute("""SELECT * FROM `subscribe` """)
    all_checkout_data = cursor.fetchall()
    all_checkout = []
    for i in all_checkout_data:
        all_checkout.append(i)
    return render_template('Aallsubscribe.html', params=params, checkout=all_checkout)


@app.route('/logout')
def logout():
    session.pop('sno')
    return redirect(url_for('login'))


@app.route('/delete/<string:sno>', methods=['GET', 'POST'])
def delete(sno):
    if 'sno' in session:
        post = Checkout.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        print(post)
    return redirect('/checkout_json_data')

@app.route("/edit")
def edit():
        return render_template('edit.html', params=params, logged_in_user=session['username'])

@app.route('/editBookingDataFetch/<string:sno>', methods=['GET', 'POST'])
def editBookingDataFetch(sno):
    cursor.execute("""SELECT * FROM `checkout` WHERE `sno` LIKE '{}' """
                   .format(sno))
    booking_data_to_be_edited = cursor.fetchall()
    return render_template('edit.html', params=params, editDataFetch=booking_data_to_be_edited)

@app.route('/editBookingData/<string:sno>', methods=['GET', 'POST'])
def editBookingData(sno):
    if (request.method == 'POST'):
        from_date = request.form.get('From')
        to_date = request.form.get('To')
        from_time = request.form.get('Start')
        to_time = request.form.get('End')
    if from_time == to_time:
        flash("same time can't be given")
        cursor.execute("""SELECT * FROM `checkout` WHERE `sno` LIKE '{}' """
                       .format(sno))
        booking_data_to_be_edited = cursor.fetchall()
        return render_template('edit.html', params=params, editDataFetch=booking_data_to_be_edited)
        #flash("same time can't be given")
        #return redirect('/edit')
    else:
        cursor.execute("""
                    UPDATE checkout
                    SET from_date = %s,
                        to_date = %s,
                        from_time = %s,
                        to_time = %s
                    WHERE sno = %s
                """, (from_date, to_date, from_time, to_time, sno))
    #booking_data_to_be_edited = cursor.fetchall()
    return redirect('/checkout_json_data')

@app.route('/all_check_delete/<string:sno>', methods=['GET', 'POST'])
def all_check_delete(sno):
    post = Cancled.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/all_checkout_json_data')


@app.route('/all_contact_delete/<string:sno>', methods=['GET', 'POST'])
def all_contact_delete(sno):
    post = Contacts.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/all_contacts_json_data')


@app.route('/all_register_delete/<string:sno>', methods=['GET', 'POST'])
def all_register_delete(sno):
    post = Register.query.filter_by(id_no=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/all_register_json_data')


@app.route('/all_subscribe_delete/<string:sno>', methods=['GET', 'POST'])
def all_subscribe_delete(sno):
    post = Subscribe.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/all_subscribe_json_data')


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
