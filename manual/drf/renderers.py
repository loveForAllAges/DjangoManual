from rest_framework.renderers import (
    BrowsableAPIRenderer, JSONRenderer, BaseRenderer
)

from django.utils.encoding import smart_text


# Использование HTML формат возврата по умолчанию, JSON в просматриваемом API.
class CustomBrosableAPIRenderers(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()


class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1' # По умолчанию utf-8
    render_style = 'binary' # Просматриваемый API не будет пытаться отобразить 
                            # двоичное содержимое в виде строки.

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # return smart_text(data, encoding=self.charset)
        # return data.encode(self.charset) # При использовании charset.
        return data # При использовании render_style.

