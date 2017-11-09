from flask import Flask, render_template, session, redirect, request, url_for, g, flash
from twitter_utils import  get_request_token, get_oauth_verifier_url, get_access_token, get_event_footprint
from user import User
from database import Database
import requests
from event import Event
from participation import Participation
from datetime import datetime
import constants
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from oauth import OAuthSignIn
import logging

app = Flask(__name__)
app.secret_key = '1swfdqwsfqsqf234'
app_url = constants.APPLICATION_URL
Database.initialize(host='localhost', database='iwillgoifyougo', user='postgres', password='asdf')
#Database.initialize(host='35.196.51.49', database='arewegoing1', user='ck', password='##############')


## NEW ##

app.config['SECRET_KEY'] = 'top secret!'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '154318681832470',
        'secret': '47e8759336b6881ad3b15f92004bfd65'
    },
    'twitter': {
        'id': '---',
        'secret': '---'
    }
}



## NEW ##
lm = LoginManager(app)
lm.login_view = 'login'


# @lm.user_loader
# def load_user(id):
#     return User.query.get(int(id))

#we can exec the same code before each request ... use case you want to have a user object, why not pass the user, e.g., need access to user object in EVERY method

@app.before_request
def load_user():
    g.user = None
    if 'screen_name' in session: #is there a key screen_name in session
        g.user = User.load_from_db_by_screen_name(session['screen_name'])

#this is a decorator. #when we access the '/' end point, call this method
@app.route('/')
def homepage():
    if not g.user:
        return redirect(url_for('start'))
    return render_template('home.html')

