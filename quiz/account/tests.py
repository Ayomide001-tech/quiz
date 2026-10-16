from django.test import TestCase
from .forms import adminRegistrationForm


class AdminRegistrationFormTests(TestCase):
    def test_save_creates_admin_without_superuser_privileges(self):
        password = "safe-passphrase-927!"
        form = adminRegistrationForm(data={
            "email": "new-admin@example.com",
            "username": "new-admin",
            "password1": password,
            "password2": password,
        })

        self.assertTrue(form.is_valid(), form.errors)
        account = form.save()

        self.assertTrue(account.is_admin)
        self.assertTrue(account.is_staff)
        self.assertFalse(account.is_superuser)
