# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from events.models import Cart, TicketOrder, Event

class Command(BaseCommand):
    help = "Sends reminders to users who have acquired tickets for events that happen within the next 7 days."
    
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        future = now + datetime.timedelta(days=settings.REMINDER_DAYS)
        mail_list = []
        # TODO optimize (some helper db table perhaps?)
        soon_events = Event.objects.filter(date_start__range=(now, future))
        for event in soon_events:
            ticket_orders = TicketOrder.objects.filter(ticket__event=event)
            emails = ticket_orders.values_list('cart__user__email').distinct()
            emails = [e[0] for e in emails]
            # remove duplicates
            d = {}
            for e in emails:
                d[e] = 1
            emails = list(d.keys())
            subject = _(u'[Django Events] Event coming soon')
            message = """
                Hey, just wanted to let you know the event you bought the
                tickets for is coming soon.\n
                Event name: %s
                Starts at:  %s\n
                Take care,
                Django Events
            """ % (event.name, event.date_start)
            send_mail(subject, message, 'noreply@django-events.com', emails)
    