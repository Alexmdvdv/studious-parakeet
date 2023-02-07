from .models import *
from django.core.cache import cache

menu = [{'title': 'О сайте', 'url_name': '/about'},
        {'title': 'Добавить статью', 'url_name': '/add_page'},
        {'title': 'Контакты', 'url_name': '/contact'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = cache.get('categories')
        if not categories:
            categories = Category.objects.all()
            cache.set('categories', categories, 60)
        context['menu'] = menu
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
