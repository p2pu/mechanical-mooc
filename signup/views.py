# Create your views here.
from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse

from forms import SignupForm
from signup import models as signup_model

@require_http_methods(['POST'])
def signup( request ):

    form = SignupForm(request.POST)

    if not form.is_valid():
        return render_to_response('signup/error.html', {'form': form}, context_instance=RequestContext(request))

    email = form.cleaned_data['email']
    timezone = form.cleaned_data['timezone']
    signup_questions = request.POST.dict()
    del signup_questions['email']
    del signup_questions['csrfmiddlewaretoken']

    signup_model.create_or_update_signup(email, signup_questions )

    return http.HttpResponseRedirect(reverse('signup_success'))


def signup_success( request ):
    return render_to_response('signup/success.html', {}, context_instance=RequestContext(request))
