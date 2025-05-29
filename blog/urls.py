from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogRecordListView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogRecordListView.as_view(), name='records_list'),

]