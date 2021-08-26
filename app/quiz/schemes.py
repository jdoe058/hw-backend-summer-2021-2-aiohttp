from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class ThemeRequestSchema(Schema):
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True)


class QuestionIdScheme(QuestionSchema):
    id = fields.Int(required=True)


class ThemeListSchema(Schema):
    pass


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    pass
