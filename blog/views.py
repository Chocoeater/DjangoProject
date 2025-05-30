from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from blog.models import BlogRecord
from django.urls.base import reverse_lazy, reverse
from blog.forms import BlogRecordForm

# Create your views here.


class BlogRecordListView(ListView):
    model = BlogRecord
    template_name = "records_list.html"
    context_object_name = "records"
    paginate_by = 3

    def get_queryset(self):
        self.queryset = super().get_queryset()
        new_queryset = [x for x in self.queryset if x.publication is True]
        return new_queryset


class BlogRecordDetailView(DetailView):
    model = BlogRecord
    template_name = "record_detail.html"
    context_object_name = "record"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()

        if self.object.number_of_views == 100:
            send_mail(
                subject="Поздравляем!",
                message=f"Статья {self.object.title} просмотрели 100 раз!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["kourdackov@yandex.ru"],
                fail_silently=False,
            )

        return self.object


class BlogRecordCreateView(CreateView):
    model = BlogRecord
    template_name = "record_create.html"
    form_class = BlogRecordForm
    success_url = reverse_lazy("blog:records_list")


class BlogRecordUpdateView(UpdateView):
    model = BlogRecord
    template_name = "record_update.html"
    form_class = BlogRecordForm

    def get_success_url(self):
        return reverse("blog:record_detail", kwargs={"pk": self.object.pk})


class BlogRecordDeleteView(DeleteView):
    model = BlogRecord
    template_name = "record_delete.html"
    success_url = reverse_lazy("blog:records_list")
