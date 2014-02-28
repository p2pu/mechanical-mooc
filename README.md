# Mechanical MOOC [![Build Status](https://travis-ci.org/p2pu/mechanical-mooc.png)](https://travis-ci.org/p2pu/mechanical-mooc)

The Mechanical MOOC is a web based app for running a course with a large number of users. Users can sign up for a course, you can send regular email updates about the course and group people into small groups where they can discuss the course with their peers. Nothing more and nothing less.

## Documentation

Documentation can be found [here](http://the-mechanical-mooc.readthedocs.org/en/latest/quickstart.html)

## Running your own instance

The Mechanical MOOC is written as a Django application. You can use any hosting provider, but the easiest way to get going quickly is with [heroku](https://www.heroku.com/).

Get the code from github `git clone https://github.com/p2pu/mechanical-mooc`

After [setting up a heroku account](https://devcenter.heroku.com/articles/quickstart#step-4-deploy-an-application) if you havent already, run `heroku create` and `git push heroku master`

### Email

For sending email and managing mailing lists we use [mailgun](http://mailgun.com/). Sign up for a mailgun account and get the API keys.

You need to configure the domain name for email - the @whatever.com where your emails will come from. See the mailgun documentation for instructions on how to configure this.

You will need to set a few configuration variables on heroku:
- SECRET_KEY - a random string used for ecrypting user cookies
- MAILGUN_API_DOMAIN - the domain that you will use for email
- MAILGUN_API_KEY - your mailgun API key
- EMAIL_HOST - smtp.mailgun.org
- EMAIL_HOST_USER - the user for sending email through mailgun
- EMAIL_HOST_PASSWORD - the password for sending email
- EMAIL_DOMAIN - the same as the MAILGUN_API_DOMAIN (we probably need to remove this)
- DEFAULT_FROM_EMAIL - the email address that will be used when sending out emails
- AWS_ACCESS_KEY_ID - your AWS credentials if you want to use the class photo function
- AWS_SECRET_ACCESS_KEY - 
- AWS_S3_BUCKET -
- MOOC_TITLE - Title of your course. Used in notifications
- MOOC_DOMAIN - The base URL where the MechanicalMOOC is running
- TWITTER_ACCESS_TOKEN - Twitter credentials to allow users to get info from Twitter for the class photo.
- TWITTER_ACCESS_TOKEN_SECRET - 
- GOOGLE_PLUS_API_KEY - Google+ credentials to allow users to get info from Google+ for the class photo

You can set these variables by running `heroku config:set MAILGUN_API_DOMAIN=yourdomain.org`

Don't forget to update the confirmation emails that are sent out to people who sign up. The templates are in the `templates/signup/emails` folder.

We recommend that you also setup a mailbox for the default email address that you are sending from. This way you can analyze the messages sent during the run of the course.

### Database 

Add the postgres addon by running `heroku addons:add heroku-postgresql:dev`.

Then set the config variable DATABASE_URL to the value of HEROKU_POSTGRESQL_URL

Run `heroku run python manage.py syncdb`.

During the database creation, you need to create a superuser. This is the user that you will use to log in and create and send emails.

You also need to create a sequence for your MOOC. A sequence is a single run of your course, obviously your course will be a resounding success and you will want to run many more!

    heroku run python manage.py shell
    > from sequence import models
    > from datetime import datetime
    > start_date = datetime(2013, 12, 1)
    > signup_close_date = datetime(2013, 11, 23)
    > models.create_sequence(start_date, signup_close_date)
    > exit()

### Heroku Scheduler

Enable the Heroku scheduler to send out the emails to new signups and scheduled emails. Run: `heroku addons:add scheduler:standard`

Then add the tasks - log into your application dashboard. `heroku addons:open scheduler` will open the dashboard in your webbrowser. Through the web form, add the following scripts:

- python manage.py handle_new_signups
- python manage.py send_scheduled_mail

The first task should run every 10 minutes and the second task should run every hour.

That's it, you are all set up to run your very own Mechanical Mooc and enlighten the world with peer learning!

### Setting up a custom domain

If you've followed the instruction above, you will have a MOOC running at some url like randomname.herokuapp.com. You probably want your MechanicalMOOC to run at a URL like thebestcourseintheworld.org. To do this, follow [these](https://devcenter.heroku.com/articles/custom-domains) instructions from Heroku.

### Setup for class photo (optional)

The MechanicalMOOC also supports a light weigth method for users to put a face to their participation. To use this feature you will need a Amazon Webservices Account since images are uploaded to Amazon S3. Once you created the account, create a keypair with access to the AWS S3 bucket that you want to use.

Next you need to obtain app keys for Twitter and Google+. For twitter you can follow [these](https://dev.twitter.com/docs/auth/tokens-devtwittercom) instructions. For Google+, see [this](https://developers.google.com/+/api/oauth).

Once you've obtained all the necessary keys, update the following variables:

- AWS_ACCESS_KEY_ID - your AWS credentials if you want to use the class photo function
- AWS_SECRET_ACCESS_KEY - 
- AWS_S3_BUCKET - the name of the bucket where the user images will be uploaded
- TWITTER_ACCESS_TOKEN - Twitter credentials to allow users to get info from Twitter for the class photo.
- TWITTER_ACCESS_TOKEN_SECRET - 
- GOOGLE_PLUS_API_KEY - Google+ credentials to allow users to get info from Google+ for the class photo


## Example Use Cases

The Mechanical MOOC has been used to create a number of educational experiences on the web. We've included the relevant Trello boards for the MOOCs to show the learning design and content development phases as well.

### Learning Creative Learning: [learn.mit.edu](http://learn.media.mit.edu/)
A partnership with the MIT Media Lab, the Learning Creative Learning Mechanical MOOC supported over 14,000 learners.

### Data Explorer Mission: [schoolofdata.org/datamooc](http://schoolofdata.org/datamooc/)
A pilot project with the [Open Knowledge Foundation](http://okfn.org/), the Data Explorer Mission supported 13 learning groups and 151 learners.
[Trello Board for Data Explorer Mission](https://trello.com/b/cUxgGZOO/data-explorer-mission)

### A Gentle Introduction to Python: [mechanicalmooc.org](http://mechanicalmooc.org/)
The original "Mechanical MOOC" is a partnership between MIT OCW, OpenStudy, Codecademy and P2PU. Now in its 4th cycle, MOOC has supported over 10,000 learners.

### Play with your music: [playwithyourmusic.org](http://www.playwithyourmusic.org)
A online course in audio production in collaboration with NYU Steinhardt with more than 3000 students in the first round.
