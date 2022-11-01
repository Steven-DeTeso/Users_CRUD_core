import re
from flask import Flask, render_template, request, redirect, session # type: ignore
from users import User
app = Flask(__name__)
app.secret_key = "ABCD1234"

# immediately redirects to the home page when just '/' is called
@app.route('/')
def read():
    return redirect('/home')

# renders read.html and passes the User classmethod getall() to be displayed in the table
@app.route('/home')
def home():
    return render_template('read.html', users = User.get_all())

# renders the create form html page
@app.route('/home/create')
def create():
    return render_template('/create.html')

# listens on the /home/show which is the forms action on the create.html page, because its a form it also listens for the method=['POST] AND accepts it here under methods=['POST'], note the extra s on methods here in the listener. It takes in the info as data in the form of 'request.form' and that is injected into User class method save(); that triggers the query to add it to the database (see users.py)
# - we NEVER render on a 'POST' so we redirect home which again calls the get_all(). 
@app.route('/home/show', methods=['POST'])
def r_show():
    if not User.validate_user(request.form):
        return redirect('/home/create')
    print(request.form)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    # session['id'] = request.form['id']
    User.save(request.form)
    return redirect('/home')

@app.route('/user/<int:id>')
def r_one_user(id):
    data = {
        'id': id
    }
    return render_template('edit.html', user=User.get_one(data))

@app.route('/user/show/<int:id>')
def show(id):
    data = {
        'id': id
    }
    return render_template('read_one.html', user=User.get_one(data))

@app.route('/user/update', methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/home')

@app.route('/user/destroy/<int:id>')
def destroy(id):
    data = {
        'id': id
    }
    User.destroy(data)
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True)