Quickstart
==========

The Mechanical MOOC is a Django application. This quickstart will show you how to deploy the Mechanical MOOC to `heroku <https://www.heroku.com/>`_. To complete this quickstart you will need to use the linux command line.

`Set up a heroku account <https://devcenter.heroku.com/articles/quickstart#step-4-deploy-an-application>`_ and install the heroku toolbelt.

Get the code from github::

    git clone https://github.com/p2pu/mechanical-mooc

change into the source directory and run::

    heroku create

Set the django SECRET_KEY by running::

    heroku config:set SECRET_KEY="`uuidgen | md5pass`"

Next push the application code to heroku::

    git push heroku master

Then add the free development database and create the database tables::

    heroku addons:add heroku-postgresql:dev
    heroku run python manage.py syncdb --migrate

During the database creation, you need to create a superuser. This is the user that you will use to log in and create and send emails. Be sure to remember the credentials and don't make them admin:password!!

And finally, to open the Mechanical MOOC in your browser run::

    heroku open


What's next?
------------

* :doc:`Complete the Mechanical MOOC setup <setup>`
* :doc:`course`
* `Share your course idea and ask questions on the P2PU forum <http://thepeople.p2pu.org/t/using-the-mechanical-mooc-for-large-online-courses/437>`_
* :doc:`Update website and messaging copy <content>`
* :doc:`classphoto`
