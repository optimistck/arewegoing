from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import  get_request_token, get_oauth_verifier_url, get_access_token, get_event_footprint
from user import User
from database import Database
import requests
from event import Event


app = Flask(__name__)
app.secret_key = '1swfdqwsfqsqf234'

Database.initialize(host='localhost', database='iwillgoifyougo', user='postgres', password='asdf')

#we can exec the same code before each request ... use case you want to have a user object, why not pass the user, e.g., need access to user object in EVERY method

@app.before_request
def load_user():
    if 'screen_name' in session: #is there a key screen_name in session
        g.user = User.load_from_db_by_screen_name(session['screen_name'])

#this is a decorator. #when we access the '/' end point, call this method
@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    #determine if the users is already logged in
    if 'screen_name' in session:
        return redirect(url_for('event'))

    #first we need to get the request token
    request_token = get_request_token()
    session['request_token'] = request_token #session is persistent between requests via cookie. Cookie is linked to a session

    return redirect(get_oauth_verifier_url(request_token))

    #redirect the user to Twitter to confirm authorizaton.
    #then we ask the Twitter to redirect back to us
    #we need to use cookies / session in order to preserve the value of the request_token, because the request_token variable won't be available to us on retunr

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage')) #redirects to the METHOD home page.


@app.route('/auth/twitter') #http://127.0.0.1:4995/auth/twitter?oauth_token=utbuKQAAAAAA2DxrAA
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    #encountered an error here, because the database was not initialized
    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user: #then create a new one
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('event')) #user.screen_name


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)

@app.route('/event')
def event():
    return render_template('event.html', user=g.user)

@app.route('/event_confirmation')
def eventconfirmation():
    description = request.args.get('description')
    date = request.args.get('date')
    organizer_id = request.args.get('organizer_id')

    event_footprint = get_event_footprint()
    #store into the database
    event = Event(description, date, organizer_id, None, event_footprint, None)
    event.save_to_db()
    return render_template('eventconfirmation.html', user=g.user, description=description, date=date, organizer_id=organizer_id, event_footprint=event_footprint)

@app.route('/events')
def list_events():
    event = Event.load_from_db_by_organizer_id(2) #this is hardcoded
    return render_template('events.html', description=event.event_description, date=event.event_date, organizer_id=event.organizer_id, event_id=event.id)

@app.route('/showevent')
def show_event():
    #NEXT:
    #make a call to find out the name of the organizer
    #make a call to find out the event items

    event_footprint = request.args.get('event_footprint')


    event = Event.load_event_from_db_by_event_footprint(event_footprint) #this is hardcoded
    return  render_template('showevent.html', description=event.event_description, date=event.event_date, organizer_id=event.organizer_id, event_footprint=event.event_footprint, participant_id=event.participant_id)

@app.route('/search') #make dynamic
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))
    #putting the tweets into a dictionary. To get a dictionary of dictionaries. Now we're appending a dict for each tweet
    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']] #the first tweet gets the contents of the tweet for each of the tweet we circle through

    #now that it's a dictionary, need to iterate
    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        #this will retrieve the json content of the request
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content=tweet_texts)


app.run(port=4995, debug=True)