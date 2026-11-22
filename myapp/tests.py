from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import User


class PeopleJourneyTests(TestCase):
    def create_person(self, name, email, mobile_number='555-0123', password='not-for-display'):
        return User.objects.create(
            name=name,
            email=email,
            password=password,
            mobile_number=mobile_number,
            date_of_birth=date(1990, 1, 1),
        )

    def test_directory_search_matches_name_email_and_phone(self):
        ada = self.create_person('Ada Lovelace', 'ada@example.com', '555-0198')
        self.create_person('Grace Hopper', 'grace@example.com', '555-0155')

        for search_term in ('ada lovelace', 'ADA@EXAMPLE', '555-0198'):
            with self.subTest(search_term=search_term):
                response = self.client.get(reverse('user_list'), {'q': search_term})

                self.assertContains(response, ada.name)
                self.assertNotContains(response, 'Grace Hopper')
                self.assertContains(response, '1 result')

    def test_directory_shows_helpful_empty_search_state(self):
        response = self.client.get(reverse('user_list'), {'q': 'nobody'})

        self.assertContains(response, 'No matches found')
        self.assertContains(response, 'Try another name, email, or phone number.')

    def test_person_details_do_not_reveal_password(self):
        person = self.create_person(
            'Ada Lovelace',
            'ada@example.com',
            password='private-value',
        )

        response = self.client.get(reverse('view_user', args=[person.id]))

        self.assertContains(response, person.email)
        self.assertNotContains(response, 'private-value')

    def test_form_uses_masked_password_and_native_date_input(self):
        response = self.client.get(reverse('add_user'))

        self.assertContains(response, 'type="password"')
        self.assertContains(response, 'type="date"')

    def test_edit_form_hides_and_preserves_password_when_left_blank(self):
        person = self.create_person(
            'Ada Lovelace',
            'ada@example.com',
            password='private-value',
        )
        edit_url = reverse('edit_user', args=[person.id])

        response = self.client.get(edit_url)
        self.assertContains(response, 'Leave blank to keep the current password.')
        self.assertNotContains(response, 'private-value')

        response = self.client.post(edit_url, {
            'name': person.name,
            'email': person.email,
            'password': '',
            'mobile_number': person.mobile_number,
            'date_of_birth': '1990-01-01',
        })

        self.assertRedirects(response, reverse('user_list'))
        person.refresh_from_db()
        self.assertEqual(person.password, 'private-value')
