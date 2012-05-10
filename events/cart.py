import datetime
import models

CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request):
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.ticketorder_set.all():
            yield item

    def new(self, request):
        cart = models.Cart()
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, ticket, quantity=1):
        try:
            order = models.TicketOrder.objects.get(
                cart=self.cart,
                ticket=ticket,
            )
        except models.TicketOrder.DoesNotExist:
            order = models.TicketOrder()
            order.cart = self.cart
            order.ticket = ticket
            order.quantity = quantity
            order.save()
        else: #ItemAlreadyExists
            order.unit_price = unit_price
            order.quantity = order.quantity + int(quantity)
            order.save()

    def remove(self, ticket):
        try:
            order = models.Item.objects.get(
                cart=self.cart,
                ticket=ticket,
            )
        except models.TicketOrder.DoesNotExist:
            raise ItemDoesNotExist
        else:
            order.delete()

    def update(self, ticket, quantity):
        try:
            order = models.TicketOrder.objects.get(
                cart=self.cart,
                ticket=ticket,
            )
        except models.TicketOrder.DoesNotExist:
            raise ItemDoesNotExist
            
    def count(self):
        result = 0
        for order in self.cart.ticketorder_set.all():
            result += 1 * order.quantity
        return result
        
    def summary(self):
        result = 0
        for order in self.cart.ticketorder_set.all():
            result += order.total_price
        return result

    def clear(self):
        for order in self.cart.ticketorder_set.all():
            order.delete()
