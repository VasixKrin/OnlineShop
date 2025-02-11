from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created


class OrderCreateView(View):
    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(
            request,
            'orders/order/create.html',
            {'cart': cart, 'form': form}
        )

    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                ) for item in cart
            ])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
