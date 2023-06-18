from django.shortcuts import render,get_object_or_404, redirect

from .models import Product, Category, Order
from .cart import Cart
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def catalog_view(request):
    sort_by = request.GET.get('sort', 'newest')
    category = request.GET.get('category', '')

    if sort_by == 'name':
        products = Product.objects.order_by('name')
    elif sort_by == 'price':
        products = Product.objects.order_by('price')
    else:
        products = Product.objects.order_by('-id')  # Newest

    if category:
        products = products.filter(category__name=category)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
        'selected_sort': sort_by,
    }
    return render(request, 'catalog.html', context)

def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})


def cart(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()

    # Получите полные объекты товаров из базы данных на основе их product_id
    products = Product.objects.filter(id__in=[item['product_id'] for item in cart_items])

    # Создайте словарь, содержащий информацию о товаре и его количестве
    cart_items_with_products = []
    for item in cart_items:
        product = products.get(id=item['product_id'])
        cart_items_with_products.append({
            'product': product,
            'quantity': item['quantity']
        })

    context = {
        'cart_items': cart_items_with_products,
        'cart_total': cart.get_cart_total
    }
    
    if request.method == 'POST':
        password = request.POST.get('password')  # Get the entered password from the request

        user = authenticate(request, username=request.user.username, password=password)
        if user is None:
            # Password authentication failed, handle the error or redirect back to the cart page
            return HttpResponse('Invalid password')

        order = Order(user=user, quantity=cart.get_cart_total(), status='New')
        order.save()

        # Добавьте продукты в заказ
        for item in cart.get_cart_items():
            product = Product.objects.get(id=item['product_id'])
            order.products.add(product, through_defaults={'quantity': item['quantity']})

        # Очистите корзину после создания заказа
        cart.clear()

        # Redirect to a success page or display a success message
        return HttpResponse('Order created successfully')

    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    # Retrieve the product based on the given product_id
    product = Product.objects.get(id=product_id)

    # Create or retrieve the cart for the current user
    cart = Cart(request)

    # Add the product to the cart
    cart.add(product=product)

    return redirect('cart')  


@login_required
def checkout(request):
    if request.method == 'POST':
        password = request.POST.get('password')  # Получите введенный пароль из запроса

        user = authenticate(request, username=request.user.username, password=password)
        if user is None:
            messages.error(request, 'Пароль введен неправильно. В случае логина через администратора использовать пароль админа.')
            return redirect('cart') 

        # Пароль прошел аутентификацию, создайте и сохраните заказ
        cart = Cart(request)
        order = Order(user=user, total=cart.get_cart_total(), status='New')
        order.save()

        # Добавьте продукты в заказ
        for item in cart.get_cart_items():
            product = Product.objects.get(id=item['product_id'])
            order.products.add(product, through_defaults={'quantity': item['quantity']})

        # Очистите корзину после создания заказа
        cart.clear()

         # Сохраните состояние корзины в сессии
        request.session['cart'] = {}

        return redirect('cart') 

    # Если запрос не POST, перенаправьте пользователя на страницу корзины или отобразите сообщение об ошибке
    return HttpResponse('Invalid request')

def order_list(request):
    user = request.user


    orders = Order.objects.filter(user=user).order_by('-id')

    context = {'orders': orders}
    return render(request, 'orders.html', context)


def remove_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order_list')


def decrease_quantity_in_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)

    cart.decrease_quantity(product, 1)
   
    return redirect('cart')

def increase_quantity_in_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)

    cart.increase_quantity(product, 1)
   
    return redirect('cart')


def about(request):
    latest_products = Product.objects.order_by('-id')[:5]
    context = {'latest_products': latest_products}
    return render(request, 'about.html', context)