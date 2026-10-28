from django.test import TestCase
from django.urls import reverse
from .forms import AccountRoleForm, adminRegistrationForm
from .models import Account


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


class AccountRoleFormTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(
            email="role-user@example.com",
            username="role-user",
        )

    def test_role_form_can_promote_user_to_admin(self):
        form = AccountRoleForm(
            data={"role": "admin"},
            account=self.account,
        )

        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.account.refresh_from_db()

        self.assertTrue(self.account.is_admin)
        self.assertTrue(self.account.is_staff)
        self.assertFalse(self.account.is_superuser)

    def test_role_form_can_promote_user_to_superuser(self):
        form = AccountRoleForm(
            data={"role": "superuser"},
            account=self.account,
        )

        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.account.refresh_from_db()

        self.assertTrue(self.account.is_admin)
        self.assertTrue(self.account.is_staff)
        self.assertTrue(self.account.is_superuser)


class AccountRolePermissionTests(TestCase):
    def setUp(self):
        self.superuser = Account.objects.create(
            email="superuser@example.com",
            username="superuser",
            is_admin=True,
            is_staff=True,
            is_superuser=True,
        )
        self.regular_user = Account.objects.create(
            email="regular@example.com",
            username="regular",
        )
        self.target = Account.objects.create(
            email="target@example.com",
            username="target",
        )

    def test_regular_user_cannot_promote_an_account(self):
        self.client.force_login(self.regular_user)

        response = self.client.post(
            reverse('update_account_role', args=[self.target.pk]),
            {'role': 'admin'},
        )

        self.assertEqual(response.status_code, 403)
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_admin)
        self.assertFalse(self.target.is_superuser)

    def test_superuser_can_promote_an_account(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse('update_account_role', args=[self.target.pk]),
            {'role': 'admin'},
        )

        self.assertEqual(response.status_code, 302)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_admin)
        self.assertTrue(self.target.is_staff)
        self.assertFalse(self.target.is_superuser)

    def test_superuser_cannot_remove_own_superuser_access(self):
        self.client.force_login(self.superuser)

        response = self.client.post(
            reverse('update_account_role', args=[self.superuser.pk]),
            {'role': 'user'},
        )

        self.assertEqual(response.status_code, 302)
        self.superuser.refresh_from_db()
        self.assertTrue(self.superuser.is_superuser)
