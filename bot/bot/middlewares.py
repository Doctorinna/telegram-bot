from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from .keyboards import QuestionKeyboardMarkupFactory
from ..api import QuestionnaireAPI


class DataMiddleware(BaseMiddleware):
    def __init__(self, questionnaire_api: QuestionnaireAPI,
                 keyboard_markup_factory: QuestionKeyboardMarkupFactory):
        super().__init__()
        self._questionnaire_api = questionnaire_api
        self._keyboard_markup_factory = keyboard_markup_factory

    def _pass_parameters(self, data: dict):
        data['questionnaire'] = self._questionnaire_api.questionnaire
        data['keyboard_markup_factory'] = self._keyboard_markup_factory
        data['questionnaire_api'] = self._questionnaire_api

    async def _pass_user_context(self, data: dict):
        user_data = await data['state'].get_data()
        curr_category_index = user_data['curr_category_index']
        curr_question_index = user_data['curr_question_index']
        curr_category = self._questionnaire_api.questionnaire.get_category(
            category_index=curr_category_index
        )
        curr_question = curr_category.get_question(curr_question_index)

        data['curr_category_index'] = curr_category_index
        data['curr_question_index'] = curr_question_index
        data['curr_question'] = curr_question

    async def on_process_message(self, message: types.Message, data: dict):
        self._pass_parameters(data)
        if data.get('command') is None:
            await self._pass_user_context(data)

    async def on_process_callback_query(self,
                                        callback_query: types.CallbackQuery,
                                        data: dict):
        self._pass_parameters(data)
        await self._pass_user_context(data)
