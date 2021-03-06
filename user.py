from database import CursorFromConnectionFromPool
import oauth2
from twitter_utils import consumer
import json


class User:
	def __init__(self, screen_name, oauth_token, oauth_token_secret, id, name, email):
		self.screen_name = screen_name
		self.oauth_token = oauth_token
		self.oauth_token_secret = oauth_token_secret
		self.id = id
		self.name = name
		self.email = email

	def __repr__(self):
		return "<User {}>".format(self.screen_name)

	def save_to_db(self):
		# with connect() as connection:
		with CursorFromConnectionFromPool() as cursor:
			cursor.execute('INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
				(self.screen_name, self.oauth_token, self.oauth_token_secret))

	def save_to_db_by_email(self):
		# with connect() as connection:
		with CursorFromConnectionFromPool() as cursor:
			cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)',
				(self.name, self.email))

	def update_user_name_and_email(self):
		with CursorFromConnectionFromPool() as cursor:
			cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s',
				(self.name, self.email, self.id))

	@classmethod
	def load_from_db_by_screen_name(cls, screen_name):
		with CursorFromConnectionFromPool() as cursor:
			cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
			user_data = cursor.fetchone()
			if user_data: #if user data is not None: #so, none evals to False. So you an cut "is not None", it's assumed it's there.
				return cls(screen_name=user_data[1], oauth_token = user_data[2], oauth_token_secret = user_data[3], id=user_data[0], name=user_data[4], email=user_data[5])
			# learning point: the Python class always returns "None" as the default. So the bottom two lines are no needed
			# else:
			# 	return None
			# Also, a None object == False. If it's None, then it's False. Above executes if true.

	@classmethod
	def load_from_db_by_email(cls, email):
		with CursorFromConnectionFromPool() as cursor:
			cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
			user_data = cursor.fetchone()
			if user_data:
				return cls(screen_name=user_data[1], oauth_token = user_data[2], oauth_token_secret = user_data[3], id=user_data[0], name=user_data[4], email=user_data[5])

	def twitter_request(self, uri, verb='GET'):
		# Now, create an "authorized token" Token object and use that to perform Twitter API calls on behalf of the user
		authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
		authorized_client = oauth2.Client(consumer, authorized_token)

		# make Twitter API calls
		response, content = authorized_client.request(uri, verb)

		if response.status != 200:
			print("error")

		return json.loads(content)





