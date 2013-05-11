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
from mail.email import send_email_to_groups

import bleach
import datetime


def _clean_html(html):
    return bleach.clean(html, strip=True)


@login_required
def compose( request ):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        tags = request.POST.get('tags')
        mail_api.save_email(subject, text_body, html_body, tags)

        return http.HttpResponseRedirect(
            reverse('mail_schedule')
        )

    return render_to_response(
        'mail/compose.html',
        {},
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
        mail_api.update_email(email_uri, subject, text_body, html_body, tags)
        return http.HttpResponseRedirect(reverse('mail_schedule'))

    return render_to_response(
        'mail/compose.html',
        {'email': email},
        context_instance=RequestContext(request)
    )


@login_required
def send_preview( request ):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        to_email = request.POST.get('test_email')
        mailgun_api.send_email(to_email, settings.DEFAULT_FROM_EMAIL, subject, text_body, html_body)
        return http.HttpResponseRedirect(reverse('mail_schedule'))
    raise Exception()


@login_required
def send( request, id ):
    email_uri = mail_api.id2uri(id)
    send_email_to_groups(email_uri)
    return http.HttpResponseRedirect(reverse('mail_schedule'))


@login_required
def delete( request, id ):
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
