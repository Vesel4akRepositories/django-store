from django.urls import path
from .views import catalog_view, product_view,cart,add_to_cart,checkout,order_list,remove_order,decrease_quantity_in_cart,increase_quantity_in_cart,about
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('catalog/', catalog_view, name='catalog'),
    path('about/', about, name='about'),
    path('product/<int:product_id>/', product_view, name='product'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_list, name='orders'),
    path('orders/remove/<int:order_id>/', remove_order, name='remove_order'),
    path('decrease_quantity/<int:product_id>/', decrease_quantity_in_cart, name='decrease_quantity'),
    path('increase_quantity/<int:product_id>/', increase_quantity_in_cart, name='increase_quantity'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

