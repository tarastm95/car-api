
from apps.cars.choices import BodyTypeChoice
from apps.cars.models import CarModel

from django_filters import rest_framework as filters


class CarFilter(filters.FilterSet):
    lt = filters.NumberFilter('year','lt')
    range = filters.RangeFilter('year')
    year_in = filters.BaseInFilter('year')
    body_type = filters.ChoiceFilter('body_type', choices=BodyTypeChoice.choices)
    model_endwith = filters.CharFilter('model', 'endswith')
    order = filters.OrderingFilter(
        fields=(
            'id',
            'model',
            ('price', 'asd')
        )
    )


