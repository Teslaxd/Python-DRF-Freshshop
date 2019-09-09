import django_filters


class OrderFilter(django_filters.rest_framework.FilterSet):

    o_status = django_filters.CharFilter(method='filter_status')

    def filter_status(self, queryset, name, value):
        if value == 'not_pay':
            return queryset.filter(o_status=0)
        elif value == 'not_send':
            return queryset.filter(o_status=2)
        else:
            return queryset





