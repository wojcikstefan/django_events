import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to='event_logos', null=True, blank=True,
                             verbose_name=_('Event logo'))
    name = models.CharField(max_length=256, verbose_name=_('Event name'))
    date_start = models.DateTimeField(verbose_name=_('Event start'))
    date_end = models.DateTimeField(verbose_name=_('Event end'))
    # preferrably changed to geo-location later
    location = models.CharField(max_length=128, verbose_name=_('Event location')) 
    description = models.TextField(verbose_name=_('Event details'))
    private = models.BooleanField(default=False, verbose_name=_('Event is private'))
    secret_url = models.CharField(max_length=40, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('date_start',)
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.private:
            key = self.created_by.email+str(self.created_at)+self.name
            self.secret_url = sha_constructor(key).hexdigest()
        super(Event, self).save(*args, **kwargs)
    
class Ticket(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=64)
    # if quantity is null, the number of available tickets is unlimited
    quantity = models.PositiveIntegerField(null=True, blank=True)
    # number of tickets that can be bought at once, null = unlimited
    quantity_limit = models.PositiveIntegerField(null=True, blank=True)
    price = models.FloatField()
    sales_start = models.DateTimeField(null=True, blank=True)
    sales_end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        
    def __unicode__(self):
        return _(u'Ticket for ') + unicode(self.event.name)
        
    def quantity_range(self):
        if self.quantity_limit:
            return range(0,self.quantity_limit+1,1)
        else:
            return range(0,self.quantity+1,1)
            
    def tickets_left(self):
        if not self.quantity:
            return -1
        else:
            quantity = 0
            # TODO Change to aggregate
            checked_orders = TicketOrder.objects.filter(ticket=self, cart__checked_out=True)
            for order in checked_orders:
                quantity += order.quantity
            return self.quantity - quantity
            
    def sold_out(self):
        if self.quantity:
            quantity = 0
            # TODO Change to aggregate
            checked_orders = TicketOrder.filter(ticket=self, cart__checked_out=True)
            for order in checked_orders:
                quantity += order.quantity
            if quantity >= self.quantity:
                return True
        return False
            
    def sales_started(self):
        if self.sales_start:
            return self.sales_start > datetime.datetime.now()
        else:
            return True
            
    def sales_finished(self):
        if self.sales_end:
            return self.sales_end < datetime.datetime.now()
        else:
            return self.event.date_end < datetime.datetime.now()
    
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
