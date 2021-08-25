from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminSchema, AdminResponseSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminResponseSchema)
    async def post(self):
        data = self.request['data']
        if data['email'] != 'admin@admin.com' or data['password'] != 'admin':
            raise HTTPForbidden
        return json_response(data={'id': 1, 'email': 'admin@admin.com'})


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
