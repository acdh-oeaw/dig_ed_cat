import json
import os
from browsing.filters import EditionListFilter
from charts.models import *


class ChartConfigurator():

    """A simple helper class to bootstrap rendering of charts"""

    def __init__(
        self, ListFilter, filename='charts_config.py', default_charts=['bar', 'line', 'pie']
    ):
        self.source = ListFilter()
        self.all_charts = default_charts
        self.filename = os.path.abspath(os.path.join(os.path.dirname('__file__'), filename))
        self.fa_glyph = '<i class="fa fa-{}-chart" aria-hidden="true" title="{}-chart"></i>'

    def get_default_charttypes_conf(self):
        """A dictionary defining default ChartType objects"""
        config = {
            'bar': {
                'name': 'bar',
                'icon': self.fa_glyph.format('bar', 'bar')
            },
            'line': {
                'name': 'line',
                'icon': self.fa_glyph.format('line', 'line')
            },
            'pie': {
                'name': 'pie',
                'icon': self.fa_glyph.format('pie', 'pie')
            }
        }
        return config

    def create_default_charttypes(self):
        """creates ChartType objects in the database, derived from the configuration
        defined in `get_default_charttypes_conf`"""
        config = self.get_default_charttypes_conf()
        for key, value in config.items():
            print(value)
            temp_charttype, _ = ChartType.objects.get_or_create(
                name=value['name'], icon=value['icon']
            )
        return ChartType.objects.all()

    def get_default_config(self):
        """ returns a dictionary conatining basic Chart configuration
        information derived from the ListFilter instance"""
        values = {}
        for x in self.source.declared_filters.items():
            if x[1].label:
                label_val = x[1].label
            else:
                label_val = 'no label provided'
            if x[1].lookup_expr:
                lookup_expr_val = x[1].lookup_expr
            else:
                lookup_expr_val = 'no lookup_expr provided'
            values[x[0]] = {
                'label': label_val,
                'help_text': 'Provide some',
                'lookup_expr': lookup_expr_val,
                'chart_types': self.all_charts
            }
        return values

    def create_config_file(self):
        """ serializes a config-dict to file """
        config_dict = self.get_default_config()
        config_json = json.dumps(
            config_dict, ensure_ascii=False, indent=4, sort_keys=True
        )
        with open(self.filename, 'w') as f:
            f.write(config_json)
        return config_dict

    def store_config(self):
        """ creates ChartConfig objects in the database"""
        charttypes = [x.id for x in self.create_default_charttypes()]
        for key, value in self.get_default_config().items():
            temp_chart, _ = ChartConfig.objects.get_or_create(
                field_path=key,
                label=value['label']
            )
            temp_chart.chart_types.add(*charttypes)
        return ChartConfig.objects.all()


def create(filename="chart_config.py"):
    config_dict = ChartConfigurator(EditionListFilter, filename)
    return config_dict.create_config_file()
