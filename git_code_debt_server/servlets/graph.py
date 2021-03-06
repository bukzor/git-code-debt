import datetime
import flask
import simplejson

from git_code_debt_server.render_mako import render_template
from git_code_debt_server.logic import metrics
from git_code_debt_util.time import data_points_for_time_range
from git_code_debt_util.time import to_timestamp


graph = flask.Blueprint('graph', __name__)

@graph.route('/graph/<metric_name>')
def show(metric_name):
    repo = flask.request.args.get('repo')
    start_timestamp = int(flask.request.args.get('start'))
    end_timestamp = int(flask.request.args.get('end'))

    data_points = data_points_for_time_range(
        start_timestamp,
        end_timestamp,
        data_points=250,
    )
    metrics_for_dates = metrics.metrics_for_dates(repo, metric_name, data_points)

    metrics_for_js = sorted(set(
        (m.date * 1000, m.value)
        for m in metrics_for_dates
    ))

    return render_template(
        'graph.mako',
        metric_name=metric_name,
        metrics=simplejson.dumps(metrics_for_js),
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    )

@graph.route('/graph/<metric_name>/all_data')
def all_data(metric_name):
    earliest_timestamp = metrics.get_first_data_timestamp(metric_name)
    now = datetime.datetime.today()

    return flask.redirect(flask.url_for(
        'graph.show',
        metric_name=metric_name,
        start=str(earliest_timestamp),
        end=str(to_timestamp(now)),
    ))
