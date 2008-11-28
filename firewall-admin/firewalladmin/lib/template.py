import commands, os

import cherrypy
from genshi.core import Stream
from genshi.output import encode, get_serializer
from genshi.template import Context, TemplateLoader

loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), '..', 'templates'),
    auto_reload=True
)

def theme(filename, method='xhtml', encoding='utf-8', **options):
    """Decorator for exposed methods to specify what template the should use
    for rendering, and which serialization method and options should be
    applied.
    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            cherrypy.thread_data.template = loader.load(filename)
            if method == 'html':
                options.setdefault('doctype', 'html')
            serializer = get_serializer(method, **options)
            stream = func(*args, **kwargs)
            if not isinstance(stream, Stream):
                return stream
            return encode(serializer(stream), method=serializer,
                          encoding=encoding)
        return wrapper
    return decorate

def render(*args, **kwargs):
    """
    Function to render the given data to the template specified via the
    ``@output`` decorator.
    """
    if args:
        assert len(args) == 1, \
            'Expected exactly one argument, but got %r' % (args,)
        template = loader.load(args[0])
    else:
        template = cherrypy.thread_data.template
    ctxt = Context(url=cherrypy.url)
    
    """ Setup menu """
    if kwargs.get('show_menu', True):
        menu = [{'title': 'home', 'url': '/'}]
        if kwargs.get('menu'):
            menu.append(kwargs.pop('menu'))
        menu.extend([{'title': 'allow list', 'url': '/allowlist/' },
                    {'title': 'deny lists', 'url': '/denylist/'},
                    {'title': 'logout', 'url': '/do_logout'}])
        kwargs['menu'] = menu
    
    """ Add System Status """
    kwargs.setdefault('system_status', commands.getoutput('uptime'))
        
    ctxt.push(kwargs)
    return template.generate(ctxt)
