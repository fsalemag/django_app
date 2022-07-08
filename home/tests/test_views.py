from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from activities.models import Category
from utils.test_utils import create_activities_and_categories
from ..views import index


class TestHome:
    index_url = reverse("home-index")

    def create_activities_from_extra_settings(self, extra_settings):
        settings = {}
        for setting in extra_settings:
            settings.update({
                setting[0]: {
                    "count": setting[1],
                    "date": timezone.now() - timedelta(days=setting[2])
                }
            })
        create_activities_and_categories(settings)

    def test_index_status_code(self, rf, users):
        request = rf.get(self.index_url)
        request.user = users

        response = index(request)
        assert response.status_code == 200

    # TODO add more cases
    def test_index_context_metrics(self, client):
        response = client.get(self.index_url)
        context = response.context

        expected_context = {
            'n_activities': 14,
            'n_users': 2,
            'n_month_activities': 12,
        }

        for variable in expected_context.keys():
            assert context.get(variable) == expected_context[variable]

    # TODO add more cases
    @pytest.mark.parametrize(
        "extra_settings,expected_order",
        [
            ((("football", 2, 5), ("tennis", 1, 5)), ("football", "tennis", "padel"))
        ]
    )
    def test_index_top_categories(self, client, extra_settings, expected_order):
        self.create_activities_from_extra_settings(extra_settings)

        response = client.get(self.index_url)
        context = response.context

        assert list(context.get("top_categories")) == \
               list(
                   [Category.objects.get(name=category) for category in expected_order]
               )

    # TODO add more cases
    @pytest.mark.parametrize(
        "extra_settings,expected_order",
        [
            ((("football", 2, 5), ("tennis", 1, 5)), ("football", "tennis", "volleyball"))
        ]
    )
    def test_index_trending_categories(self, client, extra_settings, expected_order):
        self.create_activities_from_extra_settings(extra_settings)

        response = client.get(self.index_url)
        context = response.context

        assert list(context.get("trending_categories")) == \
               list(
                   [Category.objects.get(name=category) for category in expected_order]
               )
