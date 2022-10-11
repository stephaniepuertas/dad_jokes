
from flask_app import app, render_template, redirect, request, session
from flask_app.models.dad_model import Dad
from flask_app.models.joke_model import Joke

@app.get('/jokes')
def all_jokes():
    data = {
        'id': session['dad_id']
    }
    dad = Dad.find_by_id(data)
    #need to create data whenever you are grabbing data from session
    jokes = Joke.find_all()
    return render_template('all_jokes.html', dad = dad, jokes = jokes)

@app.get('/jokes/new')
def new_joke():
    return render_template('new_joke.html')

@app.post('/jokes')
def create_joke():
    if not Joke.validate_joke(request.form):
        return redirect('/jokes/new')
        #if valid we save 
    Joke.save(request.form)
    return redirect('/jokes')