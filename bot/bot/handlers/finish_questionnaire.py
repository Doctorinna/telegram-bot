import asyncio
import logging
import os
import uuid
from typing import Union

import matplotlib.pyplot as plt
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
        await send_statistics_images(message, questionnaire_api,
                                     session, questionnaire_result)
    finally:
        await session.close()


async def send_questionnaire_result(message: types.Message,
                                    questionnaire_result: dict):
    await message.answer('📄 Results:')

    for disease_result in questionnaire_result:
        illness_name = disease_result['disease']['illness'].capitalize()
        illness_description = disease_result['disease']['description']
        risk_factor = int(round(disease_result['risk_factor'], 2) * 100)
        prescription = disease_result['prescription']

        message_text = f'📍<b>{illness_name}</b>\n{illness_description}' \
                       f'\n\n❕ Risk factor: <b><i>{risk_factor}/100</i></b>\n'\
                       f'Prescription:\n{prescription}'

        await message.answer(message_text)


async def send_statistics_images(message: types.Message,
                                 questionnaire_api: QuestionnaireAPI,
                                 session: ClientSession,
                                 questionnaire_result: dict):
    await message.answer('📊 Statistics by regions:')

    for disease_result in questionnaire_result:
        illness_name = disease_result['disease']['illness']
        try:
            statistics = await questionnaire_api.get_illness_statistics(
                session=session,
                illness_name=illness_name
            )
        except (ClientError, asyncio.TimeoutError) as err:
            logger.exception(err)
            continue

        statistics_image_path = get_statistic_image(illness_name,
                                                    statistics['country'])
        statistics_image = open(statistics_image_path, 'rb')
        await message.answer_photo(statistics_image)
        statistics_image.close()
        if os.path.isfile(statistics_image_path):
            os.remove(statistics_image_path)


def get_statistic_image(
        illness_name: str,
        statistics: list[dict[str, Union[str, int]]]) -> str:
    regions = []
    factor_values = []
    for region_statistics in statistics:
        if region_statistics['region'] != "It's private":
            regions.append(region_statistics['region'])
            factor_values.append(region_statistics['avg_factor'] * 100)

    plt.figure(figsize=(3 * len(regions), 5))
    plt.title(illness_name.capitalize())
    plt.bar(regions, factor_values)
    plt.xlabel('Regions')
    plt.ylabel('Average risk factors')

    image_name = uuid.uuid4()
    image_path = f"/tmp/{image_name}.jpg"
    plt.savefig(image_path)
    plt.close()
    return image_path
