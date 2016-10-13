# Purpose
The purpose of the application is to utilize the github api to scan an organization's members and identify users who don't have their name filled out in their profile. Users identified are then prompted to add their name to their profile via email. Finally a csv of all users for that organization is uploaded to an S3 bucket.

# Installation
To install simply run `git clone https://github.com/ndpete/skilltest.git`

# Prerequisites
- Developed and Tested with Python 3.5.2
- PIP modules needed
 - `pip install pygithub`
 - `pip install boto3`

# Configuration
1. To configure application copy example configuration `cp config.example config.cfg`
2. Edit `config.cfg` with your text editor of choice
  - Github Section: add your username or alternatively your api token:
    - github_user = github username
    - github_password = github password
    - github_token = github token
    - organization = organization name to scan for missing names
  - Email section:
    - Currently script supports SMTP with TLS auth through Gmail
      - Requires gmail account to accept less secure apps. [Google Ref](https://support.google.com/accounts/answer/6010255?hl=en)
    - email_user = email username, used for SMTP AUTH and From field
    - email_password = email password used for SMTP AUTH
  - AWS section:
    - bucket_name = Name of the bucket to upload file to.
3. AWS Credentials Configuration File
  - An aws Credentials configuration file is required
    - Default location `~/.aws/credentials` [Format Examples](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration)

# Running
To run simply run `python ./pygitnames.py`

# Assumptions
1. Developed on MacOS. Will work on MacOS & \*nix Operating Systems not Tested on Windows.
