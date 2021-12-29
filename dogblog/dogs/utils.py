from django.db.models import Count
from .models import *

menu =[ {'title':"О сайте", 'url_name': 'about'},
        {'title':"Добавить статью", 'url_name': 'add_page'},
        {'title':"Обратная связь", 'url_name': 'contact'},
        
]
class DataMixin:        #mixin исключает дублирование кода
    paginate_by=4         #кол-во постов на странице                                            
    def get_user_context(self, **kwargs):
        context = kwargs
        cats=Category.objects.annotate(Count('dogs'))    #показывает категорию, если в ней есть хоть 1 пост, если нет- то пустая не видна. (base.html)

        # context['menu'] = menu 
        user_menu = menu.copy()                     #(скрывает добавление статьи для неавторизированого юзера
        if not self.request.user.is_authenticated:      #делает копию словаря menu, сохраняет копию в юзер_меню, и если юзер не авторизован,
            user_menu.pop(1)                                #удаляет  пункт добавления статьи из юзер_меню)
        context['menu'] = user_menu                                      
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0   #если ключ катселектед нет в параметрах(кваргс)- создается =0
        return context