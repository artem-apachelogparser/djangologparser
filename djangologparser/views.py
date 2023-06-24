from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, views
from .serializers import ApacheLogSerializer
from rest_framework.response import Response
from .models import ApacheLog
from django.db.models import Count
from datetime import datetime, timedelta
from django.utils import timezone

start_date = timezone.now() - timedelta(days=7)
end_date = timezone.now()

class ApacheLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Apache logs to be viewed or edited.
    """
    queryset = ApacheLog.objects.all().order_by('-time')
    serializer_class = ApacheLogSerializer


class LogsAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        logs_by_host = ApacheLog.objects.values('host').annotate(count=Count('host'))
        logs_by_date = ApacheLog.objects.extra({'date': "date(time)"}).values('date').annotate(count=Count('id'))
        logs_by_time_range = ApacheLog.objects.filter(time__range=(start_date, end_date))

        return Response({
            'logs_by_host': logs_by_host,
            'logs_by_date': logs_by_date,
            'logs_by_time_range': logs_by_time_range
        })

    def get(self, request, *args, **kwargs):
        ip = request.GET.get('ip', None)
        # Преобразование строк из параметров запроса в объекты datetime
        start_date_str = request.GET.get('start_date', None)
        end_date_str = request.GET.get('end_date', None)
        if start_date_str is not None:
            start_date = parse_datetime(start_date_str)
        else:
            start_date = timezone.now() - timedelta(days=7)
        if end_date_str is not None:
            end_date = parse_datetime(end_date_str)
        else:
            end_date = timezone.now()
        if ip is not None:
            logs_by_host = list(ApacheLog.objects.filter(host=ip).values('host').annotate(count=Count('host')))
            logs_by_date = list(ApacheLog.objects.filter(host=ip).extra({'date': "date(time)"}).values('date').annotate(
                count=Count('id')))
            logs_by_time_range = list(ApacheLog.objects.filter(host=ip, time__range=(start_date, end_date)).values())

        else:
            logs_by_host = ApacheLog.objects.values('host').annotate(count=Count('host'))
            logs_by_date = ApacheLog.objects.extra({'date': "date(time)"}).values('date').annotate(count=Count('id'))
            logs_by_time_range = ApacheLog.objects.filter(time__range=(start_date, end_date))

        return Response({
            'logs_by_host': logs_by_host,
            'logs_by_date': logs_by_date,
            'logs_by_time_range': logs_by_time_range
        })

def logs_view(request):
    logs_by_host = ApacheLog.logs_by_host()
    print(logs_by_host)
    logs_by_date = ApacheLog.logs_by_date()
    print(logs_by_date)
    logs_by_time_range = ApacheLog.logs_by_time_range(start_date, end_date)
    print(logs_by_time_range)
    return render(request, 'logs.html', {
        'logs_by_host': logs_by_host,
        'logs_by_date': logs_by_date,
        'logs_by_time_range': logs_by_time_range
    })



