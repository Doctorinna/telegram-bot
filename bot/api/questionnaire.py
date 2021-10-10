from typing import Optional, Union, Any

from aiohttp import ClientSession

from .questions import QuestionsCategory, parse_questions_category
from .requester import Requester


class Questionnaire:
    def __init__(self, categories: list[QuestionsCategory]):
        self._categories = categories

    @property
    def size(self) -> int:
        return len(self._categories)

    def get_category(self, category_index: int) -> QuestionsCategory:
        return self._categories[category_index]

    def get_next_indices(self, category_index: int, question_index: int) -> \
            Optional[tuple[int, int]]:
        # case: the very last question
        if question_index == self.get_category(category_index).size - 1 and \
                category_index == self.size - 1:
            return None
        # case: last question in the category
        elif question_index == self.get_category(category_index).size - 1:
            return category_index + 1, 0

        return category_index, question_index + 1


class QuestionnaireAPI:
    def __init__(self, api_url: str):
        self._API_URL: str = api_url
        self._session = ClientSession()
        self._requester = Requester(self._session)
        self._questionnaire: Optional[Questionnaire] = None

    @property
    def questionnaire(self):
        return self._questionnaire

    async def retrieve_questionnaire(self):
        categories_info = await self._retrieve_categories_info()
        questions_categories = []
        for category_info in categories_info:
            questions_category = await self._retrieve_questions_category(
                category_id=category_info['id'],
                category_name=category_info['title']
            )
            questions_categories.append(questions_category)
        questionnaire = Questionnaire(questions_categories)
        self._questionnaire = questionnaire

    async def _retrieve_categories_info(self) \
            -> list[dict[str, Union[int, str]]]:
        uri = '/risks/categories'
        response = await self._requester.request('GET', self._API_URL + uri)
        categories_info = await response.json()
        return categories_info

    async def _retrieve_questions_category(
            self,
            category_id: int,
            category_name: str) -> QuestionsCategory:
        uri = f'/risks/questions/{category_name}'
        response = await self._requester.request('GET', self._API_URL + uri)
        raw_questions = await response.json()
        questions_category = parse_questions_category(category_id,
                                                      category_name,
                                                      raw_questions)
        return questions_category

    async def get_results(self, session: ClientSession,
                          answers: list[dict[str, Union[str, Any]]]) -> dict:
        requester = Requester(session)
        send_answers_uri = '/risks/response/'
        await requester.request(
            method='POST',
            url=self._API_URL + send_answers_uri,
            json=answers
        )

        get_results_uri = '/risks/result/'
        response = await requester.request(method='GET',
                                           url=self._API_URL + get_results_uri)
        result = await response.json()
        return result

    async def close(self):
        await self._session.close()
