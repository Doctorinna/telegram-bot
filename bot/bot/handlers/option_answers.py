from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .base import update_user_context, send_question, send_category_title
from .finish_questionnaire import finish_questionnaire
from ..keyboards import QuestionKeyboardMarkupFactory
from ..states import QuestionnaireStates
from ...api import Question, Questionnaire


async def option_answer_handler(
        callback_query: types.CallbackQuery,
        callback_data: dict[str, str],
        state: FSMContext,
        questionnaire: Questionnaire,
        keyboard_markup_factory: QuestionKeyboardMarkupFactory,
        curr_category_index: int,
        curr_question_index: int,
        curr_question: Question,
):
    answer_option_index = int(callback_data['answer_option_index'])
    chosen_option_answer = curr_question.answer_options[answer_option_index]

    await callback_query.answer()
    await callback_query.message.edit_reply_markup()
    await callback_query.message.edit_text(f'{callback_query.message.text}\n'
                                           f'{chosen_option_answer.text}')

    # save user's answer to the storage
    await state.update_data({curr_question.id: chosen_option_answer.text})

    next_indices = questionnaire.get_next_indices(curr_category_index,
                                                  curr_question_index)
    if next_indices is None:
        await finish_questionnaire(callback_query.message, state)
        await state.reset_state()
        await state.reset_data()
        return

    next_category_index = next_indices[0]
    next_question_index = next_indices[1]
    next_category = questionnaire.get_category(next_category_index)
    next_question = next_category.get_question(next_question_index)
    await update_user_context(state, next_category_index,
                              next_question_index, next_question)

    if next_category_index != curr_category_index:
        await send_category_title(callback_query.message, next_category_index,
                                  next_category)
    await send_question(callback_query.message, keyboard_markup_factory,
                        next_question_index, next_category, next_question)


def register_answer_options_handler(
        dp: Dispatcher,
        keyboard_markup_factory: QuestionKeyboardMarkupFactory
):
    dp.register_callback_query_handler(
        option_answer_handler,
        keyboard_markup_factory.filter(),
        state=QuestionnaireStates.options_question)
    dp.register_callback_query_handler(
        option_answer_handler,
        keyboard_markup_factory.filter(),
        state=QuestionnaireStates.combined_question
    )
