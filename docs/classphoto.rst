Configure class photo (optional)
================================

The MechanicalMOOC supports a light weigth method for users to put a face to their participation. 

Configure Amazon Web Services
-----------------------------

To use this feature you need an Amazon Web Services account since images are uploaded to Amazon S3. Once you created the account, create a keypair with access to the AWS S3 bucket that you want to use. See the `documentation over at Amazon <http://aws.amazon.com/iam/>`_ to see how to do this.

You also need to create a new bucket where the images will be uploaded to.

Once done, run::

    heroku config:set AWS_ACCESS_KEY_ID=<aws_access_key>
    heroku config:set AWS_SECRET_ACCESS_KEY=<aws_secret_key>
    heroku config:set AWS_S3_BUCKET=<bucket-name>

Configure getting profile data from Google+ and Twitter
-------------------------------------------------------

Next you need to obtain app keys for Twitter and Google+. For twitter you can follow `these instructions <https://dev.twitter.com/docs/auth/tokens-devtwittercom>`_. For Google+, see `this <https://developers.google.com/+/api/oauth>`_.

Once you've obtained the needed credentials, run::

    heroku config:set TWITTER_ACCESS_TOKEN=<access-token>
    heroku config:set TWITTER_ACCESS_TOKEN_SECRET=<access-token-secret>
    heroku config:set GOOGLE_PLUS_API_KEY=<api-key>

Sending an email to everyone who signed up with a link to the class photo
-------------------------------------------------------------------------

Need to explain, but code lives `here <https://github.com/p2pu/mechanical-mooc/blob/master/classphoto/emails.py#L55>`_.
