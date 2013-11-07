# Create your views here.
from django import http
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json

from groups import models as group_model


def get_group( request ):
    context = {}
    if request.method == 'POST':
        #get group
        email = request.POST.get('email')
        groups = group_model.get_member_groups(email)
        if len(groups) > 0:
            group['number'] = group['uri'].strip('/').split('/')[-1]
            context['group'] = groups[0]
        else:
            context['problem'] = True
    
    return render_to_response('groups/get_group.html', context, context_instance=RequestContext(request))
