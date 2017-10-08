import datetime
import hashlib
import json
import os


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

        return json.dumps(award_dict)

    def check_templates():
        pass

    def create_templates(self, source):
        os.makedirs(os.path.join(source, self.directory_yr), exist_ok=True)
        files_out = {"criteria.html": "<h1> To update: {} </h1>",
                     "badge-class.json": json.dumps({"name": "ToUpdate: " + self.directory,
                                                     "description": "ToUpdate: " + self.directory,
                                                     "image": '/'.join([self.prefix_url, self.directory, 'badge-image.png']),
                                                     "criteria": '/'.join([self.prefix_url, self.directory, 'criteria.html']),
                                                     "issuer": '/'.join([self.prefix_url, 'badge-issuer.json'])}),
                     "badge-image.png": b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x90'}
        for badge_file in files_out:
            fullfile = os.path.join(source, self.directory, badge_file)
            if not os.path.isfile(fullfile):
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


