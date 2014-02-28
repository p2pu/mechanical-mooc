Customize site
==============

To customize the landing page, you need to edit `templates/signup/index.html <https://github.com/p2pu/mechanical-mooc/blob/master/templates/signup/index.html>`_. This page includes the form used during signup. You can customize the questions whithout needing to modify the Python code, but be sure to put in unique names for every field you add and to validate anything that needs validation on the client side. The only field that you cannot remove is the timezone field.

To customize the welcome email sent to users, edit the three files in `templates/signup/emails/ <https://github.com/p2pu/mechanical-mooc/tree/master/templates/signup/emails>`_.

The content that lives in the about and FAQ links at the top lives in `templates/about.html <https://github.com/p2pu/mechanical-mooc/blob/master/templates/about.html>`_ and `templates/faq.html <https://github.com/p2pu/mechanical-mooc/blob/master/templates/faq.html>`_ respectively.

To edit the topnav, update::

    <div class="nav-collapse collapse">
        <ul class="nav main-menu">
            <li><a class="home" href="{% url 'home' %}"><i class="icon-home"></i></a></li>
            <li><a href="{% url 'faq' %}">FAQ</a></li>
            <li><a href="http://mechanicalmooc.wordpress.com">Blog</a></li>
            <li><a href="{% url 'about' %}">About</a></li>
        </ul>
    </div>

in `templates/base.html <https://github.com/p2pu/mechanical-mooc/blob/master/templates/base.html>`_.
