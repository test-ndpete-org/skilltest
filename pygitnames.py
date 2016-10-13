# Nate Peterson
# Skill test October 2016

import os
import sys
import configparser
import csv
import smtplib
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from github import Github


def main():
    # Read Config file
    config_file = get_script_path() + "/config.cfg"
    config = configparser.ConfigParser()
    config.read(config_file)

    # github section
    github_user = config['github']['github_user']
    github_password = config['github']['github_password']
    gitub_token = config['github']['github_token']
    organization = config['github']['organization']

    # email section
    email_user = config['email']['email_user']
    email_password = config['email']['email_password']

    # aws section
    bucket_name = config['aws']['bucket_name']

    # CONSTANTS
    OUTPUT_DIR = get_script_path()
    OUTPUT_NAME = "nonames.csv"
    OUTPUT_FILE = get_script_path() + "/" + OUTPUT_NAME

    # Check for Github Token or Username/password for Auth
    github_api = Github(login_or_token=gitub_token) if gitub_token else Github(
        login_or_token=github_user, password=github_password)

    for u in github_api.get_organization(organization).get_members():
        if not u.name:
            send_mail(email_user, email_password, u.login, u.email)
            csv_write_to_file(OUTPUT_FILE, u.login, u.email)

    # Upload finished file to s3
    upload_to_s3(OUTPUT_FILE, OUTPUT_NAME, bucket_name)


def get_script_path():
    """return scripts current working directory"""
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def csv_write_to_file(file, username, email):
    """write a row to local csv file.

    Arguments:
    file -- local file to write to
    username -- username to write
    email -- email address to write"""

    with open(file, mode='a') as output:
        outwriter = csv.writer(output)
        print("INFO: writing to Local file %s" % file)
        outwriter.writerow([username, email])


def upload_to_s3(file, key, bucket_name):
    """Upload local file to s3 bucket_name

    Arguments
    file -- file to upload
    key -- key name on s3 (filename)
    bucket_name -- bucket to upload data to"""
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_name).put_object(Key=key, Body=open(file, 'rb'))
    print("INFO: uploaded %s to bucket %s" % (file, bucket_name))


def send_mail(gmail_from, gmail_password, username, email):
    """Send email formatted email to user

    Arguments
    gmail_from -- Email to use for SMTP auth and From Address
    gmail_password -- password for SMTP auth
    username -- username printed in email body
    email -- email address to send To"""
    # Used https://docs.python.org/3/library/email-examples.html
    # As basis for this function

    # setup framework for the email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Name missing from Github profile"
    msg['From'] = gmail_from
    msg['To'] = email

    # plain text part
    text = """ %s, \n \
    Please login to https://github.com and add your name to you profile.""" % (username)

    # HTML version
    html = """\
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

    # attach parts to the message
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    # Send the message
    # Code for Google based off answers from:
    # http://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(gmail_from, gmail_password)
    server.sendmail(gmail_from, email, msg.as_string())
    server.quit()
    print("INFO: Sent email to %s" % email)


if __name__ == '__main__':
    main()
