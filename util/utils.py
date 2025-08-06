import logging
from typing import Callable, TypeVar

import requests
from tenacity import (
    after_log,
    before_log,
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from common.config import BASE_URL, DEFAULT_TIMEOUT, Api
from common.logger import setup_logger

logger = setup_logger(__name__)

retry_decorator = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    reraise=True,
    before=before_log(logger, logging.DEBUG),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO),
)


def api_builder(
    endpoint: Api,
    resource_id: str | int = "",
    suffix: Api = "",
    start_index: int | None = None,
) -> str:
    url = f"{BASE_URL}{endpoint.value}"

    if resource_id != "":
        url += str(resource_id)

    if suffix != "":
        url += suffix.value

    if start_index is not None:
        url += str(start_index)

    return url


T = TypeVar("T")


@retry_decorator
def _fetch(url: str, timeout: int, extractor: Callable[[requests.Response], T]) -> T:
    logger.debug(f"Requesting URL: {url}")
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return extractor(response)


def fetch_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    return _fetch(url, timeout, lambda r: r.json())


def fetch_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _fetch(url, timeout, lambda r: r.text)
