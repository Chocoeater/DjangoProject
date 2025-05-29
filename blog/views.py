from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from blog.models import BlogRecord
# Create your views here.

class BlogRecordListView(ListView):
    model = BlogRecord
    template_name = 'records_list.html'
    context_object_name = 'records'
    paginate_by = 3

class BlogRecordDetailView(DetailView):
    pass

class BlogRecordCreateView(CreateView):
    pass

class BlogRecordUpdateView(UpdateView):
    pass

class BlogRecordDeleteView(DeleteView):
    pass

