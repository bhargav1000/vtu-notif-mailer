import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from zipfile import ZipFile
COMMASPACE = ', '

def notif_check(notif_var):
    searchObj1 = re.search( r'Student | student | STUDENT | students | STUDENTS | Students', notif_var, re.M|re.I)
    searchObj2 = re.search( r'Courses | courses | COURSES | courses | COURSES | Courses', notif_var, re.M|re.I)
    searchObj3 = re.search( r'Athletic Meet', notif_var, re.M|re.I)
    searchObj4 = re.search( r'All India', notif_var, re.M|re.I)
    if searchObj1 or searchObj2 or searchObj3 or searchObj4:
        return 'useful'
    else:
        return 'not useful'

def notif_scraper():
    notifications = []
    notif_page = 'http://vtu.ac.in/'
    page = urllib.request.urlopen(notif_page)
    soup = BeautifulSoup(page, 'html.parser')

    notif = soup.find('li',attrs={"class":"infobox-widget-description"})
    notif_body = notif.find_all('a')

    for i in notif_body:
        notifications.append(i.text.strip())

    notifs_to_send = []

    for i in range(1, int(len(notifications)/6)):
        notifs_to_send.append(notifications[i])

    mail = []
    body_of_mail = ''
    mail = re.split('\r\n\n\n\r\n |\r\n\n\n', notifs_to_send[0])
    for i in range(0, len(mail)):
        if notif_check(mail[i]) == 'useful':
            body_of_mail = body_of_mail + str(mail[i]) + '\n\n'
    return body_of_mail

def mailer():
    sender = '' #add your mail id, be sure to enable less secure apps in google security settings
    gmail_password = ''
    recipients = [] #list of recipients
    # Create the enclosing (outer) message

    outer = MIMEMultipart()
    email_subject = "VTU Notifications."
    outer['Subject'] = email_subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this attachment in a MIME-aware mail reader.\n'
    from email.mime.text import MIMEText
    text = 'This week\'s notifcations. \n\n' + notif_scraper() + '\nPFA: zip file with documents\n-Regards'
    outer.attach(
    MIMEText(text, 'plain')) # or 'html'
    # List of attachments
    attachments = ['./attachments.zip']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

def link_scraper():
    scraped_links = []
    html_page = urllib.request.urlopen("http://vtu.ac.in/")
    soup = BeautifulSoup(html_page, 'html.parser')
    links = soup.find('li',attrs={"class":"infobox-widget-description"})
    for link in links.find_all('a', attrs={'href': re.compile("^http://")}):
        scraped_links.append(link.get('href'))

    for href in scraped_links:
        if(href[len(href)-4:len(href)] == '.pdf'):
            os.system("wget " + href)






def get_all_file_paths(directory):

    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths

def compressor():
    # path to folder which needs to be zipped
    directory = './attachments'

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    with ZipFile('attachments.zip','w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    print('All files zipped successfully!')

def main():
    os.system("mkdir ./attachments")
    os.chdir("./attachments")
    link_scraper()
    os.chdir("..")
    compressor()
    mailer()
    os.system("rm -r attachments attachments.zip")


main()
