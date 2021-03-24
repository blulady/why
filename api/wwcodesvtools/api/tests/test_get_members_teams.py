import json
from django.test import TransactionTestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TestGetMembersTeams(TransactionTestCase):
    reset_sequences = True
    fixtures = ['get_members_data.json']

    def setUp(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        self.access_token = self.get_token(self.username, self.password)
        self.bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.access_token)}

    def get_token(self, username, password):
        s = TokenObtainPairSerializer(data={
            TokenObtainPairSerializer.username_field: self.username,
            'password': self.password,
        })
        self.assertTrue(s.is_valid())
        return s.validated_data['access']

    # Testing get members with user teams
    def test_get_members_teams(self):
        self.username = 'director@example.com'
        self.password = 'Password123'
        access_token = self.get_token(self.username, self.password)
        bearer = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(access_token)}
        response = self.client.get("/api/users/?ordering=first_name", **bearer)

        self.assertEqual(json.loads(response.content)[0]['first_name'], 'Alice')
        self.assertEqual(json.loads(response.content)[0]['teams'][0]['id'], 4)
        self.assertEqual(json.loads(response.content)[0]['teams'][0]['name'], 'Partnership Management')
        self.assertEqual(json.loads(response.content)[0]['teams'][1]['id'], 5)
        self.assertEqual(json.loads(response.content)[0]['teams'][1]['name'], 'Social Media')
        self.assertEqual(json.loads(response.content)[0]['teams'][2]['id'], 3)
        self.assertEqual(json.loads(response.content)[0]['teams'][2]['name'], 'Host Management')

        self.assertEqual(json.loads(response.content)[1]['first_name'], 'Bruno')
        self.assertEqual(json.loads(response.content)[1]['teams'][0]['id'], 1)
        self.assertEqual(json.loads(response.content)[1]['teams'][0]['name'], 'Event Volunteers')
        self.assertEqual(json.loads(response.content)[1]['teams'][1]['id'], 7)
        self.assertEqual(json.loads(response.content)[1]['teams'][1]['name'], 'Volunteer Management')

        self.assertEqual(json.loads(response.content)[2]['first_name'], 'Caroline')
        self.assertEqual(json.loads(response.content)[2]['teams'], [])