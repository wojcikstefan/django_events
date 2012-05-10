from django import template

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
    