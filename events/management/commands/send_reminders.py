# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from events.models import Cart, TicketOrder, Event

class Command(BaseCommand):
    help = "Sends reminders to users who have acquired tickets for events that happen within the next 7 days."
    
    def handle(self, *args, **options):
        week_future = datetime.datetime.now() + datetime.timedelta(days=7)
        carts = Cart.objects.filter(checked_out=True)
        mail_list = []
        # TODO optimize and get rid of redundancy
        soon_events = Event.objects.filter(date_start__range=(datetime.datetime.now(),
                                                              week_future))
        soon_orders = TicketOrder.objects.filter(ticket__event__in=soon_events).distinct('ticket__event')
        print 'Soon orders:',soon_orders
        for order in soon_orders:
            event = order.ticket.event
            user = order.cart.user
            if user:
                subject = _(u'[Django Events] Event coming soon')
                message = """
                    Hey, just wanted to let you know the event you bought the
                    tickets for is coming soon.\n
                    Event name: %s
                    Starts at:  %s\n
                    Take care,
                    Django Events
                """ % (event.name, event.date_start)
                send_mail(subject, message, 'noreply@django-events.com', [user.email])
                