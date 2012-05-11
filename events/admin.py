from django.contrib import admin
from models import *

admin.site.register(Event)
admin.site.register(Ticket, list_display=('__unicode__', 'name', 'price'))
