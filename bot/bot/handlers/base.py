import roman
from aiogram import types
from aiogram.dispatcher import FSMContext

from ..keyboards import QuestionKeyboardMarkupFactory
from ..states import QuestionnaireStates
from ...api import Question, QuestionsCategory


async def update_user_context(state: FSMContext,
                              category_index: int,
                              question_index: int,
                              question: Question):
    await state.update_data({'curr_category_index': category_index,
                             'curr_question_index': question_index})

    if question.answer_options and question.answer_range:
        await state.set_state(QuestionnaireStates.combined_question.state)
    elif question.answer_options:
        await state.set_state(QuestionnaireStates.options_question.state)
    elif question.answer_range:
        await state.set_state(QuestionnaireStates.range_question.state)


async def send_question(message: types.Message,
                        keyboard_markup_factory: QuestionKeyboardMarkupFactory,
                        question_index: int, category: QuestionsCategory,
                        question: Question):
    await message.answer(
        text=f'❓ ({question_index + 1}/{category.size}) {question.text}',
        reply_markup=keyboard_markup_factory.new(question)
    )


async def send_category_title(message: types.Message, category_index: int,
                              category: QuestionsCategory):
    await message.answer(
        f'<b>{roman.toRoman(category_index + 1)}. '
        f'{category.title.capitalize()}</b>'
    )
