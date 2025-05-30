from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    BlogRecordListView,
    BlogRecordDetailView,
    BlogRecordCreateView,
    BlogRecordUpdateView,
    BlogRecordDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogRecordListView.as_view(), name="records_list"),
    path("record/<int:pk>/", BlogRecordDetailView.as_view(), name="record_detail"),
    path("create/", BlogRecordCreateView.as_view(), name="record_create"),
    path(
        "record/<int:pk>/update", BlogRecordUpdateView.as_view(), name="record_update"
    ),
    path(
        "record/<int:pk>/delete", BlogRecordDeleteView.as_view(), name="record_delete"
    ),
]
