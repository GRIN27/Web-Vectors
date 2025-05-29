import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Stronger secret key for session security

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

def add_user(username, email, password):
    if User.query.filter_by(email=email).first():
        return "User with this email already exists!"
    
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return "User added successfully!"
    except Exception as e:
        db.session.rollback()
        return f"Error adding user: {str(e)}"

@app.route('/')
def home():
    return render_template("01_HomePage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        session_token = secrets.token_hex(16)

        if username == "admin" and password == "webvector":
            session["role"] = "admin"
            session["session_token"] = session_token
            return redirect(url_for("AdminUser"))  

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["role"] = "user"
            session["session_token"] = session_token
            return redirect(url_for("dashboard"))  

        return "Invalid Credentials"
    
    return render_template("02_LoginPage.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        message = add_user(username, email, password)

        if message == "User added successfully!":
            return redirect(url_for("login"))  

        return message
    return render_template("03_SignupPage.html")

@app.route('/Terms-and-Conditions')
def rules():
    return render_template("04_Terms-and-Conditions.html")

@app.route('/Attack-vectors')
def attacks():
    return render_template("05_Attack-vectors.html")

@app.route('/contact')
def contact():
    return render_template("06_Contact.html")

@app.route('/dashboard')
def dashboard():
    if "role" not in session or "session_token" not in session:
        return "Access Denied! Login first."
    return render_template("07_Dashboards.html")

@app.route('/09_Messages.html')
def messages():
    return render_template("09_Messages.html")

@app.route('/admin/user-panel')
def AdminUser():
    if "role" not in session or "session_token" not in session:
        return "Access Denied! Login first."

    if session["role"] != "admin":
        return "Access Denied!"

    users = User.query.all()  
    return render_template("08_Admin-user-panel.html", users=users)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f"File uploaded! Access it <a href='/uploads/{file.filename}'>here</a>"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='text/html')

@app.route('/view')
def view_file():
    filename = request.args.get("file", "")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    return "File not found!"

@app.route('/user/1')
def idor1():
    return "Access Denied!" 
@app.route('/user/2')
def idor2():
    return "Access Denied!" 
@app.route('/user/3')
def idor3():
    return "IDOR vulnerability.\nUsername=something&password=123456" 
@app.route('/user/4')
def idor4():
    return "Access Denied!" 

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
