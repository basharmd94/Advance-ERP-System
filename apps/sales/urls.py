from django.urls import path
from .views.pos_sales import SalesView


urlpatterns = [
    # Sales Management URLs
    path(
        "pos-sales/",
        SalesView.as_view(template_name="pos_sales.html"),
        name="pos-sales",
    ),
    

]
