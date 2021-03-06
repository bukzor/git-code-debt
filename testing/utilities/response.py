
import pyquery
import simplejson

from git_code_debt_util.decorators import cached_property


class Response(object):
    """A Response wraps a response from a testing Client."""

    def __init__(self, response):
        self.response = response

    @cached_property
    def pq(self):
        return pyquery.PyQuery(self.response.data)

    @cached_property
    def json(self):
        return simplejson.loads(self.response.data)
