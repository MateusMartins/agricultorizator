from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
import json

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agro'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
    # Create cursor
    cur = mysql.connection.cursor()

    cur.execute("select mdct, sum(prcp) as prcp from agua group by mdct")

    locations = cur.fetchall()
    
    result = [[element['mdct'], element['prcp']] for element in locations]

    data = []
    prcp = []

    for x, y in result:
        data.append(x)
        prcp.append(float(y))

    if len(result) > 0:
        return render_template('home.html', prcp=json.dumps(prcp), datas=json.dumps(data))
    else:
        msg = 'Nenhuma região cadastrada'
        return render_template('home.html', msg=msg)
    # Close connection
    cur.close()

# locations
@app.route('/locations')
def locations():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get locations
    result = cur.execute("SELECT * FROM locations")

    locations = cur.fetchall()

    if result > 0:
        return render_template('locations.html', locations=locations)
    else:
        msg = 'Nenhuma região cadastrada'
        return render_template('locations.html', msg=msg)
    # Close connection
    cur.close()

#Single Location
@app.route('/location/<string:id>/')
def location(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get location
    _ = cur.execute("SELECT * FROM locations WHERE id = %s", [id])

    location = cur.fetchone()

    return render_template('location.html', location=location)

# Register Form Class
class RegisterForm(Form):
    name = StringField('Nome', [validators.Length(min=1, max=50)])
    username = StringField('Usuário', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Senha', [
        validators.DataRequired('Senha'),
        validators.EqualTo('confirm', message='Senhas não conferem')
    ])
    confirm = PasswordField('Confirme sua senha')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('Cadastro realizado com sucesso', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            name = data['name']
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['name'] = name

                flash('Login realizado com sucesso', 'success')
                return redirect(url_for('dashboard_location'))
            else:
                error = 'Problema ao validar senha'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Usuário ou senha inválido'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado, entre para acessar esta página', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Usuário deslogado com sucesso', 'success')
    return redirect(url_for('login'))

# Dashboard_location
@app.route('/dashboard_location')
@is_logged_in
def dashboard_location():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get locations
    result = cur.execute("SELECT * FROM locations")

    locations = cur.fetchall()

    if result > 0:
        return render_template('dashboard_location.html', locations=locations)
    else:
        msg = 'Nenhuma região cadastrada'
        return render_template('dashboard_location.html', msg=msg)
    
    # Close connection
    cur.close()

# Location Form Class
class LocationForm(Form):
    #state = StringField('Região', [validators.Length(min=1, max=200)])
    state = SelectField('Regiões', coerce=str)
    #descricao = TextAreaField('Descrição', [validators.Length(min=30)])

# Add Location
@app.route('/add_location', methods=['GET', 'POST'])
@is_logged_in
def add_location():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get locations
    cur.execute("select wsnm from agua group by wsnm")
    locations = cur.fetchall()

    form = LocationForm(request.form)
    form.state.choices = [(key['wsnm'], key['wsnm']) for key in locations]
    if request.method == 'POST' and form.validate():
        state = form.state.data

        # Execute
        cur.execute("INSERT INTO locations(state, descricao, author) VALUES(%s, %s, %s)",(state, 'teste', session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Location Created', 'success')

        return redirect(url_for('dashboard_location'))

    return render_template('add_location.html', form=form)


# Edit Location
@app.route('/edit_location/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_location(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get location by id
    _ = cur.execute("SELECT * FROM locations WHERE id = %s", [id])

    location = cur.fetchone()

    # Get locations
    cur.execute("select wsnm from agua group by wsnm")
    locations = cur.fetchall()

    form = LocationForm(request.form)
    form.state.choices = [(key['wsnm'], key['wsnm']) for key in locations]

    # Populate location form fields
    form.state.data = location['state']

    if request.method == 'POST' and form.validate():
        state = request.form['state']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(state)
        # Execute
        cur.execute ("UPDATE locations SET state=%s, descricao=%s WHERE id=%s",(state, 'teste', id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Região atualizada', 'success')

        return redirect(url_for('dashboard_location'))

    return render_template('edit_location.html', form=form)

# Delete Location
@app.route('/delete_location/<string:id>', methods=['POST'])
@is_logged_in
def delete_location(id):
    
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM locations WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Região deletada com sucesso', 'success')

    return redirect(url_for('dashboard_location'))


if __name__ == '__main__':
    import sys
    sys.dont_write_bytecode = True
    app.secret_key='secret123'
    app.run(debug=True)