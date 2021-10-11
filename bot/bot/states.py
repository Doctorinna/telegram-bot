from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionnaireStates(StatesGroup):
    options_question = State()
    range_question = State()
    combined_question = State()
