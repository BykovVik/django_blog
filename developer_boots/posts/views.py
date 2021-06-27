from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from taggit.models import Tag
from . models import Post, Category, Static_page, AppUser
from . forms import search_form, ChangeUserForm, RegUserForm



class IndexPage(ListView):
    
    model = Post
    template_name = "index.html"
    context_object_name = "index"
    paginate_by = 2

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()
        context['new_post'] = Post.objects.first()
        context['posts_count'] = self.paginate_by

        return context



class PostList(ListView):

    template_name = "posts_list.html"
    context_object_name = "list"
    paginate_by = 1

    def get_queryset(self):

        num_cat = Category.objects.get(category_name=self.request.path.replace("/",""))
        return Post.objects.filter(category=num_cat.id)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()
        context['posts_count'] = self.paginate_by
        context['req_path'] = self.request.path.replace("/","")

        return context



class SearchByTags(ListView):

    template_name = "search_by_tags.html"
    context_object_name = "tags_search"
    paginate_by = 1

    def get_queryset(self):

        tag_slug = self.request.path.split("/")[2]
        tag = get_object_or_404(Tag, slug=tag_slug) 
        return Post.objects.all().filter(tags__in=[tag])

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()
        context['posts_count'] = self.paginate_by
        context['req_path'] = self.request.path.replace("/","")

        return context


class SearchByArticles(ListView):

    template_name = "search.html"
    context_object_name = "posts_search"
    paginate_by = 1
    query = []

    def get_queryset(self):

        if 'query' in self.request.GET:

            form = search_form(self.request.GET)

            if form.is_valid():

                self.query = form.cleaned_data['query']
                return Post.objects.annotate(
                    search=SearchVector('post_title', 'post_body'),
                    ).filter(search=self.query)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()
        context['posts_count'] = self.paginate_by
        context['req_path'] = self.request.path.replace("/","")
        context['query'] = self.query

        return context



class OnePost(DetailView):

    model = Post
    template_name = 'post.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()

        return context


def pages(request):

    req_path = request.path
    page_title = request.path.replace("/","")
    post = get_object_or_404(Static_page, url=req_path)

    title_path = req_path.replace(" ", "/")

    return render(request, 'pages.html', {'post': post, 'req_path': title_path, 'page_title': page_title})

################################################USERS_VIEWS##################################

class AppLoginViews(LoginView):
    
    template_name = 'login.html'



@login_required
def profile(request):

    return render(request, 'profile.html')



class AppLogoutViews(LoginRequiredMixin, LogoutView):

    template_name = 'logout.html'



class ChangeUserDataViews(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

    model = AppUser
    template_name = "change_user.html"
    form_class = ChangeUserForm
    success_url = reverse_lazy('profile')
    success_message = "Данные пользователя успешно изменены"

    def setup(self, request, *args, **kwargs):

        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):

        if not queryset:

            queryset = self.get_queryset()
        
        return get_object_or_404(queryset, pk = self.user_id)



class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):

    template_name = 'change_pass.html'
    success_url = reverse_lazy('password_change')
    success_message = 'Пароль успешно изменён'



class RegUserView(CreateView):

    model = AppUser
    template_name = 'reg_user.html'
    form_class = RegUserForm
    success_url = reverse_lazy('register')
