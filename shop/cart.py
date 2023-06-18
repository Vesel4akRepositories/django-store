from .models import Product
from django.contrib.auth import authenticate
from django.http import HttpResponse
from .models import Order

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in self.session or not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1}
        else:
            self.cart[product_id]['quantity'] += 1
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.cart = {}
        self.save()

    def get_cart_items(self):
        cart_items = []
        for product_id, item in self.cart.items():
            cart_items.append({
                'product_id': product_id,
                'quantity': item['quantity']
            })
        return cart_items

    def get_cart_total(self):
        total = 0
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            total += item['quantity'] * product.price
        return total

    def get_product_quantity(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        return 0

    def decrease_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= quantity
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()
    
    def increase_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
            self.save()

    
    