from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.views.decorators.csrf import ensure_csrf_cookie

from feincms3.regions import Regions
from feincms3_meta.utils import meta_tags

from cms.models import Page
from cms.renderer import renderer


@ensure_csrf_cookie
def page_detail(request, path=None):
    page = get_object_or_404(
        Page.objects.active(),
        path=f"/{path}/" if path else '/',
    )

    if page.redirect_to_url or page.redirect_to_page:
        return redirect(page.redirect_to_url or page.redirect_to_page)

    edit = request.user.is_authenticated and request.user.is_staff

    page.activate_language(request)
    ancestors = list(page.ancestors().reverse())
    return render(
        request,
        page.template.template_name,
        {
            "page": page,
            "edit": edit,
            "header_image": page.image,
            "meta_tags": meta_tags([page] + ancestors, request=request),
            "regions": Regions.from_item(
                page, renderer=renderer, timeout=60,
                inherit_from=ancestors
            ),
        },
    )
