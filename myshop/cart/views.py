from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.decorators.http import require_POST
from django.contrib import messages

from .cart import Cart
from .forms import CartAddProductForm
from ..shop.models import Product

@method_decorator(require_POST, name='dispatch')
class AddToCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product,
                quantity=cd['quantity'],
                override_quantity=cd['override']
            )
        messages.success(request, 'The product added successfully to your cart.')
        return redirect('cart:cart_detail')


@method_decorator(require_POST, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartTemplateView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
