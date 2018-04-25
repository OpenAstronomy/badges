# Badges

This repository contains the code and the site to award and store awarded badges.

The codes in the `master` branch, the awarded ones are available on `gh-pages`.


The awarded badges will be stored following structure:

where `openastronomy/badges` will be the online site where it is available.

```
   openastronomy/badges/
                       /index.html                                  -- To explain what's in here.
                       /SoC/                                        -- award
                           /student/                                -- category (nested? separated with ';')
                                   /criteria.html
                                   /badge-class.json
                                   /badge-image.png
                                   /2017/
                                        /student1.json
                                        /student2.json
                           /mentor/
                                  /criteria.html
                                  /badge-class.json
                                  /badge-image.png
                                  /2017/
                                       /mentor1.json
                                       /mentor2.json
                                  /2016/
                                       /mentor1.json
                                       /mentor2.json
                           /organiser/
                                     /...
                       /Maintainer/                                -- Awarded at the end of the year.
                                  /SubOrg/
                                         /package/
                                                 /criteria.html
                                                 /badge-class.json
                                                 /badge-image.png
                                                 /2017/
                                              
                       /ConfOrganiser/
                       /Instructor/
````

Each directory may contain subdirectories, for example `ConfOrganiser` may
contain a `conference` (*e.g.*, `PiA` ) and badges awarded per different years.

As it is now, generate.py will generate the folder structure needed for that when a 
file with the following structure is given:

   | name    | email  | award      | category      |       date |
   |---------|--------|------------|---------------|------------|
   | personA | Aemail | SoC        | mentor        | 2017-09-01 |
   | personA | Aemail | Maintainer | sunpy;irispy  | 2017-01-01 |

where `category` can have multiple levels separated by `;`.

## How to award people badges?

Interesting question. Using GitHub pull-request system would be awesome.
However, the email of the person is needed, and I don't like to keep a list of
emails plain open in here. If that wouldn't be a problem, then a run on travis
could be done to generate the new awards. 
Meanwhile, I think it's easier if using a google document and run it manually
for the time being.

## How I use this

I open the two branches at the same time:

```bash
mkdir OAbadges
cd OAbadges
git clone git@github.com:OpenAstronomy/badges.git
cd badges
git fetch origin
git worktree add ../site gh-pages
cd ..
# Create the passwd file to send automatically the emails.
echo "email\npasswd" > passwd
```

then in python:
``` python
from badges.code.generate import Award
import pandas as pd
import datetime
import time

all = pd.read_csv('./gsoc2017.csv')

for index, n in all.iterrows():
    aw = Award(*[n[x] for x in all.head()])
    aw.save_award(source='./site')
    # If you are using gmail to send the emails.
    if index > 1 and index % 20 == 0 and (datetime.datetime.now() - t0).total_seconds() / 60. < 1:
        print("Waiting to don't pass the 20 msg/min limit")
        time.sleep(60)
    aw.email_badge(source='./site')
```

Though, remember, before the awardee can import the badges into their backpacs,
they need to be available online (*i.e.*, you need to push the `site` directory
as `gh-pages`)

To be able to send all using gmail, you need first to turn
on ["Access for less secure apps"](https://myaccount.google.com/lesssecureapps).
Also, be aware of the 20 e-mails/minute limit.
