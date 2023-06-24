from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApacheLogViewSet, LogsAPIView, logs_view

router = DefaultRouter()
router.register(r'apachelogs', ApacheLogViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/logs/', LogsAPIView.as_view(), name='api-logs'),
    path('logs/', logs_view, name='logs-view' )
]
