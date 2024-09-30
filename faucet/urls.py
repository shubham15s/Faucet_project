# faucet/urls.py
from django.urls import path
from .views import fund_faucet, faucet_stats

urlpatterns = [
    path('fund', fund_faucet, name='fund_faucet'),
    path('stats', faucet_stats, name='faucet_stats'),
]
