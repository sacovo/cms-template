from django.shortcuts import render, get_object_or_404
from feincms3.apps import page_for_app_request

from feincms3.shortcuts import render_list
from django.utils import timezone
from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags
from cms.renderer import renderer as cms_renderer
from blog.models import Article, Namespace
from blog.renderer import renderer

# Create your views here.

def article_list(request):
    page = page_for_app_request(request)

    page.activate_language(request)
    ancestors = list(page.ancestors().reverse())

    article_list = Article.objects.filter(
        namespace=page.namespace,
        publication_date__lte=timezone.now()
    )

    return render_list(
        request, article_list,
        {
            'page': page,
            'article_list': article_list,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page, renderer=cms_renderer, timeout=60,
                inherit_from=ancestors
            ),
        }
    )

def article_detail(request, slug):
    page = page_for_app_request(request)
    page.activate_language(request)
    ancestors = list(page.ancestors().reverse())

    article = get_object_or_404(
        Article,
        slug=slug,
        namespace=page.namespace,
        language_code=page.language_code
    )
    return render(
        request,
        'blog/article_detail.html',
        {
            'page': page,
            'title': article.title,
            'article': article,
            "meta_tags": meta_tags([article, page] + ancestors, request=request),
            "blog_regions": Regions.from_item(
                article, renderer=renderer, timeout=60
            ),
            "regions": Regions.from_item(
                page, renderer=cms_renderer, timeout=60,
                inherit_from=ancestors
            ),
        }
    )
