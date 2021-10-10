from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .base import update_user_context, send_question, send_category_title
from .finish_questionnaire import finish_questionnaire
from ..keyboards import QuestionKeyboardMarkupFactory
from ..states import QuestionnaireStates
from ...api import Question, Questionnaire, QuestionnaireAPI


async def range_answer_handler(
        message: types.Message,
        state: FSMContext,
        questionnaire: Questionnaire,
        keyboard_markup_factory: QuestionKeyboardMarkupFactory,
        questionnaire_api: QuestionnaireAPI,
        curr_category_index: int,
        curr_question_index: int,
        curr_question: Question
):
    answer = message.text
    # validate input
    try:
        answer = int(answer)
    except ValueError:
        await message.answer('Incorrect input. '
                             'The answer should be a number. '
                             'Please try again')
        return
    if answer < curr_question.answer_range.min_value or \
            answer > curr_question.answer_range.max_value:
        await message.answer('Incorrect input. '
                             'The number is invalid. Please try again')
        return

    # save user's answer to the storage
    await state.update_data({curr_question.id: answer})

    next_indices = questionnaire.get_next_indices(curr_category_index,
                                                  curr_question_index)
    if next_indices is None:
        await finish_questionnaire(message, state, questionnaire_api)
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
        await send_category_title(message, next_category_index, next_category)
    await send_question(message, keyboard_markup_factory, next_question_index,
                        next_category, next_question)


def register_range_answers_handler(dp: Dispatcher):
    dp.register_message_handler(range_answer_handler,
                                state=QuestionnaireStates.range_question)
    dp.register_message_handler(range_answer_handler,
                                state=QuestionnaireStates.combined_question)
