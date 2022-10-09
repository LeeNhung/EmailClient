from flask import Flask, render_template
import imaplib
import email
from email.header import decode_header
import webbrowser
import os

app = Flask(__name__)


@app.route('/')
def read_page():
    username = "nhungleqaz2@gmail.com"
    password = "pfnrbgsnqhuehhmb"
    imap_server = "imap.gmail.com"
    mails=[]

    def clean(text):

        return "".join(c if c.isalnum() else "_" for c in text)

    # create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL(imap_server)

    # authenticate
    imap.login(username, password)

    status, messages = imap.select("inbox")

    # number of top emails to fetch
    N = 1

    # total number of emails
    messages = int(messages[0])

    for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                # decode Date
                Date, encoding = decode_header(msg.get("Date"))[0]
                if isinstance(Date, bytes):
                    Date = Date.decode(encoding)
                
                print("Subject:", subject)
                print("From:", From)
                print("Date:", Date)

                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                            dict1={'Subject': subject,'From':From, 'Date':Date, 'Content':body}

                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                a= open(filepath, "wb").write(part.get_payload(decode=True))
                            dict1={'Subject': subject,'From':From, 'Date':Date, 'Content':a}
      
                # if content_type == "text/html":
                #     # if it's HTML, create a new HTML file and open it in browser
                #     folder_name = clean(subject)
                #     if not os.path.isdir(folder_name):
                #         # make a folder for this email (named after the subject)
                #         os.mkdir(folder_name)
                #     filename = "index.html"
                #     filepath = os.path.join(folder_name, filename)
                #     # write the file
                #     open(filepath, "w", encoding='utf-8').write(body)
                #     # open in the default browser
                #     webbrowser.open(filepath)
                # print("="*100)

                mails.append(dict1)
                for mail in mails:
                    print(mail)
    return render_template('readMails.html', mails = mails)
    # close the connection and logout
    imap.close()
    imap.logout()

if __name__ == "__main__":
   app.run(debug = True)
