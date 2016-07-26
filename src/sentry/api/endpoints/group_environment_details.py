from __future__ import absolute_import

from rest_framework.response import Response

from sentry.api.base import StatsMixin
from sentry.api.bases.group import GroupEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models.grouprelease import (
    GroupReleaseWithStatsSerializer
)
from sentry.models import Environment, GroupRelease, ReleaseEnvironment


class GroupEnvironmentDetailsEndpoint(GroupEndpoint, StatsMixin):
    def get(self, request, group, environment):
        environment = Environment.objects.get(
            project_id=group.project_id,
            # XXX(dcramer): we have no great way to pass the empty env
            name='' if environment == 'none' else environment,
        )

        first_release = GroupRelease.objects.filter(
            group_id=group.id,
            environment=environment.name,
        ).order_by('first_seen').first()

        last_release = GroupRelease.objects.filter(
            group_id=group.id,
            environment=environment.name,
        ).order_by('-first_seen').first()

        # the current release is the 'latest seen' release within the
        # environment even if it hasnt affected this issue
        current_release = GroupRelease.objects.filter(
            group_id=group.id,
            environment=environment.name,
            release_id=ReleaseEnvironment.objects.filter(
                project_id=group.project_id,
                environment_id=environment.id,
            ).order_by('-first_seen').values_list('release_id', flat=True).first(),
        ).first()

        stats_args = self._parse_args(request)

        context = {
            'environment': serialize(environment, request.user),
            'firstRelease': serialize(first_release, request.user),
            'lastRelease': serialize(last_release, request.user),
            'currentRelease': serialize(
                current_release, request.user, GroupReleaseWithStatsSerializer(
                    since=stats_args['start'],
                    until=stats_args['end'],
                )
            ),
        }
        return Response(context)
