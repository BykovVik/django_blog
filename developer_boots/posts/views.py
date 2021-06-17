from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from . models import Post, Category, Static_page
from taggit.models import Tag
from . forms import search_form


def index_page(request, tag_slug=None): 

    last_post = Post.objects.first()
    all_posts = Post.objects.all()
    posts_count = 3
    paginator = Paginator(all_posts, posts_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    search_form_area = search_form()
    tag = None
    all_tags = Tag.objects.all()

    if tag_slug: 
        tag = get_object_or_404(Tag, slug=tag_slug) 
        all_posts = all_posts.filter(tags__in=[tag])

    if request.is_ajax():
        return render(request, 'new_posts.html', {'new_post': last_post, 'all_posts': all_posts, 'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'paginator':paginator, 'posts_count': posts_count})

    return render(request, 'index.html', {'new_post': last_post, 'all_posts': all_posts, 'page_obj':page_obj, 'search_form_area': search_form_area, 'tag': tag, 'all_tags': all_tags, 'paginator':paginator, 'posts_count': posts_count})



def post_list(request, tag_slug=None):

    req_path = request.path.replace("/","")
    num_cat = Category.objects.get(category_name=req_path)
    posts_list = Post.objects.filter(category_title=num_cat.id)
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
