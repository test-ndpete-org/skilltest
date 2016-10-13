#Nate Peterson
#Skill test October 2016

import os
import sys
import csv
import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv
from github import Github

def main():
    # Sanity Check
    #Check for token as an argument fail if not provided
    if not len(argv)>2:
        print("Missing github token or organization")
        print("Usage: python pyGit.py [token] [org]")
        exit(1)

    g = Github(login_or_token=argv[1])

    for u in g.get_organization(argv[2]).get_members():
        if not u.name:
            send_mail(u.login, u.email)
            csv_write_to_file(u.login, u.email)
            print("FAILED:login: %s name: %s email: %s" % (u.login,u.name,u.email))
        else:
            print("PASSED:login: %s name: %s email: %s" % (u.login,u.name,u.email))


def send_mail(username, email):
    #Used https://docs.python.org/3/library/email-examples.html
    #As basis for this function

    #get from Address
    gmail_from = input("Gmail Username: ")

    #setup framework for the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Name missing from Github profile"
    msg['From'] = gmail_from
    msg['To'] = email

    #plain text part
    text=""" %s, \n \
    Please login to https://github.com and add your name to you profile.""" % (username)

    #HTML version
    html="""\
    <html>
        <head></head>
        <body>
            <p>%s,<br>
                Please login to \
                <a href="https://github.com">https://github.com</a>\
                and add your name to your profile. Thanks.
            </p>
        </body>
    </html>""" % (username)

    #attach parts to the message
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    #Send the message
    #Code for Google based off examples from:
    #http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(gmail_from, getpass.getpass(prompt='Gmail Password: '))
    server.sendmail(gmail_from, email, msg.as_string())
    server.quit()


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def csv_write_to_file(username, email):
    writeFile = get_script_path() + "/nonames.csv"
    with open(writeFile, mode='a') as output:
        outwriter = csv.writer(output)
        outwriter.writerow([username, email])


if __name__ == '__main__':
    main()
