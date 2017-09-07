import oauth2
import constants
import urllib.parse as urlparse
import random

# create a consumer that represents our app. It exists regarding the user existence.
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


# we shouldn't use (self) here, this method is just generating a number really, has nothing to do with the user
#get a request token should be part of a twitter connection. User only cares about the access token, not the request token
def get_request_token():
    client = oauth2.Client(consumer)

    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status != 200:
        print("An error occured getting a request token from Twitter")

    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def get_oauth_verifier(request_token):
    # www.example.com "login with twitter" -> go to twitter with our generate request token -> then they sign-in and authorize us
    # when they send us back to our site, we get the access token.
    # in our case, since there is no re-direct, Twitter will provide an access token.

    print("GO to this site:")
    print(get_oauth_verifier_url(request_token))

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oauth_verifier):
    #just an OAuth2 token
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret']) #this binds these two together (combines) in one object
    token.set_verifier(oauth_verifier)
    #now we can use the client again, but with a token too.
    client = oauth2.Client(consumer, token) #it's no longer a completely unknown client. Now we can get Access token.

    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')

    return dict(urlparse.parse_qsl(content.decode('utf-8'))) #obviously content var gets overwritten, having access token data

def get_event_footprint():
    random.seed(version=2)
    return random.randrange(10000, 999999, 1)