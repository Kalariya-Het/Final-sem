import django_filters
from django_filters import DateFilter,CharFilter
from .models import Attendance

class AttendenceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude=['inst','dept','in_time','out_time']