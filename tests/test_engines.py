import datetime

import pytz
from django.test import TestCase
from django_clickhouse.migrations import migrate_app

from django_clickhouse.database import connections
from tests.clickhouse_models import ClickHouseCollapseTestModel
from tests.models import TestModel


class CollapsingMergeTreeTest(TestCase):
    fixtures = ['test_model']
    maxDiff = None

    collapse_fixture = [{
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": 1,
        "version": 1
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": -1,
        "version": 1
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": 1,
        "version": 2
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": -1,
        "version": 2
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": 1,
        "version": 3
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": -1,
        "version": 3
    }, {
        "id": 1,
        "created": "2018-01-01 00:00:00",
        "sign": 1,
        "version": 4
    }]

    def setUp(self):
        self.db = connections['default']
        self.db.drop_database()
        self.db.create_database()
        migrate_app('tests', 'default')
        ClickHouseCollapseTestModel.get_storage().flush()

        ClickHouseCollapseTestModel.objects.bulk_create([
            ClickHouseCollapseTestModel(**item) for item in self.collapse_fixture
        ])
        self.objects = TestModel.objects.filter(id=1)

    def test_get_final_versions_by_final_date(self):
        final_versions = ClickHouseCollapseTestModel.engine.get_final_versions(ClickHouseCollapseTestModel,
                                                                               self.objects)

        self.assertEqual(1, len(final_versions))
        self.assertDictEqual({'id': 1, 'sign': 1, 'version': 4, 'value': 0},
                             final_versions[0].to_dict(field_names=('id', 'sign', 'value', 'version')))

    def test_get_final_versions_by_version_date(self):
        ClickHouseCollapseTestModel.engine.version_col = 'version'
        final_versions = ClickHouseCollapseTestModel.engine.get_final_versions(ClickHouseCollapseTestModel,
                                                                               self.objects)

        self.assertEqual(1, len(final_versions))
        self.assertDictEqual({'id': 1, 'sign': 1, 'version': 4, 'value': 0},
                             final_versions[0].to_dict(field_names=('id', 'sign', 'value', 'version')))

    def test_get_final_versions_by_final_datetime(self):
        final_versions = ClickHouseCollapseTestModel.engine.get_final_versions(ClickHouseCollapseTestModel,
                                                                               self.objects, date_col='created')

        self.assertEqual(1, len(final_versions))
        self.assertDictEqual({'id': 1, 'sign': 1, 'version': 4, 'value': 0},
                             final_versions[0].to_dict(field_names=('id', 'sign', 'value', 'version')))

    def test_get_final_versions_by_version_datetime(self):
        ClickHouseCollapseTestModel.engine.version_col = 'version'
        final_versions = ClickHouseCollapseTestModel.engine.get_final_versions(ClickHouseCollapseTestModel,
                                                                               self.objects, date_col='created')

        self.assertEqual(1, len(final_versions))
        self.assertDictEqual({'id': 1, 'sign': 1, 'version': 4, 'value': 0},
                             final_versions[0].to_dict(field_names=('id', 'sign', 'value', 'version')))