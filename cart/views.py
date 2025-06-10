from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse,HttpResponseBadRequest
import logging
from django.contrib import messages
from django.urls import reverse


def cart_summary(request):
    cart=Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    return render(request,"cart_summary.html",{"cart_products":cart_products,"quantities": quantities,"totals":totals})
def cart_add(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))
        product=get_object_or_404(Product,id=product_id)
        cart.add(product=product,quantity=product_qty)
        cart_quantity=cart.__len__()
        response=JsonResponse({'qty':cart_quantity})
        messages.success(request,("Product added to the cart"))
        return response
logger = logging.getLogger(__name__)    
def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        logger.debug(f"Received product_id: {product_id}")
        if not product_id :
            logger.error("Product ID is required")
            return HttpResponseBadRequest("Product ID is required.")
        try:
            product_id = int(product_id)
        except ValueError:
            logger.error("Invalid product ID .")
            return HttpResponseBadRequest("Invalid product ID ")    

        cart.delete(product_id)
        response = JsonResponse({'product': product_id})
        messages.success(request,("Item Deleted From Shopping Cart"))
        return response
    else:
        logger.error("Invalid request method or action.")
        return HttpResponseBadRequest("Invalid request method or action.")

logger = logging.getLogger(__name__)

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        # Log the received values
        logger.debug(f"Received product_id: {product_id}, product_qty: {product_qty}")

        if not product_id or not product_qty:
            logger.error("Product ID and quantity are required.")
            return HttpResponseBadRequest("Product ID and quantity are required.")

        try:
            product_id = int(product_id)
            product_qty = int(product_qty)
        except ValueError:
            logger.error("Invalid product ID or quantity.")
            return HttpResponseBadRequest("Invalid product ID or quantity.")

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        messages.success(request,("Your Cart has been updated"))
        return response
    else:
        logger.error("Invalid request method or action.")
        return HttpResponseBadRequest("Invalid request method or action.")

