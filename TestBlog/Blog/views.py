from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from unidecode import unidecode

from .forms import AddPostForm, LoginUserForm, RegisterUserForm
from .models import *
from .utils import DataMixin


class BlogHome(DataMixin, ListView):
    model = BlogModel
    template_name = 'Blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(mixin_context.items()))

    def get_queryset(self):
        return BlogModel.objects.filter(is_published=True)


class ShowPost(DataMixin, DetailView):
    model = BlogModel
    template_name = 'Blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(mixin_context.items()))


class ShowCategory(DataMixin, ListView):
    model = BlogModel
    template_name = 'Blog/index.html'
    slug_url_kwarg = 'cat_slug'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogModel.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                              cat_selected=self.kwargs['cat_slug'])
        return dict(list(context.items()) + list(mixin_context.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'Blog/addpage.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'

    def get_context_data(self, *, object_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(mixin_context.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'Blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(mixin_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'Blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(mixin_context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class AboutView(DataMixin, TemplateView):
    template_name = 'Blog/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(mixin_context.items()))


class ContactView(DataMixin, TemplateView):
    template_name = 'Blog/contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Контакты')
        return dict(list(context.items()) + list(mixin_context.items()))


class Search(DataMixin, ListView):
    model = BlogModel
    template_name = 'Blog/search.html'
    context_object_name = 'found'

    def get_queryset(self):
        return BlogModel.objects.filter(
            Q(title__iregex=self.request.GET.get('q')) | Q(content__iregex=self.request.GET.get('q')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        mixin_context = self.get_user_context(title='Результат поиска - ' + context['q'])
        return dict(list(context.items()) + list(mixin_context.items()))
