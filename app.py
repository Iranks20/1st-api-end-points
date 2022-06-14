from ctypes.wintypes import MSG
from email import message
import json
import pymysql
from flask import jsonify, request
from flaskext.mysql import MySQL
from flask import Flask
from flask_mail import Mail,Message
from random import *

c_app = Flask(__name__)
mail=Mail(c_app)


c_app.config["MAIL_SERVER"]='smtp.gmail.com'
c_app.config["MAIL_PORT"]=465
c_app.config["MAIL_USERNAME"]='******@gmail.com'
c_app.config['MAIL_PASSWORD']='************'                    #you have to give your password of gmail account
c_app.config['MAIL_USE_TLS']=False
c_app.config['MAIL_USE_SSL']=True
mail=Mail(c_app)
otp=randint(000000,999999)




mysql = MySQL()
c_app.config['MYSQL_DATABASE_USER']='root'
c_app.config['MYSQL_DATABASE_PASSWORD']=''
c_app.config['MYSQL_DATABASE_DB']='practice'
c_app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(c_app)


@c_app.route('/create', methods=['POST'])
def create_student():
    try:        
        data = request.json
        _id = data['id']
        _name = data['name']
        _email = data['email']
        _address = data['address']
        msg=Message(subject='OTP',sender='irankundainnocent673@gmail.com',recipients=['rankunda48@gmail.com'])
        msg.body=str(otp)
        mail.send(msg)
        response = jsonify('OTP SENT TO YOUR EMAIL')
        response.status_code = 200
        #return response

        if request.method == 'POST':
            bindData = (_id, _name, _email, _address)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO student(id, name, email, address) VALUES(%s, %s, %s, %s)""", bindData)
            conn.commit()
            respone = jsonify('studentinfo added successfully!')
            respone.status_code = 200
            return respone
        else:
            return {'error': 'it has failed'}
    except Exception as e:
        print(e)
        return jsonify(str(e))         
     
@c_app.route('/student', methods=['GET'])
def student():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM student")
        studentRows = cursor.fetchall()
        respone = jsonify(studentRows)
        respone.status_code = 200
    except Exception as e:
        print(e)
        respone = str(e)
    finally:
        cursor.close() 
        conn.close()
        return respone  

#@c_app.route('/student/')
#def student_details(student_id):
    #try:
        #conn = mysql.connect()
        #cursor = conn.cursor(pymysql.cursors.DictCursor)
        #cursor.execute("SELECT id, name, email, address FROM student WHERE id =%s", student_id)
        #studentRow = cursor.fetchone()
        #respone.status_code = 200
        #return respone
    #except Exception as e:
        #print(e)
    #finally:
        #cursor.close() 
        #conn.close() 

@c_app.route('/update', methods=['PUT'])
def update_student():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _address = _json['address']
        if _name and _email and _address and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE student SET name=%s, email=%s, address=%s WHERE id=%s"
            bindData = (_name, _email, _address, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('studentinfo updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@c_app.route('/delete/<string:id>', methods=['DELETE'])
def delete_student(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM student WHERE id =%s", (id,)) 
		conn.commit()
		respone = jsonify('studen deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close() 

       
@c_app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    c_app.run()