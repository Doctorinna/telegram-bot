import asyncio
import logging
from time import time

from aiohttp import ClientSession, ClientTimeout, ClientResponse


class Requester:
    """
    Wrapper around ClientSession to retry requests in case of timeouts and
    log them
    """

    def __init__(self, session: ClientSession,
                 timeout: int = 3,
                 tries: int = 2):
        if timeout < 1:
            raise ValueError('timeout should be greater than 0')
        if tries < 1:
            raise ValueError('tries should be greater than 0')

        self._MAX_TIMEOUT = 16
        self._MAX_TRIES = 4
        self._timeout = min(timeout, self._MAX_TIMEOUT)
        self._tries = min(tries, self._MAX_TRIES)
        self._session = session
        self._logger = logging.getLogger(__name__)

    async def request(self, method: str, url: str, **kwargs) -> ClientResponse:
        timeout = ClientTimeout(total=self._timeout)

        for i in range(self._tries - 1):
            time_start = time()
            try:
                response = await self._session.request(method, url,
                                                       timeout=timeout,
                                                       **kwargs)
            except asyncio.TimeoutError:
                self._logger.warning(f"{method.upper()} {url} "
                                     f"{timeout.total}s timeout")
                timeout = ClientTimeout(
                    total=min(timeout.total * 2, self._MAX_TIMEOUT)
                )
            else:
                time_end = time()
                self._log_response(response, time_end - time_start)
                response.raise_for_status()
                return response

        time_start = time()
        response = await self._session.request(method, url,
                                               timeout=timeout, **kwargs)
        time_end = time()
        self._log_response(response, time_end - time_start)
        response.raise_for_status()
        return response

    def _log_response(self, response: ClientResponse, time_: float):
        log_message = f"{response.method} {response.url} {response.status} " \
                      f"{round(time_, 2)}s"
        if response.ok:
            self._logger.info(log_message)
        else:
            self._logger.error(log_message)
