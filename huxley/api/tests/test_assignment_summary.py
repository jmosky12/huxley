# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.accounts.models import User
from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models
# Copyright (c) 2011-2015 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from huxley.api import tests
from huxley.api.tests import auto
from huxley.utils.test import models



class AssignmentSummaryDetailGetTestCase(auto.RetrieveAPIAutoTestCase):
    url_name = 'api:assignment_summary_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_assignment_summary()

    def test_anonymous_user(self):
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        self.as_user(self.object.registration.school.advisor).do_test()

    def test_chair(self):
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test()

    def test_superuser(self):
        self.as_superuser().do_test()


class AssignmentSummaryDetailPutTestCase(tests.UpdateAPITestCase):
    url_name = 'api:assignment_summary_detail'
    params = {
        'name': 'Jake',
        'summary': '10/10',
        'published_summary': 'published_summary'
    }

    def setUp(self):
        self.assignment_summary = models.new_assignment_summary()

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignments.'''
        response = self.get_response(self.assignment_summary.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be able to update assignment summaries'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.assignment_summary.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should be able to update assignment summaries'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.assignment_summary.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.assignment_summary.id,
            "name": self.assignment_summary.name,
            "summary": self.assignment_summary.summary,
            "published_summary": self.assignment_summary.published_summary
        })

    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment_summary.id)
        self.assertEqual(response.data, {
            "id": self.assignment_summary.id,
            "name": self.assignment_summary.name,
            "summary": self.assignment_summary.summary,
            "published_summary": self.assignment_summary.published_summary
        })



class AssignmentSummaryDetailPatchTestCase(tests.PartialUpdateAPITestCase):
    url_name = 'api:assignment_summary_detail'
    params = {
        'name': 'Jake',
        'summary': '10/10',
        'published_summary': 'published_summary'
    }

    def setUp(self):
        self.summary = models.new_assignment_summary(
            name='Jake', summary='9/10', published_summary='Great')

    def test_anonymous_user(self):
        '''Unauthenticated users shouldn't be able to update assignment summaries.'''
        response = self.get_response(self.assignment_summary.id, params=self.params)
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''Advisors should not be allowed to edit assignment summaries.'''
        self.client.login(username='advisor', password='advisor')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertPermissionDenied(response)

    def test_chair(self):
        '''Chairs should be able to update assignments'''
        self.client.login(username='chair', password='chair')
        response = self.get_response(self.assignment.id, params=self.params)
        self.assertEqual(response.data, {
            "id": self.assignment_summary.id,
            "name": self.assignment_summary.name,
            "summary": self.assignment_summary.summary,
            "published_summary": self.assignment_summary.published_summary
        })


    def test_superuser(self):
        '''It should return correct data.'''
        superuser = models.new_superuser(username='s_user', password='s_user')
        self.client.login(username='s_user', password='s_user')
        response = self.get_response(self.assignment_summary.id)
        self.assertEqual(response.data, {
            "id": self.assignment_summary.id,
            "name": self.assignment_summary.name,
            "summary": self.assignment_summary.summary,
            "published_summary": self.assignment_summary.published_summary
        })



class AssignmentSummaryDetailDeleteTestCase(auto.DestroyAPIAutoTestCase):
    url_name = 'api:assignment_summary_detail'

    @classmethod
    def get_test_object(cls):
        return models.new_assignment_summary()

    def test_anonymous_user(self):
        '''Anonymous users cannot delete assignment summaries.'''
        self.do_test(expected_error=auto.EXP_NOT_AUTHENTICATED)

    def test_advisor(self):
        '''Advisors cannot delete their assignment summaries.'''
        self.as_user(self.object.registration.school.advisor).do_test(
            expected_error=auto.EXP_DELETE_NOT_ALLOWED)

    def test_chair(self):
        '''Chairs cannot delete their assignment summaries.'''
        chair = models.new_user(user_type=User.TYPE_CHAIR)
        self.as_user(chair).do_test(expected_error=auto.EXP_PERMISSION_DENIED)

    def test_other_user(self):
        '''A user cannot delete another user's assignment summaries.'''
        models.new_school(user=self.default_user)
        self.as_default_user().do_test(
            expected_error=auto.EXP_PERMISSION_DENIED)

    def test_superuser(self):
        '''A superuser cannot delete assignment summaries.'''
        self.as_superuser().do_test(expected_error=auto.EXP_DELETE_NOT_ALLOWED)


class AssignmentSummaryListGetTestCase(tests.ListAPITestCase):
    url_name = 'api:assignment_summary_list'

    def setUp(self):
        self.a1 = models.new_assignment_summary(
            name='Jake', summary='9/10', published_summary='Great')
        self.a2 = models.new_assignment_summary(
            name='Michael', summary='10/10', published_summary='Amazing')
        self.a3 = models.new_assignment_summary(
            name='Sachit', summary='4/10', published_summary='Aight')

    def test_anonymous_user(self):
        '''It rejects a request from an anonymous user.'''
        response = self.get_response()
        self.assertNotAuthenticated(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assertNotAuthenticated(response)

    def test_advisor(self):
        '''It returns the assignment summary for the school's advisor.'''
        self.client.login(username='advisor', password='advisor')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_assignment_summaries_equal(response, [self.a1, self.a2])

    def test_chair(self):
        '''It returns the assignments associated with the chair's committee'''
        self.client.login(username='chair', password='chair')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(
            params={'committee_id': self.committee.id})
        self.assert_assignment_summaries_equal(response, [self.a1, self.a2])

    def test_other_user(self):
        '''It rejects a request from another user.'''
        user2 = models.new_user(username='another', password='user')
        models.new_school(user=user2)
        self.client.login(username='another', password='user')

        response = self.get_response()
        self.assertPermissionDenied(response)

        response = self.get_response(params={'school_id': self.school.id})
        self.assertPermissionDenied(response)

    def test_superuser(self):
        '''It returns the assignment summary for a superuser.'''
        models.new_superuser(username='test', password='user')
        self.client.login(username='test', password='user')

        response = self.get_response()
        self.assert_assignment_summaries_equal(response, [self.a1, self.a2, self.a3])

        response = self.get_response(params={'school_id': self.school.id})
        self.assert_assignment_summaries_equal(response, [self.a1, self.a2])

    def assert_assignment_summaries_equal(self, response, assignment_summaries):
        '''Assert that the response contains the assignment summaries in order.'''
        self.assertEqual(response.data, [{
            'name': a.id,
            'summary': a.summary,
            'published_summary': a.published_summary
        } for a in assignment_summaries])
