from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester', email='tester@email.com', password='pass'
        )
        self.snack = Snack.objects.create(
            name='Licorice Twizzlers', description='impossible to eat', purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), 'Licorice Twizzlers')

    def test_snack_content(self):
        self.assertEqual(f'{self.snack.name}', 'Licorice Twizzlers')
        self.assertEqual(f'{self.snack.purchaser}', 'tester')
        self.assertEqual(f'{self.snack.description}', 'impossible to eat')

    def test_snack_list_view(self):
        response = self.client.get(reverse('list_snack'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Licorice Twizzlers')
        self.assertTemplateUsed(response, 'snack_list.html')

    def test_snack_detail_view(self):
        response = self.client.get(reverse('detail_snack', args='1'))
        no_response = self.client.get('/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Purchaser: tester')
        self.assertTemplateUsed(response, 'snack_detail.html')

    def test_snack_create_view(self):
        response = self.client.post(
            reverse('create_snack'),
            {
                'name': 'Fermented Tofu',
                'description': 'mmmm',
                'purchaser': self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse('list_snack'))
        self.assertContains(response, 'Fermented Tofu')

    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse('update_snack', args='1'),
            {'name': 'Updated name', 'description': 'new description',
                'purchaser': self.user.id}
        )

        self.assertRedirects(response, reverse('detail_snack', args='1'))

    def test_snack_delete_view(self):
        response = self.client.get(reverse('delete_snack', args='1'))
        self.assertEqual(response.status_code, 200)
