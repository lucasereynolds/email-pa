# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 09:56:29 2021

@author: LReynolds
"""
from string import Template
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from tower_bridge_lift_scraper import Parser, Scraper

class EmailBot():
    """Bot to send results email."""
    SENDER_ADDRESS = "XXX"
    SENDER_PASSWORD = "XXX"
    
    def __init__(self):
        self.connection = None
        self.target_address = "XXX"
        self.target_name = "Lucas"
        self.message_template = self._set_message_template("template.txt")
        
        self.payload = ""
    
    def create_connection(self):
        self.connection = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        self.connection.starttls()
        self.connection.login(EmailBot.SENDER_ADDRESS, EmailBot.SENDER_PASSWORD)

    def close_connection(self):
        if self.connection is not None:
            self.connection.quit()
            
    def send_message(self):
        msg = MIMEMultipart()
        
        payload = self.message_template.substitute(PERSON_NAME="Lucas")
        
        # Set Parameters
        msg['From'] = EmailBot.SENDER_ADDRESS
        msg['To'] = self.target_address
        msg['Subject'] = "This is a test."
        
        msg.attach(MIMEText(payload, "plain"))
        
        self.connection.send_message(msg)
        
        del msg
    
    def _set_message_template(self, template_file):
        """Set template from template.txt."""
        with open("template.txt", "r") as f:
            message_template = f.readlines()
        message_template = ''.join(message_template)
        message_template = Template(message_template)
        
        return message_template
    
    def create_payload(self):
        """Construct email withlift events parameter""" 
        message = self.message_template.substitute(PERSON_NAME="Lucas")
        return message


def send_email_test(email_bot):
    email_bot.create_connection()
    email_bot.send_message()
    email_bot.close_connection()

if __name__ == "__main__":
    # Create objects
    scraper = Scraper()
    parser = Parser()
    email_bot = EmailBot()
    
    send_email_test(email_bot)
    
    