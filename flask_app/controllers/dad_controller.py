from flask_app.models.dad_model import Dad
from flask_app import app, render_template, redirect, request, session, flash, bcrypt

# redirect dad to /login_reg
@app.get('/')
def redirect_dad():
    return redirect('/dads/login_reg')

# 
@app.get('/dads/login_reg')
def login_reg():
    return render_template('login_reg.html')

@app.post('/dads/register')
def register_dad():
    # check if form is valid
    if not Dad.validate_registration(request.form):
        return redirect('/dads/login_reg')

    # if the form is valid, check to see if
    # they already registered
    found_dad = Dad.find_by_email(request.form)
    if found_dad:
        flash('Email already in database. Please login.', 'email')
        return redirect('/dads/login_reg')

    # hash password (encrypt with bcrypt)
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashed
    }

    # register (save) the dad
    dad_id = Dad.save(data)

    # log the dad in and save dad's id in session
    session['dad_id'] = dad_id
    return redirect('/jokes')

@app.post('/dads/login')
def login_dad():
    # check if form is valid
    if not Dad.validate_login(request.form):
        return redirect('/dads/login_reg')

    # if the form is valid, check to see if
    # they are registered
    found_dad = Dad.find_by_email(request.form)
    if not found_dad:
        flash('Email not found, please register.', 'log_email')
        return redirect('/dads/login_reg')

    # if they did register, check if the
    # password is correct
    if not bcrypt.check_password_hash(found_dad.password, request.form['password']):
        flash('Invalid credentials. Please check your password.', 'log_password')
        return redirect('/dads/login_reg')

    # if the password is correct,
    # log them in
    session['dad_id'] = found_dad.id
    return redirect('/jokes')

@app.get('/dads/<int:dad_id>')
def one_dad(dad_id):
    data = {
        'id': dad_id
    }
    creator = Dad.find_by_id_with_jokes(data)
    return render_template('one_dad.html', creator = creator)

@app.get('/dads/logout')
def logout():
    session.clear()
    return redirect('/dads/login_reg')