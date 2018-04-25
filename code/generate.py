import datetime
import hashlib
import json
import os
import tempfile

from openbadges_bakery import bake


class Award(object):
    def __init__(self, name, email, award, category, date, salt="Don't Panic"):
        self.name = name
        self.email = email

        self.award = award
        self.categories = category.split(';')

        if not isinstance(date, datetime.date):
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        self.date = date

        self.salt = salt
        self.uid = hashlib.sha256(self.email.encode() + salt.encode()).hexdigest()
        self.short_uid = self.uid[0:10]

        self.prefix_url = "http://openastronomy.org/badges"

    def generate_json(self):
        award_dict = {"@context": "https://w3id.org/openbadges/v1",
                      "type": "Assertion",
                      "uid": "",
                      "recipient": {
                          "type": "email",
                          "hashed": True,
                          "salt": "",
                          "identity": ""
                      },
                      "issuedOn":  "",
                      "badge": "",
                      "verify": {
                          "type": "hosted",
                          "url": ""
                      }}

        award_dict['recipient']['salt'] = self.salt
        award_dict['uid'] = self.short_uid
        award_dict['recipient']['identity'] = 'sha256$' + self.uid

        award_dict['issuedOn'] = '{:%Y-%m-%d}'.format(self.date)

        self.directory = '/'.join([self.award, *self.categories])
        self.directory_yr = '/'.join([self.directory, str(self.date.year)])
        self.award_file = '/'.join([self.directory_yr, '{}.json'.format(self.short_uid)])
        award_dict['badge'] = '/'.join([self.prefix_url, self.directory, 'badge-class.json'])
        award_dict['verify']['url'] = '/'.join([self.prefix_url, self.award_file])

        return json.dumps(award_dict, indent=4)

    def check_templates():
        pass

    def create_templates(self, source):
        os.makedirs(os.path.join(source, self.directory_yr), exist_ok=True)
        files_out = {"criteria.html": "<h1> To update: {} </h1>",
                     "badge-class.json": json.dumps({"name": "ToUpdate: " + self.directory,
                                                     "description": "ToUpdate: " + self.directory,
                                                     "image": '/'.join([self.prefix_url, self.directory, 'badge-image.png']),
                                                     "criteria": '/'.join([self.prefix_url, self.directory, 'criteria.html']),
                                                     "issuer": '/'.join([self.prefix_url, 'badge-issuer.json'])},
                                                    indent=4),
                     "badge-image.png": b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90'}
        for badge_file in files_out:
            fullfile = os.path.join(source, self.directory, badge_file)
            if not os.path.isfile(fullfile) and not os.path.isfile(fullfile.replace('png', 'svg')):
                print("########## created {} - please update ".format(badge_file)) # TODO: Set as log message
                binary = 'wb' if 'png' in badge_file else 'w'
                with open(fullfile, binary) as ff:
                    ff.write(files_out[badge_file])

    def save_award(self, source='./badges'):
        award_json = self.generate_json()

        self.create_templates(source)
        award_file = os.path.join(source, self.award_file)
        if not os.path.isfile(award_file):
            with open(award_file, 'w') as ff:
                ff.write(award_json)
        else:
            print("********** Award already exists - Not overwriting \n {}".format(award_file))


    def cooking(self, source):
        # find the image of the award:
        self.badge = os.path.join(source, self.directory, 'badge-image.png')
        if not os.path.isfile(self.badge):
            self.badge = self.badge.replace('png', 'svg')
            if not os.path.isfile(self.badge):
                raise "Badge not available: it should be in {}/badge_image.[png|svg]".format(os.join(source, self.directory))
        badge_file = open(self.badge, 'rb')
        with tempfile.NamedTemporaryFile('wb', suffix=self.badge[-3:], delete=False) as badge_baked:
            bake(badge_file, self.generate_json(), badge_baked)
        return badge_baked.name

    def email_badge(self, source='./badges'):
        import smtplib
        import imghdr
        from email.message import EmailMessage
        import textwrap


        with open('passwd', 'r') as passwd:
            gmail_user = passwd.readline()[:-1] # if reads the \n, it messes the whole email.
            gmail_password = passwd.readline()
        # Create the container email message.

        msg = EmailMessage()
        msg['Subject'] = 'Your OpenAstronomy badge: {}'.format(self.directory)
        # me == the sender's email address
        # family = the list of all recipients' email addresses
        msg['From'] = gmail_user
        msg['To'] = self.email
        msg.preamble = "Your OpenAstronomy badge!"
        msg.set_content(textwrap.dedent("""\
        Dear {name},

        Congratulations!!! You've been awarded this badge for being a {what} during {when:%Y}.

        You can import the attached badge into Mozilla's backpack (http://backpack.openbadges.org/) or
        on Open Badge Passport (https://openbadgepassport.com/).

        Thanks for making OpenAstronomy better!!
        """.format(name=self.name, what=self.directory, when=self.date)))

        badge_file = self.cooking(source)
        print(badge_file)
        with open(badge_file, 'rb') as badge:
            badge_content = badge.read()
            if badge_file[-3:] != 'svg':
                subtype = imghdr.what(None, badge_content)
            else:
                subtype = "svg+xml"
            msg.add_attachment(badge_content, maintype='image',
                               subtype=subtype,
                               filename='OA_{what}_badge_{when:%Y}.{ext}'.format(what=self.directory.replace('/', '_'),
                                                                                 when=self.date,
                                                                                 ext=badge_file[-3:]))

        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server_ssl.ehlo()   # optional
            server_ssl.login(gmail_user, gmail_password)
            server_ssl.send_message(msg)
            server_ssl.close()
        except:
            raise 'Something went wrong...'
        finally:
            os.remove(badge_file)
