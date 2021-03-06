"""Test the kernels service API."""
import json

from jupyterlab.tests.utils import LabTestBase, APITester
from notebook.tests.launchnotebook import assert_http_error
from jupyterlab.commands import build


class SettingsAPI(APITester):
    """Wrapper for settings REST API requests"""

    url = 'lab/api/settings'

    def get(self, section_name):
        return self._req('GET', section_name)

    def patch(self, section_name, body):
        return self._req('PATCH', section_name, json.dumps(body))


class SettingsAPITest(LabTestBase):
    """Test the settings web service API"""
    @classmethod
    def setup_class(cls):
        super(SettingsAPITest, cls).setup_class()
        build()

    def setUp(self):
        self.settings_api = SettingsAPI(self.request)

    def test_get(self):
        id = '@jupyterlab/apputils-extension:themes'
        data = self.settings_api.get(id).json()
        assert data['id'] == id
        assert len(data['schema'])
        assert 'data' in data

    def test_get_bad(self):
        with assert_http_error(404):
            self.settings_api.get('foo')

    def test_patch(self):
        id = '@jupyterlab/apputils-extension:themes'
        resp = self.settings_api.patch(id, dict())
        assert resp.status_code == 204

    def test_patch_wrong_id(self):
        with assert_http_error(404):
            self.settings_api.patch('foo', dict())

    def test_patch_bad_data(self):
        id = '@jupyterlab/codemirror-extension:commands'
        data = dict(keyMap=10)
        with assert_http_error(400):
            self.settings_api.patch(id, data)
