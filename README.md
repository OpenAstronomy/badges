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
