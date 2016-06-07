from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms

from .models import Post, Document, UserInfo, Like
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import auth
from django import template
from datetime import date, timedelta

register = template.Library()
logger = logging.getLogger(__name__)

items_per_page = 5


#
# @login_required
# def start(self):
#     if not self.user.is_authenticated():
#         return HttpResponseRedirect(reverse('index'))

@register.filter(name='ends_with')
def ends_with(value, arg):
    if str(value).lower().endswith():
        return 1
    else:
        return 0


@login_required
def index_without_page(self):
    return index(self, 0)


@login_required
def index(self, page):
    form = DocumentForm()
    likes = []

    return render_to_response(
        'index.html',
        {'form': form,
         'likes': likes,
         'latest_post_list':
             Post.objects.order_by(
                 '-pub_date')
             [

             (int(page) * items_per_page)
             :
             ((int(page) * items_per_page) + 5)]
            , 'page': int(page)}
        , context_instance=RequestContext(self)
    )


class login_page(TemplateView):
    template_name = "login.html"


def login_post(self):
    username = self.POST['inputUsername']
    password = self.POST['inputPassword']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(self, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
def new_post(self):
    text = self.POST['post_text']
    poster = self.user

    if self.method == 'POST':
        form = DocumentForm(self.POST, self.FILES)
        p = None

        if form.is_valid():
            newdoc = Document(docfile=self.FILES['docfile'])
            newdoc.save()
            p = Post(poster=poster, text=text, file='/media/' + newdoc.docfile.__str__())
        else:
            p = Post(poster=poster, text=text)
        p.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        form = DocumentForm()  # A empty, unbound form
        p = Post(poster=poster, text=text)
        p.save()

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        # {'form': form},
        context_instance=RequestContext(self)
    )


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


@login_required
def del_post(self, post_id):
    post_to_delete = Post.objects.get(pk=post_id)
    if post_to_delete.poster.pk is self.user.id:
        post_to_delete.delete()

    return HttpResponseRedirect(reverse('index'))


@login_required
def change_post(self, post_id):
    post_to_change = Post.objects.get(pk=post_id)
    a = 'change_text' + post_id
    text = self.POST[a]
    post_to_change.text = text
    post_to_change.save()

    return HttpResponseRedirect(reverse('index'))


class Registration(TemplateView):
    template_name = 'register.html'


def register(self):
    user = User.objects.create_user(self.POST['inputName'], self.POST['inputEmail'], self.POST['inputPassword'])
    user.save()

    us = UserInfo(friend_list='1,2,3')
    us.user = user
    us.save()

    return HttpResponseRedirect(reverse('login'))


# Todo :
# - make a friends list html template in which you can search for friends   x
# - be able to add extra fields to user                                     x
# - Friend someone                                                          x
# - Unfriend someone
# - Like a post
# - Comment on a post


def list(self):
    # Handle file upload
    if self.method == 'POST':
        form = DocumentForm(self.POST, self.FILES)
        if form.is_valid():
            newdoc = Document(docfile=self.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    user = self.user
    a = user.userinfo.friend_list.split(",")

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'aaa': a[0]},
        context_instance=RequestContext(self)
    )


@login_required
def friends(self):
    user = self.user
    a = user.userinfo.friend_list.split(",")
    friends = set([])

    for id in a:
        if str(id) != '':
            friends.add(User.objects.get(pk=id))

    # Render list page with the documents and the form
    return render_to_response(
        'friends.html',
        {'friends': friends},
        context_instance=RequestContext(self)
    )


@login_required
def add_friend(self, user_name):
    friend = User.objects.get(username=user_name)
    if self.method == 'POST':
        if friend is not None:
            user = self.user
            user.userinfo.friend_list = self.user.userinfo.friend_list + "," + str(friend.id)
            user.userinfo.save()

            return HttpResponseRedirect(reverse('friends'))


@login_required
def remove_friend(self, user_name):
    user = self.user
    a = user.userinfo.friend_list.split(",")
    friends = set(a)
    friend = User.objects.get(username=user_name)
    friends.remove(str(friend.id))

    new_friends_list = ""
    for a in friends:
        new_friends_list += "," + a
    user.userinfo.friend_list = new_friends_list
    user.userinfo.save()

    return HttpResponseRedirect(reverse('friends'))


def profile(self, user_name):
    form = None
    friend = User.objects.get(username=user_name)

    if self.method == 'POST' and self.user.id is friend.id:

        form = DocumentForm(self.POST, self.FILES)
        if form.is_valid():
            newdoc = Document(docfile=self.FILES['docfile'])
            newdoc.save()
            self.user.userinfo.profile_pic = "/media/" + newdoc.docfile.__str__()

        self.user.username = self.POST['username']
        self.user.email = self.POST['email']
        self.user.first_name = self.POST['firstname']
        self.user.last_name = self.POST['lastname']

        self.user.userinfo.save()
        self.user.save()

        return HttpResponseRedirect('/profile/' + self.user.username)
    elif self.user.id is friend.id:
        form = DocumentForm()

    is_friend = 0;
    if set(self.user.userinfo.friend_list.split(',')).__contains__(str(friend.id)):
        is_friend = 1

    return render_to_response(
        'profile.html',
        {'profile': friend, 'form': form, 'is_friend': is_friend},
        context_instance=RequestContext(self)
    )


def search(self):
    from django.db.models import Q
    search_key = self.POST['searchbar']
    found_users = User.objects.filter(
        Q(email__contains=search_key) | Q(first_name__contains=search_key) | Q(last_name=search_key) | Q(
            username=search_key))

    return render_to_response(
        'searchresults.html',
        {'searchresults': found_users},
        context_instance=RequestContext(self)
    )


@login_required
def like(self, post_id):
    post = Post.objects.get(pk=post_id)
    liked_list = str(post.liked_list).split(',')

    if liked_list.__contains__(str(self.user.id)):
        liked_list.remove(str(self.user.id))
        post.liked_list = list_to_commaseperated_field(liked_list)
        post.nr_of_likes -= 1
    else:
        post.liked_list += str(",") + str(self.user.id)
        post.nr_of_likes += 1;
    post.save()
    return HttpResponse("")


def list_to_commaseperated_field(liked_list):
    field = ""
    for a in liked_list:
        field += ',' + str(a)
    return field


@login_required
def has_liked(self, post_id):
    post = Post.objects.get(pk=post_id)
    have_liked = str(post.liked_list).split(',')
    response_data = {'hasliked': have_liked.__contains__(str(self.user.id))}  # add the list of people that have liked
    return JsonResponse(response_data)


def logout_view(self):
    auth.logout(self)
    return HttpResponseRedirect(reverse('login'))
