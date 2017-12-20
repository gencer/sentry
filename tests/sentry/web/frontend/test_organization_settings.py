from __future__ import absolute_import

# from django.core import mail
from django.core.urlresolvers import reverse

# from sentry.models import AuditLogEntry, AuditLogEntryEvent, OrganizationMember
from sentry.testutils import TestCase, APITestCase, PermissionTestCase
from sentry.models import Authenticator, TotpInterface, Organization


class Organization2FAPermissionTest(PermissionTestCase):
    def setUp(self):
        super(Organization2FAPermissionTest, self).setUp()
        owner = self.create_user()
        organization = self.create_organization(owner=owner)

        self.org_settings_path = reverse(
            'sentry-organization-member-settings', args=[self.organization.slug, owner.id]
        )
        self.org_path = reverse(
            'sentry-organization-home', args=[organization.slug]
        )
        # Add Members
        user1 = self.create_user(is_superuser=False)
        user2 = self.create_user(is_superuser=False)
        user3 = self.create_user(is_superuser=False)

        self.create_member(user=user1, organization=organization, role="member")
        self.create_member(user=user2, organization=organization, role="admin")
        self.create_member(user=user3, organization=organization, role="manager")

    def test_manager_member_can_load(self):
        self.assert_manager_can_access(self.org_settings_path)

    def test_non_compliant_member_cannot_load(self):
        self.assert_non_member_cannot_access(self.path)

    def test_compliant_member_can_load(self):
        self.assert_member_can_access(self.path)

    def test_compliant_member_remove_2FA_cannot_load(self):
        pass


class OrganizationSettingsTest(TestCase):
    def test_renders_with_context(self):
        pass


class OrganizationSettings2FATest(APITestCase):
    def enable_user_2fa(self, user):
        TotpInterface().enroll(user)
        assert Authenticator.objects.user_has_2fa(user)

    def assert_can_enable_2FA(self, organization, user, status_code=200):
        self.assert_cannot_enable_2FA(organization, user, status_code)

    def assert_cannot_enable_2FA(self, organization, user, status_code):
        def enable_org_2fa():
            self.login_as(user)
            url = reverse(
                'sentry-api-0-organization-details', kwargs={
                    'organization_slug': organization.slug,
                }
            )
            response = self.client.put(
                url,
                data={
                    'require2FA': True,
                }
            )
            return response

        response = enable_org_2fa()

        assert response.status_code == status_code, response.content
        organization = Organization.objects.get(id=organization.id)
        if status_code == 200:
            assert organization.flags.require_2fa
        else:
            assert not organization.flags.require_2fa

    def test_cannot_set_enforce_2fa_without_2fa(self):
        owner = self.user
        organization = self.create_organization(owner=owner)
        assert not Authenticator.objects.user_has_2fa(owner)

        self.enable_user_2fa(owner)
        self.assert_can_enable_2FA(organization, owner)

    def test_owner_can_set_2fa(self):
        owner = self.user
        organization = self.create_organization(owner=owner)

        self.enable_user_2fa(owner)
        self.assert_can_enable_2FA(organization, owner)

    def test_manager_can_set_2fa(self):
        manager = self.create_user()
        organization = self.create_organization(owner=self.create_user())
        self.create_member(organization=organization, user=manager, role="manager")

        self.assert_cannot_enable_2FA(organization, manager, 400)
        self.enable_user_2fa(manager)
        self.assert_can_enable_2FA(organization, manager)

    def test_members_cannot_set_2fa(self):
        member = self.create_user()
        organization = self.create_organization(owner=self.create_user())
        self.create_member(organization=organization, user=member, role="member")

        self.assert_cannot_enable_2FA(organization, member, 403)
        self.enable_user_2fa(member)
        self.assert_cannot_enable_2FA(organization, member, 403)

    def test_new_member_must_enable_2FA(self):
        # prior to joing!
        pass

    def test_non_compliant_members_notified(self):
        # recieve an email that 2FA must be enabled
        pass

    def test_new_sentry_user_join_must_enable_2FA(self):
        pass

    def test_non_complaint_members_are_blocked(self):
        pass

    def test_member_disable_all_2FA_blocked(self):
        pass
