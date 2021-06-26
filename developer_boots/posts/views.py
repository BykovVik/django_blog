from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
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
    paginate_by = 2

    def get_queryset(self):

        num_cat = Category.objects.get(category_name=self.request.path.replace("/",""))

        return Post.objects.filter(category=num_cat.id)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.all()
        context['search_form_area'] = search_form()
        context['posts_count'] = self.paginate_by
        context['req_path'] = self.request.path.replace("/","")
        context['num_cat'] = Category.objects.get(category_name=context['req_path'])
        context['posts_list'] = Post.objects.filter(category=context['num_cat'].id)

        #print("ЭТОООООООООООООООООООs", context['num_cat'].id)

        return context


def post_list(request, tag_slug=None):

    req_path = request.path.replace("/","")
    num_cat = Category.objects.get(category_name=req_path)
    posts_list = Post.objects.filter(category=num_cat.id)
    posts_count = 5
    paginator = Paginator(posts_list, posts_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    search_form_area = search_form()
    tag = None
    all_tags = Tag.objects.all()

    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        all_posts = all_posts.filter(tags__in=[tag])
        paginator = Paginator(posts_list, all_posts)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        return render(request, 'new_category_posts.html', {'posts_list':posts_list, 'req_path':req_path, 'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'paginator':paginator, 'posts_count': posts_count})

    return render(request, 'posts_list.html', {'posts_list':posts_list, 'req_path':req_path, 'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'paginator':paginator, 'posts_count': posts_count})



def search_by_tags(request, tag_slug=None):

    req_path = request.path.replace("/","")
    tag = get_object_or_404(Tag, slug=tag_slug) 
    all_posts = Post.objects.all().filter(tags__in=[tag])
    posts_count = 3
    paginator = Paginator(all_posts, posts_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    search_form_area = search_form()
    tag = None
    all_tags = Tag.objects.all()

    if request.is_ajax():
        return render(request, 'new_category_posts.html', {'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'req_path':req_path, 'posts_count': posts_count, 'paginator':paginator})

    return render(request, 'search_by_tags.html', {'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'req_path':req_path, 'posts_count': posts_count, 'paginator':paginator})


def post_search(request):

    form = search_form()
    query = None
    results = []
    search_form_area = search_form() 
    
    if 'query' in request.GET:
        form = search_form(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('post_title', 'post_body'),
            ).filter(search=query)

    return render(request, 'search.html', {'form': form, 'query': query, 'results': results, 'search_form_area': search_form_area})



def one_post(request, category_title, slug):

    one_post = get_object_or_404(Post, post_slug=slug)
    search_form_area = search_form()
    all_tags = Tag.objects.all()


    return render(request, 'post.html', {'one_post': one_post, 'search_form_area': search_form_area, 'all_tags': all_tags})




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
