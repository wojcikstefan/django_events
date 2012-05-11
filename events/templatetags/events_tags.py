import datetime

from django import template
from django.utils.translation import ugettext_lazy as _

from events.models import Cart

register = template.Library()

@register.simple_tag()
def count_sold_tickets():
    # TODO might be optimized, for instance by caching
    total_count = 0
    carts = Cart.objects.filter(checked_out=True)
    for cart in carts:
        for order in cart.ticketorder_set.all():
            total_count += order.quantity
    return total_count
    
@register.filter()
def time_left(time):
    delta = time - datetime.datetime.now()
    if delta.days < 0:
        return None
    if delta.days > 1:
        return u'%s %s' % (delta.days, _(u'days'))
    elif delta.seconds/3600 > 1:
        return u'%s %s' % (delta.seconds/3600, _(u'hours'))
    else:
        return u'%s %s' % (delta.seconds/60, _(u'minutes'))
    