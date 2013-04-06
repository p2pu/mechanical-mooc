from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages

from mail import models as mail_api

import bleach


def _clean_html(html):
    return bleach.clean(html, strip=True)


def compose( request ):
    if request.method == 'POST':
        tags = request.POST.get('tags')
        subject = request.POST.get('subject')
        body = request.POST.get('body_text')
        text_body = _clean_html(body)
        mail_api.save_email(subject, text_body, body)

        return http.HttpResponseRedirect(
            reverse('mail_schedule')
        )

    return render_to_response(
        'mail/compose.html',
        {},
        context_instance=RequestContext(request)
    )


def edit( request, id ):
    email_uri = mail_api.id2uri(id)
    email = mail_api.get_email(email_uri)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        html_body = request.POST.get('body_text')
        text_body = _clean_html(html_body)
        mail_api.update_email(email_uri, subject, text_body, html_body)
        return http.HttpResponseRedirect(reverse('mail_schedule'))

    return render_to_response(
        'mail/compose.html',
        {'email': email},
        context_instance=RequestContext(request)
    )


def delete( request, id ):
    email_uri = mail_api.id2uri(id)
    mail_api.delete_email(email_uri)
    return http.HttpResponseRedirect(reverse('mail_schedule'))


def schedule( request ):
    context = {
        'schedule': mail_api.get_emails()
    }
    return render_to_response('mail/schedule.html', context, context_instance=RequestContext(request))
