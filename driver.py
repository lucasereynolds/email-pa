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
        self.target_address = "l_e_reynolds@outlook.com"
        self.target_name = "Lucas"
        self.message_template = self._set_message_template("template.txt")
    
    def create_connection(self):
        self.connection = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        self.connection.starttls()
        self.connection.login(EmailBot.SENDER_ADDRESS, EmailBot.SENDER_PASSWORD)

    def close_connection(self):
        if self.connection is not None:
            self.connection.quit()
            
    def send_message(self, events):
        msg = MIMEMultipart()
        
        payload = self.create_payload(events)
        
        # Set Parameters
        msg['From'] = EmailBot.SENDER_ADDRESS
        msg['To'] = self.target_address
        msg['Subject'] = "Morning Information"
        
        msg.attach(MIMEText(payload, "plain"))
        
        self.connection.send_message(msg)
        
        del msg
    
    def _set_message_template(self, template_file):
        """Set template from template.txt."""
        with open(template_file, "r") as f:
            message_template = f.readlines()
        message_template = ''.join(message_template)
        message_template = Template(message_template)
        
        return message_template
    
    def create_payload(self, events):
        """Construct email with lift events parameter"""
        events = [str(event) for event in events]
        
        events_string = "\n".join(events)
        
        payload = self.message_template.substitute\
            (PERSON_NAME=self.target_name, LIFT_EVENTS = events_string)
        return payload


def send_email_test(email_bot):
    email_bot.create_connection()
    email_bot.send_message()
    email_bot.close_connection()
    
def get_login_details():
    with open("credentials.txt", "r") as f:
        creds = f.readlines()
    creds = creds[0].split(" : ")
    user, password = creds[0], creds[1]
    return user, password

if __name__ == "__main__":
    # Create objects
    scraper = Scraper("https://www.towerbridge.org.uk/lift-times")
    parser = Parser()
    email_bot = EmailBot()
    
    EmailBot.SENDER_ADDRESS, EmailBot.SENDER_PASSWORD = get_login_details()
    
    # Scrape for lift times
    response = scraper.scrape()
    events = parser.parse(response)
    
    # Create connection
    email_bot.create_connection()
    
    # Send results
    email_bot.send_message(events)
    
    # Close connection
    email_bot.close_connection()
    
    
    