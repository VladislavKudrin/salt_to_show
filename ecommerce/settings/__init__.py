from .base import *
is_local = False


from .production import *

# in production.py: 
# TESTSERVER = os.environ.get('TESTSERVER')
# LIVE = os.environ.get('LIVE')
if not TESTSERVER  and not LIVE: 
	try:
		from .local import *
		is_local = True
	except:
		pass

if not is_local:
	from ecommerce.aws.conf import *