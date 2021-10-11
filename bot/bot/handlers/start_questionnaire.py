from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext

from .base import send_question, send_category_title
from .base import update_user_context
from ..keyboards import QuestionKeyboardMarkupFactory
from ...api import Questionnaire


GREETINGS_MESSAGE = "Hello! 👋 We are glad to see you in our " \
    "<b>Doctorinna</b> Telegram bot. You will be given a set questions in {} "\
    "categories. Most of the questions require choosing one variant from " \
    "the given ones via inline buttons 📋, " \
    "and some require typing in the number 📝."


async def start_questionnaire_handler(
        message: types.Message,
        state: FSMContext,
        questionnaire: Questionnaire,
        keyboard_markup_factory: QuestionKeyboardMarkupFactory):
    await message.answer(GREETINGS_MESSAGE.format(questionnaire.size))

    first_category = questionnaire.get_category(category_index=0)
    first_question = first_category.get_question(question_index=0)
    await update_user_context(state, 0, 0, first_question)

    await send_category_title(message, category_index=0,
                              category=first_category)
    await send_question(message, keyboard_markup_factory, question_index=0,
                        category=first_category, question=first_question)


def register_start_questionnaire_handler(dp: Dispatcher):
    dp.register_message_handler(start_questionnaire_handler,
                                commands=['start'])
