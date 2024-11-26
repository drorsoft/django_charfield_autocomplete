from django.http import JsonResponse
from django.contrib import admin
from django.db.models import Q
from django.urls import reverse


def admin_autocomplete(request):
    """Handle AJAX requests for admin autocomplete."""
    term = request.GET.get('term', '')
    if len(term) < 2:
        return JsonResponse({'results': []})

    # Get the model from the current admin site
    model = None
    for model_cls, model_admin in admin.site._registry.items():
        if model_cls._meta.app_label == 'testapp' and model_cls._meta.model_name == 'book':
            model = model_cls
            break

    if not model:
        return JsonResponse({'results': []})

    # Get the admin class
    model_admin = admin.site._registry[model]
    queryset = model_admin.get_queryset(request)
    search_fields = model_admin.search_fields

    if not search_fields:
        return JsonResponse({'results': []})

    # Build search query
    queries = [Q(**{f"{field}__icontains": term}) for field in search_fields]
    query = queries.pop()
    for item in queries:
        query |= item

    # Limit results
    results = queryset.filter(query).distinct()[:10]

    # Format results
    formatted_results = []
    for obj in results:
        change_url = reverse(
            f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
            args=[obj.pk]
        )
        formatted_results.append({
            'text': str(obj),
            'url': change_url
        })

    return JsonResponse({'results': formatted_results})
