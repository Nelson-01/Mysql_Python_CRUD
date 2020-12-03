from flask import Flask
from flask import jsonify
from flask import request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'api'

mysql = MySQL(app)


@app.route("/",methods=['GET'])
def all():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from empdb")   
    output = cursor.fetchall()
    for i in output: 
        print(i)       
    cursor.close()
    return ({"empdb":output})

@app.route("/create", methods=['POST'])
def create():
    empcode = request.json['empcode']
    name = request.json['name']
    cursor = mysql.connection.cursor()
    cursor.execute(''' INSERT INTO empdb VALUES(%s,%s)''',(empcode,name))
    cursor.execute("select empcode,name from empdb")
    mysql.connection.commit()
    output = cursor.fetchall()
    cursor.close()
    return jsonify({"empdb_Create":output})

@app.route("/read/<empcode>",methods=['GET'])
def getemployee(empcode):
    cursor = mysql.connection.cursor()
    empDB = cursor.execute("select * from empdb where empcode = %s", empcode)
    mysql.connection.commit()
    output = cursor.fetchall()    
    cursor.close()
    return jsonify({"empdb_Read":output})

@app.route("/update/<empcode>", methods=['PUT'])
def update(empcode):
    name = request.json['name']
    cursor = mysql.connection.cursor()
    cursor.execute("update empdb set name= %s where empcode = %s", (name,empcode))
    mysql.connection.commit()
    cursor.execute("select * from empdb")
    output = cursor.fetchall()    
    cursor.close()
    return jsonify({"empdb_Update":output})
 
@app.route("/delete/<empcode>", methods=['DELETE'])
def delete(empcode):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from empdb where empcode = %s",empcode)
    mysql.connection.commit()
    cursor.execute("select * from empdb")
    output = cursor.fetchall()    
    cursor.close()
    return jsonify({"empdb_Delete":output})

if __name__ == "__main__":
    app.run(debug=True,port='5000')