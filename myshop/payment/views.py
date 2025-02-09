from decimal import Decimal
import stripe
from django.contrib.messages import success
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View, TemplateView
from requests import session

from orders.models import Order

# create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentProcessView(View):
    def get_order(self, request):
        order_id = request.session.get('order_id')
        return get_object_or_404(Order, id=order_id)

    def get(self, request):
        order = self.get_order(request)
        return render(request, 'payment/process.html', order)

    def post(self, request):
        order = self.get_order(request)
        success_url = request.build_absolute_uri(
            reverse('payment:complete')
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:cancel')
        )
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    "price_data": {
                        'unit_amount': int(item.price * Decimal('100')),
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                    },
                    'quantity': item.quantity,
                }
            )
        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to Stripe payment form
        return redirect(session.url, code=303)

class PaymentCompletedTemplateView(TemplateView):
    template_name = 'payment/completed.html'

class PaymentCanceledTemplateView(TemplateView):
    template_name = 'payment/canceled.html'
