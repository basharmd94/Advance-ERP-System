from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from web_project import TemplateLayout
from apps.authentication.mixins import ZidRequiredMixin
from apps.authentication.mixins import ModulePermissionMixin
from ..models.caitem import Caitem
import logging

logger = logging.getLogger(__name__)


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class ItemsView(ZidRequiredMixin, ModulePermissionMixin, TemplateView):
    module_code = 'crossapp_items'
    template_name = 'items.html'
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


@login_required
def get_items_json(request):
    """Get items list with specific columns as JSON"""
    try:
        # Get current ZID from session
        current_zid = request.session.get('current_zid')
        if not current_zid:
            return JsonResponse({'error': 'No business context found'}, status=400)

        # Query items for the current ZID with specific fields
        items = Caitem.objects.filter(zid=current_zid).values(
            'xitem',      # Item Code
            'xdesc',      # Description
            'xgitem',     # Item Group
            'xwh',        # Warehouse
            'xstdcost',   # Standard Cost
            'xstdprice',  # Standard Price
            'xunitstk'    # Stock Unit
        )

        # Convert Decimal fields to string for JSON serialization
        items_list = list(items)
        for item in items_list:
            if item['xstdcost']:
                item['xstdcost'] = str(item['xstdcost'])
            if item['xstdprice']:
                item['xstdprice'] = str(item['xstdprice'])

        return JsonResponse({'items': items_list}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def delete_item_api(request, item_code):
    """Delete an existing item"""
    
    if request.method != 'POST':
        logger.warning(f"Invalid method {request.method} for item deletion by user: {request.user.username}")
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    try:
        # Get current ZID from session
        current_zid = request.session.get('current_zid')

        try:
            queryset = Caitem.objects.filter(zid=current_zid, xitem=item_code)
            item = queryset.first()
            if not item:
                logger.warning(f"Item not found for deletion: {item_code} for business: {current_zid}")
                return JsonResponse({'error': 'Item not found'}, status=404)
            logger.debug(f"Found item to delete: zid={item.zid}, xitem={item.xitem}")
        except Caitem.DoesNotExist:
            logger.warning(f"Item not found for deletion: {item_code} for business: {current_zid}")
            return JsonResponse({'error': 'Item not found'}, status=404)
        
        item_name = item.xdesc or item.xitem
        logger.debug(f"Deleting item {item_name} (code: {item_code}) for business: {current_zid} by user: {request.user.username}")
        
        # Use a specific delete query to ensure only one record is deleted
        deleted_count = Caitem.objects.filter(
            zid=current_zid,
            xitem=item_code
        ).delete()
        
        logger.info(f"Item deleted successfully: {item_name} (code: {item_code}) for business: {current_zid} by user: {request.user.username}")
        
        return JsonResponse({
            'success': True,
            'message': 'Item deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)} for user: {request.user.username}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)