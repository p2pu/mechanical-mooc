from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext

from signup import models as signup_api

def signup_count(request, sequence):
    sequence = int(sequence)

    context = {
        'signup_count': str(len(signup_api.get_signups(sequence))),
        'sequence': sequence
    }

    return render_to_response(
        'stats/signup_count.html',
        context,
        context_instance=RequestContext(request)
    )
