# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=R
from flask import request
from flask_appbuilder import expose, ModelRestApi
from flask_appbuilder.security.decorators import has_access_api
import simplejson as json

from superset import appbuilder, db, event_logger, security_manager
from superset.common.query_context import QueryContext
from superset.legacy import update_time_range
# import superset.models.core as models
from superset.utils import core as utils
from .base import api, BaseSupersetView, handle_api_exception
from flask_appbuilder.models.sqla.interface import SQLAInterface
import superset.models.core as models
from flask_appbuilder.security.sqla import models as ab_models

class Api(BaseSupersetView):
    @event_logger.log_this
    @api
    @handle_api_exception
    @has_access_api
    @expose("/v1/query/", methods=["POST"])
    def query(self):
        """
        Takes a query_obj constructed in the client and returns payload data response
        for the given query_obj.
        params: query_context: json_blob
        """
        query_context = QueryContext(**json.loads(request.form.get("query_context")))
        security_manager.assert_datasource_permission(query_context.datasource)
        payload_json = query_context.get_payload()
        return json.dumps(
            payload_json, default=utils.json_int_dttm_ser, ignore_nan=True
        )

    @event_logger.log_this
    @api
    @handle_api_exception
    @has_access_api
    @expose("/v1/form_data/", methods=["GET"])
    def query_form_data(self):
        """
        Get the formdata stored in the database for existing slice.
        params: slice_id: integer
        """
        form_data = {}
        slice_id = request.args.get("slice_id")
        if slice_id:
            slc = db.session.query(models.Slice).filter_by(id=slice_id).one_or_none()
            if slc:
                form_data = slc.form_data.copy()

        update_time_range(form_data)

        return json.dumps(form_data)


class ExampleModelApi(ModelRestApi):
    class_permission_name = "CssTemplateAsyncModelView"
    method_permission_name = {
        "get_list": "list",
        "get": "show",
        "post": "add",
        "put": "edit",
        "delete": "delete",
        "info": "list",
    }
    previous_method_permission_name = {
        "get_list": "access",
        "get": "access",
        "post": "access",
        "put": "access",
        "delete": "access",
        "info": "access"
    }
    resource_name = 'example'
    datamodel = SQLAInterface(models.CssTemplate)
    allow_browser_login = True


class UserModelApi(ModelRestApi):
    class_permission_name = "CssTemplateAsyncModelView"
    method_permission_name = {
        "get_list": "list",
        "get": "show",
        "post": "add",
        "put": "edit",
        "delete": "delete",
        "info": "list",
    }
    previous_method_permission_name = {
        "get_list": "access",
        "get": "access",
        "post": "access",
        "put": "access",
        "delete": "access",
        "info": "access"
    }
    resource_name = 'test'
    datamodel = SQLAInterface(ab_models.User)
    allow_browser_login = True

appbuilder.add_api(UserModelApi);
appbuilder.add_api(ExampleModelApi)
appbuilder.add_view_no_menu(Api)
