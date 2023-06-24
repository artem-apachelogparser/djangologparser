from django.db import models

from django.db.models import Count

class ApacheLog(models.Model):
    host = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    time = models.DateTimeField()
    request = models.TextField()
    status = models.IntegerField()
    size = models.BigIntegerField()
    referer = models.TextField()
    user_agent = models.TextField()

    @classmethod
    def logs_by_host(cls):
        return cls.objects.values('host').annotate(count=Count('host'))

    @classmethod
    def logs_by_date(cls):
        return cls.objects.extra({'date': "date(time)"}).values('date').annotate(count=Count('id'))

    @classmethod
    def logs_by_time_range(cls, start_date=None, end_date=None):
        if start_date is None:
            start_date = datetime.now() - timedelta(days=7)
        if end_date is None:
            end_date = datetime.now()
        return cls.objects.filter(time__range=(start_date, end_date))
