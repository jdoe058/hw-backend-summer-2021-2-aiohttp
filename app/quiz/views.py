from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema, ThemeRequestSchema,
)
from app.web.app import View
from app.web.utils import json_response
from aiohttp.web_exceptions import HTTPConflict


# TODO: добавить проверку авторизации для этого View
class ThemeAddView(View):
    # TODO: добавить валидацию с помощью aiohttp-apispec и marshmallow-схем
    @request_schema(ThemeRequestSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        data = self.request['data']
        theme = await self.store.quizzes.get_theme_by_title(data['title'])

        if theme:
            raise HTTPConflict

        title = (await self.request.json())[
            "title"
        ]  # TODO: заменить на self.data["title"] после внедрения валидации

        # TODO: проверять, что не существует темы с таким же именем, отдавать 409 если существует
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(View):
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={'themes': raw_themes})


class QuestionAddView(View):
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
