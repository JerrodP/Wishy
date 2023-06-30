# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import dateutil.parser as parser
import base64
from bs4 import BeautifulSoup

# Authentification Details
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
creds = None
user_id = 'me'

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "config/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


def main():

    # Output list of dictinaries
    output_list = []

    # Call the Gmail API
    try:
        gmail = build("gmail", "v1", credentials=creds)
        unread_msgs = gmail.users().messages().list(userId="me", q="is:unread label:inputs").execute()

    except HttpError as error:
        print(error)

    # Check for empty response, return if empty
    if unread_msgs['resultSizeEstimate'] == 0:
        print("No messages to aquire.")
        return

    msg_list = unread_msgs['messages']
    num_msg = len(msg_list)

    print ("Total unread messages in inbox: ", num_msg)

    for msg in msg_list:
        temp_dict = {}
        m_id = msg['id'] # Get ID of individual message

        # Get indivual message
        try:
            message = gmail.users().messages().get(userId=user_id, id=m_id).execute()

        except HttpError as error:
            print("HTTP Error", error)
        
        payload = message['payload']
        headers = payload['headers']

        # get Subject
        for header in headers:
            if header['name'] == 'Subject':
                msg_subject = header['value']
                temp_dict['Subject'] = msg_subject
            else:
                pass
        
        # get Date
        for header in headers:
            if header['name'] == 'Date':
                msg_date = header['value']
                date_parse = (parser.parse(msg_date))
                msg_date = (date_parse.date())
                temp_dict['Date'] = str(msg_date)
            else:
                pass
        
        # get Sender
        for header in headers:
            if header['name'] == 'From':
                msg_sender = header['value']
                temp_dict['Sender'] = msg_sender
            else:
                pass
        
        # get Message Snippet
        temp_dict['Snippet'] = message['snippet']

        # get Message Body
        try:
            msg_parts = payload['parts'] # fetching the message parts
            part_one  = msg_parts[0] # fetching first element of the part 
            part_body = part_one['body'] # fetching body of the message
            part_data = part_body['data'] # fetching data from the body
            clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
            clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two , "lxml" )
            msg_body = soup.body()

            # msg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned 
            # using regex, beautiful soup, or any other method
            temp_dict['Msg_Body'] = msg_body
        # TODO imporove error handling
        except:
            print("Error aquiring msg_body")
            pass

        print(temp_dict)
        output_list.append(temp_dict)

        #mark message as read so it's not read twice
        gmail.users().messages().modify(userId='me', id=m_id, body={'removeLabelIds': ['UNREAD']}).execute() 
	
    return output_list



if __name__ == "__main__":
    main()
# [END gmail_quickstart]
