import configparser 
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import telegram
import imaplib
import email
from email.header import decode_header
#import webbrowser
#import os
import time

async def sent_tg_message(messageList):
    try:
        bot = telegram.Bot(config.get("telegram","token"))
        for msg in messageList:
            logger.info("Send TG, Receive Date: [%s], from [%s], Subject [%s]", msg["recDate"], msg["sender"], msg["subject"])

            msgstr = "{}\n{}\n\n{}".format(msg["sender"], msg["subject"], msg["body"])
            await bot.send_message(config.get("telegram","chatId"), msgstr[:512])
            time.sleep(3)
    except Exception as e:
        logger.error("Exception: %s", e,exc_info=True)

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def query_unseen_email():
    messageList = []
    
    try:
        
        imap = imaplib.IMAP4_SSL(config.get("gmail","imapHost"))
        result = imap.login(config.get("gmail","username"), config.get("gmail","password"))
        imap.select('"[Gmail]/All Mail"', readonly = False)
        response, messages = imap.search(None, 'UnSeen')
        messages = messages[0].split()
        
        logger.info("Unseen email count: [%s]", len(messages))
    
        # No unseen message 
        if (len(messages) == 0):
            return messageList
                 
        for i in messages:
            # fetch the email message by ID
            res, msg = imap.fetch(str(i, 'utf-8'), "(RFC822)")
         
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                   
    
                    # decode the email subject
                    '''
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    '''
                    subject = msg["Subject"]
                    # decode email sender
                    '''
                    sender, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding)
                    '''
                    sender = msg["From"]
                    # if the email message is multipart
                    if msg.is_multipart():                        
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            """
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                print(body)
                                
                            
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
                                open(filepath, "wb").write(part.get_payload(decode=True))
                            """
                    else:                        
                        # extract content type of email
                        content_type = msg.get_content_type()
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        """
                        if content_type == "text/plain":
                            # print only text email parts
                            print(body)
                        if content_type == "text/html":
                            # if it's HTML, create a new HTML file and open it in browser
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filename = "index.html"
                            filepath = os.path.join(folder_name, filename)
                            # write the file
                            open(filepath, "w").write(body)
                            # open in the default browser
                            webbrowser.open(filepath)
                        """
                        
                    logger.info("Read email, Receive Date: [%s], from [%s], Subject [%s]", msg["Date"], sender, subject)
                        
                    msg = {
                            "recDate": msg["Date"],
                            "sender": sender,
                            "subject": subject,
                            "body": body
                        }
         
                    messageList.append(msg)
    finally: 
        if imap is not None:
            imap.close()
            imap.logout()  

    return messageList
    
def main(): 
    try:
        
        msssageList = query_unseen_email()
        asyncio.run(sent_tg_message(msssageList))
    except Exception as e:
        logger.error("Unhandled exception: %s", e,exc_info=True)
                

config = configparser.ConfigParser()    
config.read('config.ini')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
handler = RotatingFileHandler("server.log", maxBytes=1024*1024,
        backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)
        
if __name__ == "__main__":
    main()