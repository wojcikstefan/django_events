from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def home(request, template='events/home.html'):
    context = {}
    return render_to_response(template, context,
                              context_instance=RequestContext(request))