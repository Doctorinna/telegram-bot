

class BaseAnswer:
    def __init__(self, id_: int):
        self._id = id_

    @property
    def id(self):
        return self._id


class AnswerOption(BaseAnswer):
    def __init__(self, id_: int, text: str):
        super().__init__(id_)
        self._text = text

    @property
    def text(self):
        return self._text


def parse_answer_options(raw_answer_options: list[dict]) -> list[AnswerOption]:
    answer_options = []
    for raw_answer_option in raw_answer_options:
        answer_option = AnswerOption(
            id_=raw_answer_option['id'],
            text=raw_answer_option['answer']
        )
        answer_options.append(answer_option)
    return answer_options


class AnswerRange(BaseAnswer):
    def __init__(self, id_: int, min_value: int, max_value: int):
        super().__init__(id_)
        self._min_value = min_value
        self._max_value = max_value

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value


def parse_answer_range(raw_answer_range: dict) -> AnswerRange:
    return AnswerRange(
        id_=raw_answer_range['id'],
        min_value=raw_answer_range['min'],
        max_value=raw_answer_range['max']
    )
