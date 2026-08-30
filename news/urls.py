from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "articles/",
        views.article_list,
        name="article_list",
    ),

    path(
        "articles/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),

    path(
        "newsletters/",
        views.newsletter_list,
        name="newsletter_list",
    ),

    path(
        "newsletters/<int:newsletter_id>/",
        views.newsletter_detail,
        name="newsletter_detail",
    ),

    path(
        "publishers/",
        views.publisher_list,
        name="publisher_list",
    ),

    path(
        "publishers/<int:publisher_id>/",
        views.publisher_detail,
        name="publisher_detail",
    ),

    path(
        "publisher/dashboard/",
        views.publisher_dashboard,
        name="publisher_dashboard",
    ),

    path(
        "journalist/dashboard/",
        views.journalist_dashboard,
        name="journalist_dashboard",
    ),

    path(
        "journalist/articles/create/",
        views.article_create,
        name="article_create",
    ),

    path(
        "journalist/articles/<int:article_id>/edit/",
        views.article_edit,
        name="article_edit",
    ),

    path(
        "journalist/articles/<int:article_id>/delete/",
        views.article_delete,
        name="article_delete",
    ),

    path(
        "journalist/newsletters/create/",
        views.newsletter_create,
        name="newsletter_create",
    ),

    path(
        "journalist/newsletters/<int:newsletter_id>/edit/",
        views.newsletter_edit,
        name="newsletter_edit",
    ),

    path(
        "journalist/newsletters/<int:pk>/delete/",
        views.newsletter_delete,
        name="newsletter_delete",
    ),  

    path(
        "editor/dashboard/",
        views.editor_dashboard,
        name="editor_dashboard",
    ),

    path(
        "editor/articles/<int:article_id>/approve/",
        views.approve_article,
        name="approve_article",
    ),
]