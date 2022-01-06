from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_DIR = os.path.join(ROOT_DIR, "credentials")
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, 'token.pickle')
CREDENTIAL_PATH = os.path.join(CREDENTIALS_DIR, 'credentials.json')

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailClient:

    def __init__(self):
        # Variable creds will store the user access token.
        # If no valid token found, we will create one.
        creds = None
  
        # The file token.pickle contains the user access token.
        # Check if it exists
        
        if os.path.exists(TOKEN_PATH):
    
            # Read the token from the file and store it in the variable creds
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
    
        # If credentials are not available or are invalid, ask the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
    
            # Save the access token in token.pickle file for the next run
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
    
        # Connect to the Gmail API
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_query_string(self, msg_to: str, msg_subject: str):
        
        query = ""

        if msg_to and msg_subject:
             query = "to:{0} AND subject:{1}".format(msg_to, msg_subject)
        elif msg_to and not msg_subject:
             query =  "to:{0}".format(msg_to)
        elif not msg_to and msg_subject:
             query = "subject:{0}".format(msg_subject)
        else:
            raise Exception
        return query

    def get_message_id(self, msg_to: str, msg_subject: str):
        
        query = self.get_query_string(msg_to, msg_subject)  
        results = self.service.users().messages().list(userId="me",labelIds = ["INBOX"], q=query ,maxResults=1).execute()
        messages = results.get("messages", [])
        return messages[0]["id"]
    
    def get_message(self, msg_to: str, msg_subject: str):

        message_id = self.get_message_id(msg_to, msg_subject)            
        msg_id = self.service.users().messages().get(userId='me', id=message_id).execute()                                      
        return msg_id

    def get_email_html(self, msg_to:str, msg_subject:str):

        message = self.get_message(msg_to, msg_subject)

        # Get value of 'payload' from dictionary 'mssage'
        payload = message['payload']

        # The Body of the message is in Encrypted format. So, we have to decode it.
        # Get the data and decode it with base 64 decoder.
        if payload["body"]["size"] == 0:
            if 'parts' in payload:
                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
        else:
            data = payload.get('body')['data']
            
        decode_data = base64.urlsafe_b64decode(data)    
        msg_html = decode_data.decode("utf-8")       
        
        return msg_html
    
    def get_email_content(self, msg_to: str, msg_subject: str):

        msg_html = self.get_email_html(msg_to, msg_subject)
        soup = BeautifulSoup(msg_html, "html.parser")
        msg_content = soup.get_text()

        return msg_content

