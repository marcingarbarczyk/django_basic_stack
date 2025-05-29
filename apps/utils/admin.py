from django.contrib import admin


class SearchableRelatedFieldListFilter(admin.RelatedFieldListFilter):
    template = 'admin/searchable_related_field_list_filter.html'
