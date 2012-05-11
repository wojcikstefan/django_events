from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from cart import Cart, ItemAlreadyExists, ItemDoesNotExist
from models import *
from forms import *

def home(request, template='events/home.html'):
    events = Event.objects.filter(private=False)
    paginator = Paginator(events, 5)
    page = request.REQUEST.get('page')
    if page:
        page = int(page)
    try:
        events = paginator.page(page)
    except:
        events = paginator.page(1)
    context = {
        'events' : events
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def event(request, event_id, template='events/event.html'):
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event' : event
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def search(request, template='events/home.html'):
    query = request.GET.get('search')
    events = Event.objects.all()
    if query:
        events = events.filter(name__icontains=query)
    paginator = Paginator(events, 5)
    page = request.REQUEST.get('page')
    if page:
        page = int(page)
    try:
        events = paginator.page(page)
    except:
        events = paginator.page(1)
    context = {
        'events' : events,
        'query' : query
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
    
def create_event(request, template='events/event_create.html'):
    saved = False
    ticket_forms = []
    ticket_prefixes = []
    ticket_number = 0
    if request.method == 'POST':
        tickets_valid = True
        ticket_prefixes = request.POST.get('ticket_prefixes')
        if ticket_prefixes:
            ticket_prefixes = ticket_prefixes.split(',')
            # get the ticket prefix of the possible next ticket form
            ticket_number = int(ticket_prefixes[-1]) + 1
            for ticket_prefix in ticket_prefixes:
                ticket_form = TicketForm(request.POST, prefix=ticket_prefix)
                if not ticket_form.is_valid():
                    tickets_valid = False
                ticket_forms.append(ticket_form)
        event_form = EventForm(request.POST, prefix='event')
        if event_form.is_valid() and tickets_valid:
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()
            for ticket_prefix in ticket_prefixes:
                ticket_form = TicketForm(request.POST, prefix=ticket_prefix)
                ticket = ticket_form.save(commit=False)
                ticket.event = event
                ticket.save()
            saved = True
        else:
            print 'THERE ARE SOME ERRORS!'
            print event_form.errors
            for form in ticket_forms:
                print form.errors
    else:
        event_form = EventForm(prefix='event')
    context = {
        'event_form' : event_form,
        'ticket_forms' : ticket_forms,
        'ticket_number' : ticket_number,
        'ticket_prefixes' : ticket_prefixes,
        'saved' : saved
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def create_ticket(request, template='events/event_create_ticket.html'):
    ticket_number = request.GET.get('ticket_number')
    #print 'TICKET NO: ', ticket_number
    ticket_form = TicketForm(prefix=ticket_number)
    context = {
        'ticket_form' : ticket_form,
        'ticket_number' : ticket_number
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

#------------------------------------ AUTH ------------------------------------
    
def login_user(request, template='events/login.html'):
    incorrect_data = False
    if request.method == 'POST':
        incorrect_data = True
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # check if user signed in using e-mail
            try:
                user = User.objects.get(email=username)
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return redirect('home')
            except User.DoesNotExist:
                pass
    else:
        form = LoginForm()
    context = {
        'form' : form,
        'incorrect_data' : incorrect_data
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def register_user(request, template='events/register.html'):
    user_exists = False
    saved = False
    if request.POST:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # create username from email substring
            username = email[0:email.index('@')]
            if User.objects.filter(username=username):
                # append a number to the username until a non-existing found
                count = 0
                while User.objects.filter(username=username):
                    count += 1
                    username = username + str(count)
            else:
                user = User()
                user.email = email
                user.set_password(password)
                user.username = username
                user.save()
                user = authenticate(username=user.username, password=password)
                login(request, user)
                saved = True
    else:
        form = RegisterForm()
    context = {
        'form' : form,
        'user_exists' : user_exists,
        'saved' : saved,
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        return redirect('home')
        