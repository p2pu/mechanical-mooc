Setting up Mailgun
==================

For sending email and managing mailing lists we use [mailgun](http://mailgun.com/). You need to sign up for a mailgun account and get the API keys.

Set the API keys in the mechanical MOOC by running::
    
    heroku config:set MAILGUN_API_KEY=<api-key>
    heroku config:set MAILGUN_API_DOMAIN=<your-domain>

You need to replace <api-key> with the ``API Key`` you see at https://mailgun.com/cp.

And you need to replace <your-domain> with the domain you are using for mailgun. If you have just set up mailgun, chances are that this will be one of the sandbox domains: ``something.mailgun.org``. You can see :doc:`domain` on how to setup your domain properly.

Lastly you need to set the default email address that all emails to users will come from. Run::

    heroku config:set DEFAULT_FROM_EMAIL=mooc@example.net

Once you have set up sending email, make sure that you also configure :doc:`tasks <tasks>`.
