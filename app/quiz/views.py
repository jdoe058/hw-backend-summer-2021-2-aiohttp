from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema, ThemeRequestSchema, QuestionSchema, QuestionIdScheme,
)
from app.web.app import View
from app.web.utils import json_response
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest


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
    @request_schema(QuestionSchema)
    async def post(self):
        data = self.request['data']

        if len(data['answers']) == 1:
            raise HTTPBadRequest

        count = 0
        for answer in data['answers']:
            if answer['is_correct']:
                count += 1

        if count != 1:
            raise HTTPBadRequest

        theme = await self.store.quizzes.get_theme_by_id(data['theme_id'])

        if not theme:
            raise HTTPNotFound

        question = await self.store.quizzes.create_question(
            title=data['title'],
            theme_id=data['theme_id'],
            answers=data['answers']
        )
        return json_response(data=QuestionIdScheme().dump(question))


class QuestionListView(View):
    async def get(self):
        raise NotImplementedError
