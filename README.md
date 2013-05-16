# Mechanical MOOC

The Mechanical MOOC is a web based app that allows users to sign up for a course, send out regular email updates about the course and group people into small groups where they can discuss the course with their peers. Nothing more and nothing less.

## Running your own instance

The Mechanical MOOC is written as a Django application. You can use any hosting provider, but the easiest way to get going quickly is with [heroku](https://www.heroku.com/).

Get the code from github `git clone https://github.com/p2pu/mechanical-mooc`

After [setting up a heroku account](https://devcenter.heroku.com/articles/quickstart#step-4-deploy-an-application) if you havent already, run `heroku create` and `git push heroku master`

For sending email, we chose to use [mailgun](http://mailgun.com/). Unfortunately mailgun doesn't have a free account option, so sending out emails will cost some money :( You will need to set up a mailgun account and get the API keys.

Running mailgun also requires that you have a domain name set up (the @whatever.com where your emails will come from). See the mailgun documentation for instructions on this.

You will need to set a few configuration variables on heroku:
- MAILGUN_API_DOMAIN - the domain that you will use for email
- MAILGUN_API_KEY - your mailgun API key
- DEFAULT_FROM_ADDRESS - the email address that will be used when sending out emails
- EMAIL_DOMAIN - the same as the MAILFUN_API_DOMAIN (we probably need to remove this)

You can set these variables by running `heroku config:set MAILGUN_API_DOMAIN=yourdomain.org`

After all this you will need to create the database on heroku `heroku run python manage.py syncdb`

You will also need to create a sequence for your MOOC. A sequence is like a single run of your course, hopefully your course is a resounding success and you want to run many more!

    heroku run python mangage.py shell
    > from sequence import models
    > from datetime import datetime
    > start_date = datetime(2013, 12, 1)
    > signup_close_date = datetime(2013, 11, 23)
    > models.create_sequence(start_date, signup_close_date)
    > exit()

And then you will need to add the tasks that will send out the emails to new signups and scheduled emails. You can enable the scheduler by running `heroku addons:add scheduler:standard`

But to add the actual tasks, you need to log into your application dashboard. `heroku addons:open scheduler` will get you there quickly. The two scripts that you need to add are:
- python manage.py handle_new_signups
- python manage.py send_scheduled_mail

The first task should probably run every 10 minutes and the second task is recommended to run every hour.
