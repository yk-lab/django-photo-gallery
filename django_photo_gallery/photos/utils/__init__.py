import json
import base64
from numbers import Rational


class ExifJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Rational):
            return {'numerator': o.numerator, 'denominator': o.denominator}
        if isinstance(o, bytes):
            return base64.b64encode(o).decode('ascii')
        return super(ExifJSONEncoder, self).default(o)
