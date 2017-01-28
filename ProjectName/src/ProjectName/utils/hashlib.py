from hashlib import md5 as _md5
from hashlib import sha1 as _sha1

from django.utils.encoding import force_bytes

md5_text = lambda x: _md5(force_bytes(x, errors='replace'))
sha1_text = lambda x: _sha1(force_bytes(x, errors='replace'))
