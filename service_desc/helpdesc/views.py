from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Request, Comment, Event
from .forms import RequestCreateForm, CommentCreateForm, StatusUpdateForm, ResolutionUpdateForm
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from .api.serializers import RequestSerializer
from rest_framework.pagination import PageNumberPagination


class RequestList(ListView, LoginRequiredMixin):
    model = Request
    paginate_by = 100
    ordering = ['-date_last_update']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user).filter(flag_delete=False)
        return queryset

    def get_template_names(self):
        if self.request.user.is_staff:
            return ['helpdesc/admin_panel.html']
        return ['helpdesc/index.html']


class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    success_url = '/'
    form_class = RequestCreateForm
    template_name = 'helpdesc/request_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        Event.create_event(self.object.user, self.object, '1', timezone.now())
        return super().form_valid(form)


class RequestUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    form_class = RequestCreateForm
    template_name = 'helpdesc/request_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comment_set.all()
        context.update({
            'comments': comments,
            'comment_create_form': CommentCreateForm,
            'status_update_form': StatusUpdateForm
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.date_last_update = timezone.now()
        self.object.save()
        Event.create_event(self.object.user, self.object, '1', timezone.now())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_detail_url', kwargs={'pk': self.object.pk})


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = ['post']
    form_class = CommentCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.request = Request.objects.get(pk=self.request.POST.get("request"))
        Event.create_event(self.object.user, self.object.request, '3', timezone.now())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_detail_url', kwargs={'pk': self.object.request.pk})


class StatusUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    http_method_names = ['post']
    success_url = '/'
    form_class = StatusUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.date_last_update = timezone.now()
        self.object.status = self.request.POST.get("status_resolution", "1")
        if self.object.status == "4":
            self.object.flag_reopen = True
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_detail_url', kwargs={'pk': self.object.pk})


class ResolutionUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    http_method_names = ['post']
    success_url = '/'
    form_class = ResolutionUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.date_last_update = timezone.now()
        self.object.status = "3"
        self.object.resolution = self.request.POST.get("request_resolution")
        if self.object.flag_reopen and self.object.resolution == "2":
            self.object.flag_delete = True
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('request_detail_url', kwargs={'pk': self.object.pk})


class RequestDetail(LoginRequiredMixin, DetailView):
    model = Request
    success_url = '/'
    template_name = 'helpdesc/request_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comment_set.all()
        context.update({
            'comments': comments,
            'comment_create_form': CommentCreateForm,
            'status_update_form': StatusUpdateForm,
            'resolution_update_form': ResolutionUpdateForm
        })
        return context


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        priority = str(self.request.query_params.get('priority')).lower()
        if priority in ['1', '2' , '3']:
            return qs.filter(priority=priority)
        return qs