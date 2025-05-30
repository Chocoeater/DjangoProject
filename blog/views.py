from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from blog.models import BlogRecord
from django.urls.base import reverse_lazy, reverse
from blog.forms import BlogRecordForm
# Create your views here.

class BlogRecordListView(ListView):
    model = BlogRecord
    template_name = 'records_list.html'
    context_object_name = 'records'
    paginate_by = 3

class BlogRecordDetailView(DetailView):
    model = BlogRecord
    template_name = 'record_detail.html'
    context_object_name = 'record'

class BlogRecordCreateView(CreateView):
    model = BlogRecord
    template_name = 'record_create.html'
    form_class = BlogRecordForm
    success_url = reverse_lazy('blog:records_list')

class BlogRecordUpdateView(UpdateView):
    model = BlogRecord
    template_name = 'record_update.html'
    form_class = BlogRecordForm

    def get_success_url(self):
        return reverse('blog:record_detail', kwargs={'pk': self.object.pk})

class BlogRecordDeleteView(DeleteView):
    model = BlogRecord
    template_name = 'record_delete.html'
    success_url = reverse_lazy('blog:records_list')
