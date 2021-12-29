# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import List
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *

# Create your views here.

# menu =[ {'title':"О сайте", 'url_name': 'about'},
#         {'title':"Добавить статью", 'url_name': 'add_page'},                                          #в utils.py
#         {'title':"Обратная связь", 'url_name': 'contact'},
#         {'title':"Войти", 'url_name': 'login'}
# ]

class DogsHome(DataMixin, ListView):
    model=Dogs                                                                     #выбирает записи из таблицы(модель Dogs) и выводит в виде списка
    template_name='dogs/index.html'
    context_object_name='posts'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu']=menu                                                                              #mixin
        # context['title']='Главная страница'
        # context['cat_selected']=0
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items())+list(c_def.items()))
    
    def get_queryset(self):
        return Dogs.objects.filter(is_published = True)


# def index(request):
#     posts=Dogs.objects.all()
#     context={
#         'posts': posts,
#         'menu': menu,                                                                            #class DogsHome
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request,'dogs/index.html', context=context)

def about(request):
    return render(request, 'dogs/about.html', {'menu': menu, 'title': 'О сайте'})

# def addpage(request):
#     if request.method=='POST':
#         form=AddPostForm(request.POST, request.FILES)
#         if form.is_valid():                                                                           #class AddPage
#             # print(form.cleaned_data)
#             # try:
#                 # Dogs.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('home')
#             # except:
#                 # form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form=AddPostForm()
#     return render(request, 'dogs/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):  #LoginRequiredMixin ограничивает доступ к странице для неавторизованого пользователя
    form_class = AddPostForm
    template_name = 'dogs/addpage.html'
    success_url = reverse_lazy('home')  #перенаправляет на гл стр
    # login_url='/admin/'
    login_url=reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title']='Добавление статьи'                                                              #mixin
        # context['menu']=menu
        c_def = self.get_user_context(title="Довавление статьи")
        return dict(list(context.items())+list(c_def.items()))

# def contact(request):
#     return HttpResponse('обратная связь')
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'dogs/contact.html'
    success_url = reverse_lazy('home') 

    def get_context_data(self, *, object_list=None, **kwargs):      #формирует контекст для шаблона
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):    #вызывается в случе правильного заполнения формы
        print(form.cleaned_data)
        return redirect('home')

# def login(request):
#     return HttpResponse('авторизация')

def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# def show_post(request, post_slug):
#     post=get_object_or_404(Dogs, slug=post_slug)                                                  #class ShowPost
#     context={
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     # передается в post.html
#     return render(request,'dogs/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Dogs
    template_name = 'dogs/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title']=context['post']                                                                  #mixin
        # context['menu']=menu
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items())+list(c_def.items()))

# def show_category(request, cat_slug):                                                             #class DogsCategory
#     posts=Dogs.objects.filter(cat__slug=cat_slug)

#     if len(posts)==0:
#         raise Http404()

#     context={
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug,
#     }
#     return render(request,'dogs/index.html', context=context)

class DogsCategory(DataMixin, ListView):
    model = Dogs
    template_name = 'dogs/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Dogs.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)  #cat__slug ссылается к полю слаг в таблице категорий
    
    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title']='Категория - ' + str(context['posts'][0].cat)                                                      #mixin
        # context['menu']=menu
        # context['cat_selected']=context['posts'][0].cat_id
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items())+list(c_def.items()))



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'dogs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'dogs/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')