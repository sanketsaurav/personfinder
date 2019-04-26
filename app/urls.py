# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""URL routing module."""

from django.conf import urls

import site_settings
import tasksmodule.deletion
import tasksmodule.sitemap_ping
import views.admin.acls
import views.admin.api_keys
import views.admin.create_repo
import views.admin.delete_record
import views.admin.statistics
import views.meta.sitemap

# We include an optional trailing slash in all the patterns (Django has support
# for automatic redirection, but we don't want to send people redirect responses
# if it's not really needed).
_BASE_URL_PATTERNS = [
    ('admin_acls', r'(?P<repo>[^\/]+)/admin/acls/?',
     views.admin.acls.AdminAclsView.as_view),
    ('admin_apikeys-list', r'(?P<repo>[^\/]+)/admin/api_keys/list/?',
     views.admin.api_keys.ApiKeyListView.as_view),
    ('admin_apikeys-manage', r'(?P<repo>[^\/]+)/admin/api_keys/?',
     views.admin.api_keys.ApiKeyManagementView.as_view),
    ('admin_create-repo', r'global/admin/create_repo/?',
     views.admin.create_repo.AdminCreateRepoView.as_view),
    ('admin_delete-record', r'(?P<repo>[^\/]+)/admin/delete_record/?',
     views.admin.delete_record.AdminDeleteRecordView.as_view),
    ('admin_statistics', r'global/admin/statistics/?',
     views.admin.statistics.AdminStatisticsView.as_view),
    ('meta_sitemap', r'global/sitemap/?',
     views.meta.sitemap.SitemapView.as_view),
    ('tasks_process-expirations',
     r'(?P<repo>[^\/]+)/tasks/process_expirations/?',
     tasksmodule.deletion.ProcessExpirationsTask.as_view),
    ('tasks_cleanup-stray-notes',
     r'(?P<repo>[^\/]+)/tasks/cleanup_stray_notes/?',
     tasksmodule.deletion.CleanupStrayNotesTask.as_view),
    ('tasks_cleanup-stray-subscriptions',
     r'(?P<repo>[^\/]+)/tasks/cleanup_stray_subscriptions/?',
     tasksmodule.deletion.CleanupStraySubscriptionsTask.as_view),
    ('tasks_sitemap-ping', r'global/tasks/sitemap_ping/?',
     tasksmodule.sitemap_ping.SitemapPingTaskView.as_view),
]

# pylint: disable=invalid-name
# Pylint would prefer that this name be uppercased, but Django's going to look
# for this value in the urls module; it has to be called urlpatterns.
urlpatterns = [
    urls.url('^%s$' % path_exp, view_func(), name=name)
    for (name, path_exp, view_func) in _BASE_URL_PATTERNS
]

if site_settings.OPTIONAL_PATH_PREFIX:
    urlpatterns += [
        urls.url(
            '^%(prefix)s/%(path)s$' % {
                'prefix': site_settings.OPTIONAL_PATH_PREFIX,
                'path': path_exp
            },
            view_func(),
            name='prefixed__%s' % name)
        for (name, path_exp, view_func) in _BASE_URL_PATTERNS
    ]