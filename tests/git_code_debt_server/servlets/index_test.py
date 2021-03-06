
import flask
import pytest

from git_code_debt_server.servlets.index import DeltaPresenter
from git_code_debt_server.servlets.index import MetricPresenter
from testing.assertions.response import assert_no_response_errors


def _test_it_loads(server):
    response = server.client.get(flask.url_for('index.show'))
    assert_no_response_errors(response)
    # Should have a nonzero number of links to things
    assert len(response.pq.find('a[href]')) > 0

@pytest.mark.integration
def test_it_loads_no_data(server):
    _test_it_loads(server)

@pytest.mark.integration
def test_it_loads_with_data(server_with_data):
    _test_it_loads(server_with_data)


def test_delta_classname_negative():
    delta = DeltaPresenter('url', -9001)
    assert delta.classname == 'metric-down'

def test_delta_classname_zero():
    delta = DeltaPresenter('url', 0)
    assert delta.classname == 'metric-none'

def test_delta_classname_positive():
    delta = DeltaPresenter('url', 9001)
    assert delta.classname == 'metric-up'


def test_metric_classname_overriden():
    metric = MetricPresenter('metric', True, 0, tuple(), '')
    assert metric.classname == 'color-override'

def test_metric_classname_normal():
    metric = MetricPresenter('metric', False, 0, tuple(), '')
    assert metric.classname == ''
