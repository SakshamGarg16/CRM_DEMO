from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
from firebase_config import firebase_config

app = Flask(__name__)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

app.secret_key = 'sjkvbkadvna_122'


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/clients')
def clients():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        user_token = session['user']
        user_info = auth.get_account_info(user_token)
        user_id = user_info['users'][0]['localId']

        clients_ref = db.child("clients").child(user_id).get(user_token)
        clients_data = []
        if clients_ref.each():
            for client in clients_ref.each():
                client_data = client.val()
                client_data['key'] = client.key()  # Needed for delete
                clients_data.append(client_data)

        return render_template('clients.html', clients=clients_data)
    except Exception as e:
        print("Get clients error:", e)
        return "Failed to load clients"

@app.route('/delete_client/<client_id>', methods=['POST'])
def delete_client(client_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        user_token = session['user']
        user_info = auth.get_account_info(user_token)
        user_id = user_info['users'][0]['localId']

        db.child("clients").child(user_id).child(client_id).remove(user_token)
        return redirect(url_for('clients'))
    except Exception as e:
        print("Delete client error:", e)
        return "Failed to delete client"


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        try:
            user_token = session['user']
            user_info = auth.get_account_info(user_token)
            user_id = user_info['users'][0]['localId']
            
            db.child("clients").child(user_id).push({
                "name": name,
                "email": email,
                "phone": phone
            }, user_token)

            return redirect(url_for('clients'))
        except Exception as e:
            print("Add client error:", e)
            return "Failed to add client"

    return render_template('add_client.html')  # for GET request



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user['idToken']  # Save login session
            return redirect(url_for('clients'))  # Redirect to clients/dashboard
        except Exception as e:
            print("Signup error:", e)
            return render_template('signup.html', error="Signup failed. Try again.")
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect(url_for('clients'))
        except Exception as e:
            return str(e)
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)
