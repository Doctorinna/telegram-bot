from .start_questionnaire import register_start_questionnaire_handler
from .option_answers import register_answer_options_handler
from .range_answers import register_range_answers_handler
from aiogram import Dispatcher
from ..keyboards import QuestionKeyboardMarkupFactory


def register_questionnaire_handlers(
        dp: Dispatcher,
        keyboard_markup_factory: QuestionKeyboardMarkupFactory
):
    register_start_questionnaire_handler(dp)
    register_answer_options_handler(dp, keyboard_markup_factory)
    register_range_answers_handler(dp)
