import logging
from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.authentication.mixins import ZidRequiredMixin
from apps.authentication.mixins import ModulePermissionMixin


# Get logger for this module
logger = logging.getLogger(__name__)

class ItemLedgerView(ZidRequiredMixin, ModulePermissionMixin, TemplateView):
    module_code = 'inventory_reports_item_ledger'
    template_name = 'item_ledger.html'
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
