import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from dotenv import load_dotenv

scope = [
	'https://spreadsheets.google.com/feeds',
	'https://www.googleapis.com/auth/drive'
]

"""
Uncomment for running locally with .env file, you will need to move each key-value from client_secret.json
there. And wrap private key in quotes so it doesn't escape the backslashes.
"""
# load_dotenv()

# Using Heroku environment vars
cred_dict = {
	'type': os.environ.get('type'),
	'project_id': os.environ.get('project_id'),
	'private_key_id': os.environ.get('private_key_id'),
	'private_key': os.environ.get('private_key'),
	'client_email': os.environ.get('client_email'),
	'client_id': os.environ.get('client_id'),
	'auth_uri': os.environ.get('auth_uri'),
	'token_uri': os.environ.get('token_uri'),
	'auth_provider_x509_cert_url': os.environ.get('auth_provider_x509_cert_url'),
	'client_x509_cert_url': os.environ.get('client_x509_cert_url')
}

# Authorization
curPath = os.path.dirname(__file__)


cred = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,
														scope,
														token_uri=os.environ.get('token_uri'))

client = gspread.authorize(cred)

# Open a spreadsheet and a worksheet inside of it
sheet = client.open(os.environ.get('sheet_name'))
worksheet = sheet.worksheet('Maplist')


def fetch():
	nameList = worksheet.col_values(1)[3:]
	sizeList = worksheet.col_values(2)[3:]
	categList = worksheet.col_values(3)[3:]
	brokenList = worksheet.col_values(10)[3:]
	TscoreList = worksheet.col_values(11)[3:]
	validList = worksheet.col_values(14)[3:]
	return [nameList, sizeList, categList, brokenList, TscoreList, validList]
