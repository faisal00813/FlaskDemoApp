import os
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify
import sqlite3
from contextlib import closing

app= Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'bookings.db'),
    DEBUG=True,
    SECRET_KEY='faisal',
    USERNAME='admin',
    PASSWORD='admin'
))


@app.route('/')
def hello_world():
    return 'Driver booking app!'
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
	conn= sqlite3.connect(app.config['DATABASE']) 
	conn.row_factory =  dict_factory
	return conn
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.route('/driver/<id>', methods=['GET'])
def get_driver(id):
	db=get_db()
	cur = db.execute('select id,name as name,phone,vehicleno from driver where id=?',id)
	driver = cur.fetchall()
	print driver
	return jsonify(results=driver)

@app.route('/driver/<id>', methods=['DELETE','PUT'])
@app.route('/drivers', methods=['GET', 'POST'])
def add_driver(id=0):
	db=get_db()
	drivers=[]
	if request.method=='DELETE' and int(id)>0:
		db.execute('delete from driver  where id=?', id)
		db.commit()
		drivers = [dict(isSuccess = 'true')]
	if 	request.method=='PUT' and int(id)>0:
		print request.form
		db.execute('update driver set name = ? , phone=? , vehicleno=? where id=?',[request.form['name'], request.form['phone'], request.form['vehicleno'], id])
		db.commit()
		cur = db.execute('select * from driver where id =? ',id)
		drivers = cur.fetchall()
			
	if request.method=='POST':
		db.execute('insert into driver (name, phone, vehicleno) values (?, ?,?)',[request.form['name'], request.form['phone'], request.form['vehicleno']])
		db.commit()
		cur = db.execute('select * from driver order by id desc limit 1')
		drivers = cur.fetchall()
	if request.method=='GET':
		cur = db.execute('select * from driver order by id desc')
		drivers = cur.fetchall()	
	# print drivers
	return jsonify(results=drivers)
#####Bookings section
@app.route('/booking/<id>', methods=['GET'])
def get_booking(id):
	db=get_db()
	cur = db.execute('select id,name,phone,startlocation,endlocation from booking where id=?',id)
	booking = cur.fetchall()
	print booking
	return jsonify(results=booking)

@app.route('/booking/<id>', methods=['DELETE','PUT'])
@app.route('/bookings', methods=['GET', 'POST'])
def crud_bookings(id=0):
	db=get_db()
	bookings=[]
	if request.method=='DELETE' and int(id)>0:
		db.execute('delete from booking  where id=?', id)
		db.commit()
		bookings = [dict(isSuccess = 'true')]
	if 	request.method=='PUT' and int(id)>0:
		print request.form
		db.execute('update booking set name = ? , phone=? , startlocation=? , endlocation=? where id=?',[request.form['name'], request.form['phone'], request.form['startlocation'],request.form['endlocation'], id])
		db.commit()
		cur = db.execute('select * from booking where id =? ',id)
		bookings = cur.fetchall()
			
	if request.method=='POST':
		db.execute('insert into booking (name, phone, startlocation,endlocation) values (?, ?,?,?)',[request.form['name'], request.form['phone'], request.form['startlocation'],request.form['endlocation']])
		db.commit()
		cur = db.execute('select * from booking order by id desc limit 1')
		bookings = cur.fetchall()
	if request.method=='GET':
		cur = db.execute('select * from booking order by id desc')
		bookings = cur.fetchall()	
	# print bookings
	return jsonify(results=bookings)

###Asignments
@app.route('/assign', methods=['POST'])
def set_assignment():
	db=get_db()
	db.execute('update booking set driver = ? where id=?',[request.form['driverid'], request.form['bookingid']])
	db.commit()
	cur = db.execute('select * from booking where id = ?',request.form['bookingid'])
	bookings = cur.fetchall()
	print bookings
	return jsonify(results=bookings)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__=='__main__':
	app.run()

