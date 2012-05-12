import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from cart import Cart as CartManager
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
    
def event(request, event_id=None, secret_url=None, template='events/event.html'):
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = get_object_or_404(Event, secret_url=secret_url)
    if request.method == 'POST':
        ticket_quantity = request.POST.get('ticket_quantity')
        if ticket_quantity:
            ticket_quantity = ticket_quantity.split(',')
            cart = CartManager(request)
            for t_q in ticket_quantity:
                t_q = t_q.split(':')
                ticket = Ticket.objects.get(pk=t_q[0])
                quantity = t_q[1]
                cart.add(ticket, quantity)
            return redirect('cart')
    context = {
        'event' : event
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def cart(request, clear=False, template='events/cart.html'):
    cart = CartManager(request)
    if clear:
        cart.clear()
        return redirect('home')
    context = {
        'cart' : cart,
        'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def cart_checkout(request, template='events/cart_checkout.html'):
    context = {}
    cart = CartManager(request)
    if request.method == 'POST':
        try:
            stripe.api_key = settings.STRIPE_PRIVATE_KEY
            # get the credit card details submitted by the form
            token = request.POST['stripeToken']
            # create the charge on Stripe's servers - this will charge the user's card
            charge = stripe.Charge.create(
                amount=int(cart.summary()*100), # amount in cents
                currency="usd",
                card=token,
                description=request.user.email
            )
            print charge
            if charge.get('paid'):
                cart.check_out()
                return HttpResponse('TRUE')
            return HttpResponse('FALSE')
        except:
            import traceback
            traceback.print_exc()
    
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
    
@login_required
def create_event(request, template='events/event_create.html'):
    event = None
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
        'event' : event
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
                        if request.GET.has_key('next'):
                            return redirect(request.GET['next'])
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
        