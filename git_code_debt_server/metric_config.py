
import collections
import re

import staticconf
import staticconf.errors
import staticconf.getters


CONFIG_NAMESPACE = 'metric_config'
metric_config_watcher = staticconf.ConfigFacade.load(
    'metric_config.yaml',
    CONFIG_NAMESPACE,
    staticconf.YamlConfiguration,
    min_interval=30,
)
metric_config_getter = staticconf.NamespaceGetters(CONFIG_NAMESPACE)


class Group(collections.namedtuple('Group', ['name', 'metrics', 'metric_expressions'])):
    __slots__ = ()

    def contains(self, metric_name):
        return (
            metric_name in self.metrics or
            any(expr.search(metric_name) for expr in self.metric_expressions)
        )

    @classmethod
    def from_yaml(cls, name, metrics, metric_expressions):
        if not metrics and not metric_expressions:
            raise staticconf.errors.ValidationError(
                'Group {0} must define at least one of '
                '`metrics` or `metric_expressions`'.format(name)
            )
        return cls(
            name,
            set(metrics),
            tuple(re.compile(expr) for expr in metric_expressions),
        )


def _get_groups_from_yaml(yaml):
    # A group dict maps it's name to a dict containing metrics and
    # metric_expressions
    # Here's an example yaml:
    # [{'Bar': {'metrics': ['Foo', 'Bar'], 'metric_expressions': ['^Baz']}}]
    return tuple(
        Group.from_yaml(
            group_dict.keys()[0],
            group_dict.values()[0].get('metrics', []),
            group_dict.values()[0].get('metric_expressions', []),
        )
        for group_dict in yaml
    )


groups = staticconf.getters.build_getter(
    _get_groups_from_yaml,
    getter_namespace='metric_config',
)('Groups')

color_overrides = metric_config_getter.get_set('ColorOverrides')
