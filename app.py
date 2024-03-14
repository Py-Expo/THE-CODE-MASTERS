from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from twilio.rest import Client

app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="nithya",
    password="2005",
    database="farmer"
)

mycursor = mydb.cursor()

# Create a table if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS farmers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), mobile VARCHAR(15), email VARCHAR(255), address TEXT, state VARCHAR(255), district VARCHAR(255), block VARCHAR(255), village VARCHAR(255), age INT, gender VARCHAR(10), qualification VARCHAR(255), land_holding VARCHAR(255), language VARCHAR(255), sms_mode VARCHAR(255), sector VARCHAR(255), soil_type VARCHAR(255), category VARCHAR(255), crop VARCHAR(255))")

# Twilio credentials
account_sid = 'AC47cec984684f6fcabb523a844b06dee6'
auth_token = '4af1390f28595e21e8fa2638dd70bb07'
client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        state = request.form['state']
        district = request.form['district']
        block = request.form['block']
        village = request.form['village']
        age = request.form['age']
        gender = request.form['gender']
        qualification = request.form['qualification']
        land_holding = request.form['land_holding']
        language = request.form['language']
        sms_mode = request.form['sms_mode']
        sector = request.form['sector']
        soil_type = request.form['soil_type']
        category = request.form['category']
        crop = request.form['crop']

        # Insert data into the database
        sql = "INSERT INTO farmers (name, mobile, email, address, state, district, block, village, age, gender, qualification, land_holding, language, sms_mode, sector, soil_type, category, crop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, mobile, email, address, state, district, block, village, age, gender, qualification, land_holding, language, sms_mode, sector, soil_type, category, crop)
        mycursor.execute(sql, val)
        mydb.commit()

        # Send a sample weather message
        message = ""
        client.messages.create(body=message, from_='+16149454183', to="+91"+mobile)

        return redirect(url_for('home'))

@app.route('/home')
def home():
    mycursor.execute("SELECT * FROM farmers")
    data = mycursor.fetchall()
    return render_template('home.html', farmers=data)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        # Delete record from the database
        sql = "DELETE FROM farmers WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
