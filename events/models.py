from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    created_by = models.ForeignKey(User)
    name = models.CharField(max_length=256)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    sales_end = models.DateTimeField()
    location = models.CharField(max_length=128) # preferrably changed to geo-location later
    description = models.TextField()
    private = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('date_start',)
        
    def __unicode__(self):
        return self.name
    
class Ticket(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=64)
    description = models.TextField()
    available_quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.FloatField()
    
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
    
class Cart(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True,
                                         verbose_name=_('Creation date'))
    checked_out = models.BooleanField(default=False,
                                      verbose_name=_('Checked out'))

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')
        ordering = ('-creation_date',)

    def __unicode__(self):
        return unicode(self.creation_date)
    
class TicketOrder(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    ticket = models.ForeignKey(Ticket, verbose_name = _('Ticket'))
    
    #objects = ItemManager()

    class Meta:
        verbose_name = _('Ticket Order')
        verbose_name_plural = _('Ticket Orders')
        ordering = ('cart',)

    def __unicode__(self):
        return u'%d tickets (%s) for %s' % (self.quantity, self.ticket.name,
                                            self.ticket.event.name)

    def total_price(self):
        return self.quantity * self.ticket.price
    total_price = property(total_price)
