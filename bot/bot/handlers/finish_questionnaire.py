import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession, CookieJar, ClientError

from ...api import QuestionnaireAPI

logger = logging.getLogger(__name__)


async def finish_questionnaire(message: types.Message,
                               state: FSMContext,
                               questionnaire_api: QuestionnaireAPI):
    user_data = await state.get_data()
    user_data.pop('curr_category_index')
    user_data.pop('curr_question_index')

    user_answers = []
    for question_id, answer in user_data.items():
        user_answer = {
            'question': question_id,
            'answer': answer
        }
        user_answers.append(user_answer)

    session = ClientSession(cookie_jar=CookieJar(unsafe=True))
    try:
        questionnaire_result = await questionnaire_api.get_results(
            session=session,
            answers=user_answers
        )
    except (ClientError, asyncio.TimeoutError) as err:
        logger.exception(err)
        await message.answer('Sorry, something went wrong')
    else:
        await send_questionnaire_result(message, questionnaire_result)
    finally:
        await session.close()


async def send_questionnaire_result(message: types.Message,
                                    questionnaire_result: dict):
    for disease_result in questionnaire_result:
        illness_name = disease_result['disease']['illness'].capitalize()
        illness_description = disease_result['disease']['description']
        risk_factor = int(round(disease_result['risk_factor'], 2) * 100)
        prescription = disease_result['prescription']

        message_text = f'<b>{illness_name}</b>\n{illness_description}' \
                       f'\n\n❕ Risk factor: {risk_factor}\n' \
                       f'Prescription:\n{prescription}'

        await message.answer(message_text)
