from django.urls import path
from .views.item_ledger import ItemLedgerView

urlpatterns = [
    # path('', inventory_items, name='inventory-items'),
    path('reports/item-ledger/', ItemLedgerView.as_view(), name='reports-item-ledger'),
]
