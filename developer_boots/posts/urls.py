from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name="home"),
    path('about/', views.pages, name='about'),
    path('contacts/', views.pages, name='contacts'),
    path('privacy-policy/', views.pages, name='privacy_policy'),
    path('report-a-bug/', views.pages, name='report_a_bug'),
    path('news/', views.PostList.as_view(), name='news'),
    path('linux/', views.post_list, name='linux'),
    path('programming/', views.post_list, name='programming'),
    path('my-projects/', views.post_list, name='prod'),
    path('computer-science/', views.post_list, name='computer-science'),
    path('search/', views.post_search, name='search'),
    path('accounts/login/', views.AppLoginViews.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/change/', views.ChangeUserDataViews.as_view(), name='profile_change'),
    path('account/password/change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('accounts/logout/', views.AppLogoutViews.as_view(), name='logout'),
    path('accounts/register/', views.RegUserView.as_view(), name='register'),
    path('tag/<slug:tag_slug>/', views.search_by_tags, name='post_list_by_tag'),
    path('<str:category_title>/<slug:slug>/', views.one_post, name='one_post'),
]