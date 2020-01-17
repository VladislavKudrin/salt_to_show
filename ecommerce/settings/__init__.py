from .base import *
is_local = False


from .production import *

try:
	from .local import *
	is_local = True
except:
	pass

if not is_local:
	from ecommerce.aws.conf import *