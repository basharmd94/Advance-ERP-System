from django.shortcuts import render
from django.http import HttpResponse


def inventory_items(request):
    return HttpResponse("Inventory Items")
