from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from cart.cart import Cart
from store.models import Product

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'store/cart/summary.html', {'cart' : cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)# This line explained below
        #try:
        #   product = Product.objects.get(id = product_id)
        #except:
        #   raise Http404
        cart.add(product=product, qty=product_qty)
        cartqty = cart.__len__()
        response = JsonResponse({'qty' : cartqty})
        return response
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        cart.delete(product = product_id)
        cart_total = cart.get_total_price()
        cartqty = cart.__len__()
        response = JsonResponse({'qty' : cartqty, 'subtotal' : cart_total})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        #print(product_id)
        #print(product_qty)
        cart.update(product = product_id, qty = product_qty)
        cartqty = cart.__len__()
        cart_total = cart.get_total_price()
        #print(cart_total)

        response = JsonResponse({'qty' : cartqty, 'subtotal' : cart_total})
        return response