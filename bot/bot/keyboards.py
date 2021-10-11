from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from ..api import Question


class QuestionKeyboardMarkupFactory:
    """
    Factory to create keyboard markups for questions with answer options
    """

    def __init__(self):
        self._callback_data_factory = CallbackData('q', 'answer_option_index')

    def new(self, question: Question) -> Optional[InlineKeyboardMarkup]:
        if question.answer_options is None:
            return None
        keyboard_markup = InlineKeyboardMarkup(row_width=1)
        self._insert_answer_option_buttons(keyboard_markup, question)
        return keyboard_markup

    def _insert_answer_option_buttons(self,
                                      keyboard_markup: InlineKeyboardMarkup,
                                      question: Question):
        for i in range(len(question.answer_options)):
            button = InlineKeyboardButton(
                text=question.answer_options[i].text,
                callback_data=self._callback_data_factory.new(
                    answer_option_index=i
                )
            )
            keyboard_markup.insert(button)

    def filter(self):
        return self._callback_data_factory.filter()
