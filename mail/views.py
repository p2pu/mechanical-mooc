from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from mail import models as mail_api
from mailgun import api as mailgun_api
from mail.email import send_email
from sequence import models as sequence_model

import bleach
import datetime
import re


def _clean_html(html):
    expression = re.compile(r'<a.*?href="(?P<url>.*?)".*?>(?P<text>.*?)</a>')
    # rewrite links
    html = expression.sub(r'\2 ( \1 ) ', html)
    # remove all HTML markup
    return bleach.clean(html, tags=[], strip=True)


@login_required
def compose( request ):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        tags = request.POST.get('tags')
        sequence = 1
        audience = 'individuals'
        if request.POST.get('to', None):
            sequence = int(request.POST.get('to').split('-')[1])
            audience = request.POST.get('to').split('-')[0]

        mail_api.save_email(subject, text_body, html_body, sequence, audience, tags)

        return http.HttpResponseRedirect(
            reverse('mail_schedule')
        )

    context = {
        'sequences': sequence_model.get_all_sequences()
    }
    return render_to_response(
        'mail/compose.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def edit( request, id ):
    email_uri = mail_api.id2uri(id)
    email = mail_api.get_email(email_uri)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        tags = request.POST.get('tags')
        sequence = int(request.POST.get('to').split('-')[1])
        audience = request.POST.get('to').split('-')[0]

        mail_api.update_email(email_uri, subject, text_body, html_body, 
            sequence, audience, tags)
        return http.HttpResponseRedirect(reverse('mail_schedule'))

    context = {
        'sequences': sequence_model.get_all_sequences(),
        'email': email,
    }
    return render_to_response(
        'mail/compose.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def send_preview( request ):
    """ ajax view to send preview email """
    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        to_email = request.POST.get('test_email')
        mailgun_api.send_email(to_email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body)
        return http.HttpResponse('')
    raise Exception()


@login_required
def send( request, id ):
    #TODO should require a POST
    email_uri = mail_api.id2uri(id)
    send_email(email_uri)
    return http.HttpResponseRedirect(reverse('mail_schedule'))


@login_required
def delete( request, id ):
    #TODO should require a POST
    email_uri = mail_api.id2uri(id)
    mail_api.delete_email(email_uri)
    return http.HttpResponseRedirect(reverse('mail_schedule'))


@login_required
def schedule( request ):
    context = {
        'schedule': mail_api.get_emails()
    }
    return render_to_response('mail/schedule.html', context, context_instance=RequestContext(request))


@login_required
def schedule_email( request, id ):
    email_uri = mail_api.id2uri(id)
    date_text = request.POST.get('scheduled_date')
    time_text = request.POST.get('scheduled_time')

    if len(date_text) == 0:
        return http.HttpResponse(_('Please choose a date.'), status=400)

    if len(time_text) == 0:
        return http.HttpResponse(_('Please choose a time.'), status=400)

    date_text += time_text
    dt = datetime.datetime.strptime(date_text, '%Y-%m-%d%H:%M')
    if dt < datetime.datetime.utcnow():
        return http.HttpResponse(_('Scheduled time is in the past'), status=400)
    mail_api.schedule_email(email_uri, dt)
    return http.HttpResponse('')
