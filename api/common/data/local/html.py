import os
import logging
import inspect

logger = logging.getLogger(__name__)
print(os.getcwd())

class HTML:
    REGISTRATION_PENDING = None
    REGISTRATION_PENDING_EMAIL = None
    REGISTRATION_EXISTING = None


TEMPLATE_DIR = os.path.join('web', 'templates')
_did_load = False



__load__ = [
    k for k, v in
    inspect.getmembers(
        HTML,
        lambda attr: not inspect.isroutine(attr)
    )
    if k.isupper() and v is None
]

# this should run before start of the api gateway
# so this does not necessarily need to be asynchronous
if _did_load is False:
    for html in __load__:
        try:
            _path = os.path.join(
                TEMPLATE_DIR, 
                'internal', 
                f'{html.lower()}.html'
            )
            logger.info('Loading HTMl %s' % _path)
            with open(_path) as f:
                setattr(
                    HTML,
                    html,
                    f.read()
                )
        except FileNotFoundError:
            logger.warning('Missing HTML file with path : %s' % _path)
    
    
    

    assert all(getattr(HTML, html) is not None for html in __load__)
    _did_load = True
