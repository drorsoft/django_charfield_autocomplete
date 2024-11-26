from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, reverse
from django.db.models import Q
from functools import reduce
from operator import or_
from django.conf import settings


class AutocompleteAdminMixin:
    class Media:
        js = ('admin_autocomplete/js/autocomplete.js',)
        css = {
            'all': ('admin_autocomplete/css/autocomplete.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'autocomplete/',
                self.admin_site.admin_view(self.autocomplete_view),
                name='autocomplete',
            ),
        ]
        return custom_urls + urls

    def autocomplete_view(self, request):
        """Handle AJAX requests for autocomplete suggestions."""
        term = request.GET.get('term', '')
        
        # Get settings or use defaults
        admin_settings = getattr(settings, 'ADMIN_AUTOCOMPLETE', {})
        min_chars = admin_settings.get('MIN_CHARS', 2)
        max_results = admin_settings.get('MAX_RESULTS', 10)

        if len(term) < min_chars:
            return JsonResponse({'results': []})

        # Build search query
        if not self.search_fields:
            return JsonResponse({'results': []})

        queryset = self.model.objects.all()
        search_queries = []
        
        for field in self.search_fields:
            search_queries.append(Q(**{f"{field}__icontains": term}))

        queryset = queryset.filter(reduce(or_, search_queries))
        queryset = queryset[:max_results]

        results = [
            {
                'id': str(obj.pk),
                'text': str(obj),
                'url': reverse(
                    f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change',
                    args=[obj.pk]
                )
            }
            for obj in queryset
        ]

        return JsonResponse({'results': results})
