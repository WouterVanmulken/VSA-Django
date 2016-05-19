from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms

from .models import Post, Document, UserInfo
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



from django.shortcuts import render, get_object_or_404

logger = logging.getLogger(__name__)

items_per_page = 5


def start(self):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))


class index(generic.ListView):
    template_name = '../../Bookface/templates/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        page = 1
        # form = DocumentForm() # A empty, unbound form

        return Post.objects.order_by('-pub_date')[:page * items_per_page]

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['form'] = DocumentForm()

        return context


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


def new_post(self):
    text = self.POST['post_text']
    poster = self.user

    if self.method == 'POST' and self.FILES['docfile']:
        form = DocumentForm(self.POST, self.FILES)
        if form.is_valid():
            newdoc = Document(docfile=self.FILES['docfile'])
            newdoc.save()
            p = Post(poster=poster, text=text, file=newdoc.docfile.__str__())
            p.save()
            # Redirect to the document list after POST
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
        context_instance=RequestContext(request)
    )


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
from django.db import models

#
# class Document(models.Model):
#     docfile = models.FileField(upload_to='documents/%Y/%m/%d')


def del_post(self, post_id):
    post_to_delete = Post.objects.get(pk=post_id)
    if post_to_delete.poster.pk is self.user:
        post_to_delete.delete()

    return HttpResponseRedirect(reverse('index'))


def change_post(self, post_id):
    post_to_change = Post.objects.get(pk=post_id)
    a = 'change_text' + post_id
    text = self.POST[a]
    post_to_change.text = text
    post_to_change.save()

    return HttpResponseRedirect(reverse('index'))


class registration(TemplateView):
    template_name = 'register.html'


def register(self):
    user = User.objects.create_user(self.POST['inputName'], self.POST['inputEmail'], self.POST['inputPassword'])
    user.save()

    us = UserInfo(friend_list='1,2,3')
    us.user = user
    us.save()

    return HttpResponseRedirect(reverse('login'))

# Todo :
# - make a friends list html template in which you can search for friends
# - be able to add extra fields to user
# - Friend someone
# - Unfriend someone
# - Like a post
# - Comment on a post


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    user = request.user
    a = user.userinfo.friend_list.split(",")

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'aaa':a[0]},
        context_instance=RequestContext(request)
    )


def friends(request):
    # Handle file upload
    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         newdoc = Document(docfile = request.FILES['docfile'])
    #         newdoc.save()
    #
    #         # Redirect to the document list after POST
    #         return HttpResponseRedirect(reverse('list'))
    # else:
    #     form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    # documents = Document.objects.all()
    user = request.user
    a = user.userinfo.friend_list.split(",")

    friends = []

    for id in a:
        friends.append(User.objects.get(pk=id))

    # Render list page with the documents and the form
    return render_to_response(
        'friends.html',
        {'friends': friends},
        context_instance=RequestContext(request)
    )


def profile(request, user_name):

    friend = User.objects.get(username=user_name)

    if request.method == 'POST':
        if friend is not None:
            user = request.user
            user.userinfo.friend_list = request.user.userinfo.friend_list + "," + str(friend.id)
            user.userinfo.save()

            return HttpResponseRedirect(reverse('friends'))

    return render_to_response(
        'profile.html',
        {'user': friend},
        context_instance=RequestContext(request)
    )


def search(self):
    from django.db.models import Q
    search_key = self.POST['searchbar']
    found_users = User.objects.filter(Q(email__contains=search_key) | Q(first_name__contains=search_key) |Q(last_name=search_key) | Q(username=search_key))

    return render_to_response(
        'searchresults.html',
        {'searchresults': found_users},
        context_instance=RequestContext(self)
    )

