from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
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
    
def login_user(request, template='events/login.html'):
    incorrect_data = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # check if user signed in using e-mail instead of username
            if user is None:
                try:
                    user = User.objects.get(email=username)
                    user = authenticate(username=user.username, password=password)
                except:
                    pass
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('home')
            else:
                incorrect_data = True
    else:
        form = LoginForm()
    context = {
        'form' : form,
        'incorrect_data' : incorrect_data
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    
def register_user(request, template='auth/register2.html'):
    user_exists = False
    saved = False
    if request.POST:
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            profile_type = form.cleaned_data['profile_type']
            email = form.cleaned_data['email']
            username = email[0:email.index('@')]
            if User.objects.filter(email=email):
                user_exists = True
            elif User.objects.filter(username=username):
                count = 0
                while User.objects.filter(username=username):
                    count += 1
                    username = username + str(count)
            else:
                user = User()
                user.email = email
                user.set_password(form.cleaned_data['password'])
                user.username = username
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.is_active = False
                user.save()
                profile = Profile()
                profile.user = user
                profile.type = profile_type
                salt = sha_constructor(str(random.random())).hexdigest()[:5]
                activation_key = sha_constructor(salt+user.username).hexdigest()
                profile.activation_key = activation_key
                profile.save()
                saved = True
                activation_link = '%s/user/activate/%s/' % (request.get_host(),
                                                            activation_key)
                if profile.type == 'ART':
                    artist = Artist(profile=profile)
                    artist.test1 = form.cleaned_data['file1']
                    artist.test2 = form.cleaned_data['file2']
                    artist.test3 = form.cleaned_data['file3']
                    artist.test4 = form.cleaned_data['file4']
                    artist.test5 = form.cleaned_data['file5']
                    artist.save()
                       
                dane = form.cleaned_data
                template = 'emails/potw_rejestracji.txt'
                tresc = loader.get_template(template).render(
                    Context({'dane': dane, 'activation_link':activation_link}))
                send_mail('Potwierdzenie rejestracji', tresc,
                          settings.EMAIL_HOST, [dane['email']])
                return HttpResponse('OK')
    else:
        form = RegisterForm()
    
    context = {
        'form' : form,
        'user_exists' : user_exists,
        'saved' : saved,
        'error_type' : request.POST.get('profile_type') # for tab opening in case of error
    }
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    if request.GET.get('next'):
        return HttpResponseRedirect(request.GET['next'])
    else:
        return redirect('home')