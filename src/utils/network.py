# -*- encoding: utf-8 -*-
# src/utils/network.py
# Helper functions for network operations.


import time
import ujson
import httpx
import asyncio
import websockets

from functools import wraps
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from solana.exceptions import SolanaRpcException

from src.utils.config import load_config
from src.utils.logging import log_debug, log_error, exit_with_error


async def get_async_sleep(sleep_time) -> None:
    """Async sleep function."""
    await asyncio.sleep(int(sleep_time))


def get_fast_decoded_rpc_response(raw_response: bytes) -> dict:
    """Decode a raw response from the RPC."""
    return ujson.loads(raw_response)


def craft_url(url: str, endpoint: str) -> str:
    """Add an url to an endpoint."""
    return urljoin(url, endpoint)


def format_perc(value: float) -> str:
    """Format a percentage float to a well-suitable string."""
    return "%.8f%%" % (100 * value)


def format_price(value: float) -> str:
    """Format a price float to a well-suitable rounded string."""
    return "{:.2f}".format(round(value, 2))


def get_request(url: str) -> dict:
    """Sends a GET request to the given URL."""
    try:
        return httpx.get(url)
    except httpx.HTTPStatusError as e:
        log_error(f'Coud not connect to {url}: {e}')

def html_to_json(response: httpx.Response):
    """
    Process the HTTP response based on its content type. If the content type is JSON, 
    format and print it. If the content type is HTML, extract and convert JSON from 
    HTML to a formatted JSON string.

    Args:
        response (httpx.Response): The HTTP response object to process.
    """
    content_type = response.headers.get('Content-Type', '')

    if 'application/json' in content_type:
        # Convert the response to JSON
        try:
            data = response.json()
            return data

        except ujson.JSONDecodeError:
            exit_with_error("Error decoding JSON.")
    
    elif 'text/html' in content_type:
        # Parse the HTML content and extract the JSON
        soup = BeautifulSoup(response.text, 'html.parser')
        code_block = soup.find('code')
        if code_block:
            try:
                json_text = code_block.get_text(strip=True)
                data = ujson.loads(json_text)
                return data
            except ujson.JSONDecodeError:
                exit_with_error("Error decoding JSON from HTML.")
        else:
            exit_with_error("No JSON code block found in the HTML response.")
    else:
        exit_with_error("Received an unknown content type:", content_type)
        exit_with_error(response.text)


def post_request(url, data=None, headers=None) -> dict:
    """Wrapper for httpx package to handle POST requests."""
    if headers is None:
        headers = {'Content-Type': 'application/json'}

    try:
        # If data is a dictionary or list, use the json parameter
        if isinstance(data, (dict, list)):
            response = httpx.post(url, json=data, headers=headers)
        else:
            # If data is a string, ensure it's valid JSON and use content parameter
            response = httpx.post(url, content=data, headers=headers)
    except httpx.HTTPStatusError as e:
        exit_with_error(f'Could not connect to {url}: {e}')

    if (response.status_code == 201 or response.status_code == 200): #201 posted succesfully
        return response.json()
    else:
        exit_with_error(f'Error: {response.text}')


async def get_async_request(url: str) -> dict:
    """Wrapper for httpx.get() with error handling."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    except httpx.HTTPStatusError as e:
        log_error(f'Could not connect to {url}: {e}')


async def post_async_request(url: str, data: dict) -> dict:
    """Wrapper for httpx.post() with error handling."""
    try:
      async with httpx.AsyncClient() as client:
          response = await client.post(
              url,
              headers={"Content-Type": "application/json"},
              json=data  # Use the `json` parameter to automatically set the content type
          )
          response.raise_for_status()  # Raises an exception for 4xx/5xx responses
          return response.json()  # Parse JSON response
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors (e.g., 4xx, 5xx)
        return {"error": str(e)}
    except Exception as e:
        # Handle other possible exceptions
        return {"error": str(e)}

def rate_limited() -> callable:
    """Decorator to handle rate limiting in the Solana API."""

    RATE_LIMIT_MAX_RETRIES = 5
    RATE_LIMIT_DELAY = 5

    def decorator(client):
        @wraps(client)
        def wrapper(*args, **kwargs):
            for _ in range(RATE_LIMIT_MAX_RETRIES):
                try:
                    return client(*args, **kwargs)
                except SolanaRpcException as e:
                    if 'HTTPStatusError' in e.error_msg:
                        log_debug(f'Rate limit exceeded in {client.__name__}')
                        log_debug(f'Retrying in {RATE_LIMIT_DELAY}s...')
                        time.sleep(RATE_LIMIT_DELAY)
                    else:
                        raise
            log_debug('Rate limit error. Skipping this iteration.')
        return wrapper
    return decorator


async def ws_subscribe(url: str, subscription_request: dict, callback: callable, timeout: int = None, config: dict = None) -> None:
    """Subscribe to a websocket endpoint."""

    if not timeout:
        config = config or load_config()
        timeout = int(config['WEBSOCKET_TIMEOUT'])

    async with websockets.connect(url) as ws:
        await ws.send(ujson.dumps(subscription_request))
        subscription_response = await ws.recv()
        log_debug(subscription_response)

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=timeout)
                message = ujson.loads(message)
                task = asyncio.create_task(callback(message))
                await task

            except Exception as e:
                log_error(f'Error in websocket subscription: {e}')
                continue


async def ws_reloop(stream: callable, tag: str, websocket_delay: int = None, config: dict = None) -> None:
    """Main loop for the websocket reconnection."""

    if not websocket_delay:
        config = config or load_config()
        websocket_delay = int(config['WEBSOCKET_DELAY'])

    while True:
        try:
            await stream()

        except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as e:
            log_error(f'Websocket connection closed: {e}. Reconecting...')
            await asyncio.sleep(websocket_delay)
        except ConnectionError as e:
            log_error(f'An error has occurred with {tag} websocket: {e}')
            break


async def ws_publish(url: str, message: dict, config: dict = None) -> None:
    """Publish a message to a websocket endpoint."""
    config = config or load_config()

    async with websockets.connect(url) as ws:
        await ws.send(ujson.dumps(message))
        log_debug(f'Message published to {url}: {message}')
