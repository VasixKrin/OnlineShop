from django.urls import path

from payment import views, webhook

app_name = 'payment'

urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name='process'),
    path('completed/', views.PaymentCompletedTemplateView.as_view(), name='completed'),
    path('canceled/', views.PaymentCanceledTemplateView.as_view(), name='canceled'),
    path('webhook/', webhook.stripe_webhook, name='stripe_webhook')
]