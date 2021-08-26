from hashlib import sha256

from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminSchema, AdminResponseSchema, UserSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminResponseSchema)
    async def post(self):
        data = self.request['data']
        admin = await self.store.admins.get_by_email(data['email'])

        if admin:
            if sha256(str(data['password']).encode()).hexdigest() == admin.password:
                return json_response(data=UserSchema().dump(admin))
        raise HTTPForbidden


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
