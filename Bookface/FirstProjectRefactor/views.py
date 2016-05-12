from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms

from .models import Post
import logging

from django.shortcuts import render, get_object_or_404

logger = logging.getLogger(__name__)

items_per_page = 5


def start(self):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))


class index(generic.ListView):
    template_name = '../../Bookface/templates/index.html'
    context_object_name = 'latest_post_list'

    # def get_queryset(self):
    #     page = 1
    #     return Post.objects.order_by('-pub_date')[:page * items_per_page]
    def get_queryset(self):
        page = 1
        return


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
    # uploaded_file = self.FILES['myfile']

    # poster = Person(first_name="wouter", last_name="vanmulken")
    # poster = User(first_name="wouter", last_name="vanmulken", )//Todo fix this
    # poster.save()
    # poster.refresh_from_db()
    # filename ="" #Todo save the file


    # if uploaded_file is not None:
    #   p = Post(poster=poster, text=text, file=filename)
    # else:
    # p = Post(poster=poster, text=text)//Todo fix this
    # p.save()
    return HttpResponseRedirect(reverse('index'))




class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


def del_post(self, post_id):
    post_to_delete = Post.objects.get(pk=post_id)

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

    return HttpResponseRedirect(reverse('login'))









# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
