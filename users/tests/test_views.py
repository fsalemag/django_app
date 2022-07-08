from django.urls import reverse

from django.urls import reverse

from ..models import UserProfile
from ..views import ProfileActivityView, ProfileView


class TestUser:
    user_profile_url = "users-profile"
    login_url = 'account_login'
    external_profile_url = "users-external-profile"
    user_activities_url = "users-activities"

    def test_profile_page_logged_in_user_status_code(self, rf, my_user):
        request = rf.get(self.user_profile_url)
        request.user = my_user

        response = ProfileView.as_view()(request)
        assert response.status_code == 200

    def test_profile_page_logged_in_user(self, client):
        assert client.login(email="dummy@dummy.com", password="dummy_password")

        context = client.get(reverse(self.user_profile_url)).context

        assert UserProfile.objects.get(user__email="dummy@dummy.com") == context.get("user_profile")

    def test_profile_page_not_logged_in_user(self, client):
        url = reverse(self.user_profile_url)
        response = client.get(url)

        assert response.status_code == 302
        assert reverse(self.login_url) == response.url

    def test_profile_page_other_user(self, client):
        url = reverse(self.external_profile_url, kwargs={"pk": 2})
        context = client.get(url).context

        assert UserProfile.objects.get(user__email="dummy2@dummy.com") == context.get("user_profile")

    def test_activities_mine_page_status_code(self, rf, my_user):
        request = rf.get(self.user_activities_url)
        request.user = my_user

        response = ProfileActivityView.as_view()(request)
        assert response.status_code == 200

    def test_activities_mine_page(self, client):
        assert client.login(email="dummy@dummy.com", password="dummy_password")

        url = reverse(self.user_activities_url)

        context = client.get(url).context

        assert UserProfile.objects.get(user__email="dummy@dummy.com") == context["userprofile"]
