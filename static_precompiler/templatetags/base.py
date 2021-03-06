from django.core.cache import cache
from django.template import Node
from static_precompiler.settings import USE_CACHE, CACHE_TIMEOUT
from static_precompiler.utils import get_cache_key, get_hexdigest


class BaseInlineNode(Node):

    compiler = None

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        source = self.nodelist.render(context)

        if USE_CACHE:
            cache_key = get_cache_key(get_hexdigest(source))
            cached = cache.get(cache_key, None)
            if cached is not None:
                return cached
            output = self.compiler.compile_source(source)
            cache.set(cache_key, output, CACHE_TIMEOUT)
            return output

        return self.compiler.compile_source(source)
