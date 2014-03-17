Setting up the Mechanical MOOC
==============================

If you followed the instructions in the :doc:`quick start <quickstart>` you will have a basic runnig example of the Mechanical MOOC, but you won't be able to send out emails, it will run at a subdomain at heroku and all the content will still be the example content.

Setting up email
------------------

For sending email and managing mailing lists we use `mailgun <http://mailgun.com/>`_. You need to sign up for a mailgun account and get the API keys.

Set the API keys in the mechanical MOOC by running::
    
    heroku config:set MAILGUN_API_KEY=<api-key>
    heroku config:set MAILGUN_API_DOMAIN=<your-domain>

You need to replace <api-key> with the ``API Key`` you see at https://mailgun.com/cp.

And you need to replace <your-domain> with the domain you are using for mailgun. If you have just set up mailgun, chances are that this will be one of the sandbox domains: ``something.mailgun.org``.

Lastly you need to set the default email address that all emails to users will come from. Run::

    heroku config:set DEFAULT_FROM_EMAIL=mooc@example.net

Setting up Heroku scheduler
---------------------------

Enable the Heroku scheduler to send out the welcome email to new users who signed up and to send the emails that you schedule. 

Tasks use an Heroku addon that runs some python scripts. Run::

    heroku addons:add scheduler:standard

to enable the addon.

Then add the tasks - log into your application dashboard. `heroku addons:open scheduler` will open the dashboard in your webbrowser. Through the web form, add the following scripts:

* ``python manage.py handle_new_signups``
* ``python manage.py send_scheduled_mail``

The first task should run every 10 minutes and the second task should run every hour.

Setup a domain for Heroku
-------------------------

Because of the way that Heroku works, it is best to run the Mechanical MOOC at a subdomain (remember that www. is also a subdomain if another subdomain doesn't make sense). You can follow `these <https://devcenter.heroku.com/articles/custom-domains>`_ instructions on how to configure a custom domain. This will be the domain where you send users to sign up.

Setup a domain for mailgun
--------------------------

Mailgun needs a custom domain to `function properly <http://documentation.mailgun.com/quickstart.html#verifying-your-domain>`_. You can follow the instructions there to setup the domain. Once done, run::

    heroku config:set MAILGUN_API_DOMAIN=<your-domain>

with your proper domain.
