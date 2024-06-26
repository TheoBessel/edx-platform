"""
Tests for custom DOT scopes backend.
"""


import ddt
from django.conf import settings
from django.test import TestCase

from openedx.core.djangoapps.oauth_dispatch.scopes import ApplicationModelScopes
from openedx.core.djangoapps.oauth_dispatch.tests.factories import ApplicationAccessFactory
from openedx.core.djangolib.testing.utils import skip_unless_lms


@skip_unless_lms
@ddt.ddt
class ApplicationModelScopesTestCase(TestCase):
    """
    Tests for the ApplicationModelScopes custom DOT scopes backend.
    """
    @ddt.data(
        ([], []),
        (['unsupported_scope:read'], []),
        (['grades:read'], ['grades:read']),
        (['grades:read', 'certificates:read'], ['grades:read', 'certificates:read']),
    )
    @ddt.unpack
    def test_get_available_scopes(self, application_scopes, expected_additional_scopes):
        """ Verify the settings backend returns the expected available scopes. """
        application_access = ApplicationAccessFactory(scopes=application_scopes)
        scopes = ApplicationModelScopes()
        assert set(scopes.get_available_scopes(application_access.application)) == \
            set(list(settings.OAUTH2_DEFAULT_SCOPES.keys()) + expected_additional_scopes)

    def test_has_user_id_in_application_scopes(self):
        """ Verify the settings backend correctly identifies whether the user_id scope is available. """
        application_access = ApplicationAccessFactory(scopes=['user_id'])
        scopes = ApplicationModelScopes()
        assert scopes.has_user_id_in_application_scopes(application_access.application)
        application_access.scopes = []
        application_access.save()
        assert not scopes.has_user_id_in_application_scopes(application_access.application)
