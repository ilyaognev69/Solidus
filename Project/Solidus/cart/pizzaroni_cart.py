from decimal import Decimal
from django.conf import settings
from navigator.models import Pizzaroni

class PizzaroniCart(object):
    
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
                self.cart[product_id] = {'quantity':0, 
                                         'price': str(product.price)}
            
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        
    def save(self):
        self.session.modified = True
        
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
            
    def __iter__(self):
        product_ids = self.cart.keys()
        cart = self.cart.copy()
            
        market_products = Pizzaroni.objects.filter(id__in=product_ids)
        for product in market_products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            if 'price' in item:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item
            

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        summa = 0
        for item in self.cart.values():
            if 'price' in item:
                summa+=(Decimal(item['price']) * item['quantity'])
        return summa
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()