@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/login/twitter')
def twitter_login():
    logout()
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
    return redirect(url_for('homepage'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if g.user:
        #return render_template('msg.html', message="Not logged in (not g.user).")
        return redirect(url_for('homepage'))
    oauth = OAuthSignIn.get_provider(provider)
    #return render_template('msg.html', message="Logged in yes. g.user.")
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if g.user:
        #return render_template('msg.html', message="Not logged in (not g.user).")
        return redirect(url_for('homepage'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        print("AUTH FAILED")
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        print("DOING SOMETHING")
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))



@app.route('/auth/twitter') #http://127.0.0.1:4995/auth/twitter?oauth_token=utbuKQAAAAAA2DxrAA
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    #encountered an error here, because the database was not initialized
    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user: #then create a new one
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None, None, None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('event')) #user.screen_name

#TODO remove this
@app.route('/profile')
def profile():
    if not g.user:
        return render_template('msg.html', message="Please login to post an activity.")
    return render_template('profile.html', user=g.user)

@app.route('/event')
def event():
    if not g.user:
        return render_template('msg.html', message="Please login to post an activity.")
    return render_template('event.html', user=g.user)

@app.route('/event_confirmation')
def eventconfirmation():
    if not g.user:
        return render_template('msg.html', message="Please login to create an event.")
    description = request.args.get('description')
    date = request.args.get('date')
    min_participants = request.args.get('min_participants')
    organizer_id = g.user.id
    event_footprint = get_event_footprint()
    #store into the database
    event = Event(description, date, organizer_id, event_footprint, None, min_participants, 0)
    event.save_to_db()

    name_email_status = "Hello world"
    if (g.user.email == None) or (g.user.name == None):
        name_email_status = None
    return render_template('eventconfirmation.html', user=g.user, description=description, date=date, organizer_id=organizer_id, event_footprint=event_footprint, min_participants=min_participants, name_email_status=name_email_status, app_url=app_url)


#TODO this one is OK (check) to join event without being signed in
@app.route('/join_event')
def joinevent():
    name = request.args.get('person_name')
    email = request.args.get('email')
    if g.user:
        if (g.user.email == None) or (g.user.name == None):
            user = User(g.user.screen_name, g.user.oauth_token, g.user.oauth_token_secret, g.user.id, name, email)
            user.update_user_name_and_email()

        #update the profile email and password if doesn't exist.
        #if the email and name not filled out, fill it out. Else, pre-fill it.

    if not g.user:
        #do stuff to make an entry and confirm without the login in. And then add login info.
        #do create user.
        user = User(None, None, None, None, name, email)
        user.save_to_db_by_email()
        g.user = User.load_from_db_by_email(email)
        #return render_template('msg.html', message="User based on email created successfully")
    event_id = request.args.get('event_id')
    participant_id = g.user.id
    participation = Participation(event_id=event_id, participant_id=participant_id, joined_date=None, id=None)
    participation.save_to_db()
    event = Event.load_event_from_db_by_event_id(event_id)
    Event.add_one_to_event(event_id)
    return render_template('joinconfirmation.html', name=name, description=str(event.event_description[0]), date=str(event.event_date[0]), event_id=event.id)

@app.route('/bailout')
def bailfromevent():
    if not g.user:
        return render_template('msg.html', message="Please login to bail out of activity.")
    event_id = request.args.get('event_id')
    participant_id = g.user.id
    bailout_result = Participation.delete_participant_from_event(int(participant_id), int(event_id))
    Event.minus_one_from_event(event_id)
    return render_template('confirmation.html', user=g.user, message="You bailed out of the activity. Why not create your own event?")

@app.route('/cancelevent')
def cancelevent():
    if not g.user:
        return render_template('msg.html', message="Please login to cancel an event.")
    event_id = request.args.get('event_id')
    participant_id = g.user.id
    cancel_result = Event.delete_event(event_id, participant_id)
    return render_template('confirmation.html', user=g.user, message="You cancelled the activity. There is no undo, but you can create a new event.")

@app.route('/canceleventwithafoot')
def canceleventwithafootprint():
    if not g.user:
        return render_template('msg.html', message="Please login to cancel an event.")
    event_footprint = request.args.get('event_footprint')
    event_id = Event.get_event_id_from_event_footprint(event_footprint)
    participant_id = g.user.id
    cancel_result = Event.delete_event(event_id[0], participant_id)
    return render_template('confirmation.html', user=g.user, message="You cancelled the activity. There is no undo, but you can create a new event.")

#TODO: delete this?
@app.route('/events_old')
def list_events_old():
    if not g.user:
        return render_template('msg.html', message="Please login to cancel an event.")
    event = Event.load_from_db_by_organizer_id(int(g.user.id))
    if event != None:
        participants = Participation.load_event_participant_names(event.id)
    else:
        return render_template('events.html', message="No events found")
    return render_template('events.html', description=event.event_description, date=event.event_date, organizer_id=event.organizer_id, event_id=event.id, participants=participants)

@app.route('/events')
def list_events():
    if not g.user:
        return render_template('msg.html', message="Please login to see events.")
    # we want to show the events where the users is the organizer and events where the user is the participant.
    events = Event.load_from_db_all_events_by_organizer_id(int(g.user.id))
    event_participant = Participation.load_participating_in_events(int(g.user.id))

    if events == None and event_participant == None:
        return render_template('events.html', message="noeventsfound")
    elif events == None and event_participant != None:
        return render_template('events.html', participant=event_participant, message="participantonly")
    elif event_participant == None and events != None:
        return render_template('events.html', events=events, message="organizeronly")
    else:
        return render_template('events.html', events=events, participant=event_participant, message="participantandorganizer")

#TODO: remove before going live
@app.route('/workbench')
def workbench_list_all_events():
    #list all the events regardless whether a user has the right to see it or not
    participants = "None - hardcoded"
    events = Event.workbench_load_all_events()
    event_data = [{'event_id': event[0], 'description': event[1], 'date': event[2], 'organizer_id': event[3], 'event_footprint': event[4]} for event in events]
    if event != None:
        participants = "None - hardcoded 2"
        #participants = Participation.load_event_participant_names(event.id)
    else:
        return render_template('workbench.html', message="No events found")
    #return render_template('workbench.html', description=event.event_description, date=event.event_date, organizer_id=event.organizer_id, event_id=event.id, participants=participants)
    return render_template('workbench.html', events=events)


@app.route('/to')
def show_event():
    name = None
    email = None
    if g.user:
        name = g.user.name
        email = g.user.email
    event_footprint = request.args.get('this')
    event = Event.load_event_from_db_by_event_footprint(event_footprint)
    return  render_template('showevent.html', description=str(event.event_description[0]), date=str(event.event_date[0]), event_id=str(event.id[0]), name=name, email=email)

@app.route('/eventdetails')
def eventdetails(helper_event_footprint=None):
    if not g.user:
        return render_template('msg.html', message="Please login to see event participants.")
    if helper_event_footprint != None:
        event_footprint = helper_event_footprint
    else:
        event_footprint = request.args.get('this')
    event = Event.load_event_from_db_by_event_footprint(event_footprint)
    event_id = Event.get_event_id_from_event_footprint(event_footprint)
    participants = Participation.load_event_participant_names(event_id[0])
    return render_template('eventdetails.html', description=str(event.event_description[0]), date=str(event.event_date[0]), event_id=event.id, event_footprint=event_footprint, participants=participants, min_participants=event.min_participants[0], participants_count=event.participants_count, app_url=app_url)

@app.route('/add_name_email')
def add_name_email():
    name = request.args.get('name')
    email = request.args.get('email')
    event_footprint = request.args.get('this')

    if g.user:
        if (g.user.email == None) or (g.user.name == None):
            user = User(g.user.screen_name, g.user.oauth_token, g.user.oauth_token_secret, g.user.id, name, email)
            user.update_user_name_and_email()

    return eventdetails(event_footprint)


#TODO remove before going live
@app.route('/search') #make dynamic
def search():
    if not g.user:
        return render_template('msg.html', message="Please login to perform a search.")
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


@app.route('/about')
def about():
    return render_template('about.html')

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')

#TODO remove before going live
@app.route('/t')
def tester():
    return render_template('tester.html', user="FakeTestUser")

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=4995, debug=True)
# [END app]


#app.run(port=4995, debug=True)