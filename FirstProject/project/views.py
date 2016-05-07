from distutils.log import Log

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.utils import timezone
from django.shortcuts import redirect
from .models import Person, Post
import logging

logger = logging.getLogger(__name__)


class Index(generic.ListView):
    template_name = '../../FirstProjectRefactor/templates/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-pub_date')[:5]


def new_post(request):
    logger.error("fuuuuu")
    text = request.POST['post_text']
    logger.error(text)
    p = Post(poster=Person.objects[0], text=text, pub_date=timezone.now())
    p.save()
    return redirect(Index)
    return HttpResponseRedirect(reverse('index'))
    # return render(request, 'index.html', {
    #     'post': p
    # })
    # return HttpResponseRedirect(reverse('results', args=(question.id,)))
