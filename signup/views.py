# Create your views here.
from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder

from forms import SignupForm
from signup import models as signup_model

@csrf_exempt
@require_http_methods(['POST'])
def signup( request, iframe=False ):

    form = SignupForm(request.POST)

    if not form.is_valid():
        if request.is_ajax():
            #TODO include error message and use appropriate code
            return http.HttpResponse(code=400)
        else:
            return render_to_response('signup/error.html', {'form': form}, context_instance=RequestContext(request))

    email = form.cleaned_data['email']
    signup_questions = request.POST.dict()
    del signup_questions['email']
    if 'csrfmiddlewaretoken' in signup_questions:
        del signup_questions['csrfmiddlewaretoken']

    signup_model.create_or_update_signup(email, signup_questions )
    
    if request.is_ajax():
        response = http.HttpResponse(code=200)
        response['Access-Control-Allow-Origin'] = '*.p2pu.org'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        #response['Access-Control-Allow-Headers'] =  'X-PINGOTHER'
        response['Access-Control-Max-Age'] = '1728000'
        return response
    elif iframe:
        return http.HttpResponseRedirect(reverse('signup_success_iframe'))
    return http.HttpResponseRedirect(reverse('signup_success'))


def signup_success( request ):
    return render_to_response('signup/success.html', {}, context_instance=RequestContext(request))


def count(request, sequence):
    sequence = int(sequence)

    context = {
        'signup_count': str(len(signup_model.get_signups(sequence))),
        'sequence': sequence
    }

    return render_to_response(
        'signup/count.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def export(request, sequence):
    sequence = int(sequence)
    signups = signup_model.get_signups(sequence)
    return http.HttpResponse(json.dumps(signups, cls=DjangoJSONEncoder), content_type='application/json')
