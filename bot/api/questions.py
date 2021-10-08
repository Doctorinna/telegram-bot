from typing import Optional

from .answers import AnswerOption, parse_answer_options, AnswerRange, \
    parse_answer_range


class Question:
    def __init__(self,
                 id_: int,
                 text: str,
                 answer_options: Optional[list[AnswerOption]],
                 answer_range: Optional[AnswerRange]):
        self._id = id_
        self._text = text
        self._answer_options = answer_options
        self._answer_range = answer_range

    @property
    def id(self) -> int:
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def answer_options(self):
        return self._answer_options

    @property
    def answer_range(self):
        return self._answer_range


def parse_question(raw_question: dict) -> Question:
    answer_options = None
    if len(raw_question['options']) != 0:
        answer_options = parse_answer_options(raw_question['options'])

    answer_range = None
    if raw_question['range'] is not None:
        answer_range = parse_answer_range(raw_question['range'])

    return Question(
        id_=raw_question['id'],
        text=raw_question['description'],
        answer_options=answer_options,
        answer_range=answer_range
    )


class QuestionsCategory:
    def __init__(self,
                 id_: int,
                 title: str,
                 questions: list[Question]):
        self._id = id_
        self._title = title
        self._questions = questions

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def size(self):
        return len(self._questions)

    def get_question(self, question_index) -> Question:
        return self._questions[question_index]


def parse_questions_category(category_id: int,
                             category_name: str,
                             raw_questions: dict) -> QuestionsCategory:
    questions: list[Question] = []
    for raw_question in raw_questions:
        question = parse_question(raw_question)
        questions.append(question)
    questions_category = QuestionsCategory(
        id_=category_id,
        title=category_name,
        questions=questions
    )
    return questions_category
