from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, request
from django.views import generic
from django.views.generic import TemplateView

from .models import Person, Post
from django.http import HttpResponse
import logging

from django.shortcuts import render, get_object_or_404

logger = logging.getLogger(__name__)

items_per_page = 5


class index(generic.ListView):
    template_name = '../../FirstProjectRefactor/templates/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        page = 1
        return Post.objects.order_by('-pub_date')[:page * items_per_page]


class login(TemplateView):
    template_name = "login.html"



def new_post(self):
    text = self.POST['post_text']
    # uploaded_file = self.FILES['myfile']

    poster = Person(first_name="wouter", last_name="vanmulken")
    poster.save()
    poster.refresh_from_db()
    # filename ="" #Todo save the file


    # if uploaded_file is not None:
    #   p = Post(poster=poster, text=text, file=filename)
    # else:
    p = Post(poster=poster, text=text)
    p.save()
    return HttpResponseRedirect(reverse('index'))


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
