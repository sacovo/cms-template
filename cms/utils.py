from django.utils.translation import gettext as _
from content_editor.models import Region, Template

def get_template_list(app_name, templates):
    return [
        Template(
            key=template[0],
            title=_(template[0]).title(),
            template_name=f"{app_name}/{template[0]}.html",
            regions=[
                Region(key=region, title=region.title(), inherited=True)
                for region in template[1]
            ]
        ) for template in templates
    ]
