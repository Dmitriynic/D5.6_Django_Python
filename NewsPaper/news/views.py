from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post as PostModel
from .filters import PostFilter
from .forms import PostForm

class Posts(ListView):
    model = PostModel
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-datetime']
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context



class SearchPosts(ListView):
    model = PostModel
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-datetime']
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'news/post_detail.html'
    queryset = PostModel.objects.all()


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    from_class = PostForm
    permission_required = ('news.add_Post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name='news/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_Post')


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return PostModel.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name='news/post_delete.html'
    queryset=PostModel.objects.all()
    success_url='/news/'