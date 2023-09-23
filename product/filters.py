from .models import Product
import django_filters

class ProductFilter(django_filters.FilterSet):

    area = django_filters.RangeFilter()
    height = django_filters.RangeFilter()
    width = django_filters.RangeFilter()
    stitch = django_filters.RangeFilter()
    needle = django_filters.RangeFilter()
    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['price', 'area','height','width','stitch','needle']