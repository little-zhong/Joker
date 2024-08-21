import os
import time
import asyncio
import functools
import subprocess
from logger import logger
from calc import generate
from dotenv import load_dotenv
from typing import Callable, Type, Any

from curl_cffi.requests import AsyncSession

load_dotenv()

api_key = os.getenv("CAPSOLVER_API_KEY")
site_key = "0x4AAAAAAAhcU20JhZDJJSS_"
site_url = "https://blockjoker.org/home"


def retry(
    max_retries: int = 3,
    delay: int = 2,
    exceptions: tuple[Type[Exception]] = (Exception,),
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries < max_retries:
                        logger.warning(f"Retry {retries}/{max_retries} for {func.__name__} due to {e}. Retrying in {delay} seconds...")  # fmt: skip
                        await asyncio.sleep(delay)
                    else:
                        logger.error(f"Failed after {retries} retries.")
                        raise

        return wrapper

    return decorator


class Joker:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def capsolver(self):
        payload = {
            "clientKey": api_key,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteKey": site_key,
                "websiteURL": site_url,
            },
        }
        res = await self.session.post(
            "https://api.capsolver.com/createTask", json=payload
        )
        resp = res.json()
        task_id = resp.get("taskId")
        if not task_id:
            logger.error(f"Failed to create task: {res.text}")
            return
        logger.info(f"Got taskId: {task_id} / Getting result...")

        while True:
            await asyncio.sleep(2)
            payload = {"clientKey": api_key, "taskId": task_id}
            res = await self.session.post(
                "https://api.capsolver.com/getTaskResult", json=payload
            )
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                return resp.get("solution", {}).get("token")
            if status == "failed" or resp.get("errorId"):
                logger.error(f"Solve failed! response: {res.text}")
                return

    async def _request(self, method, url, status_code: tuple[int, ...], **kwargs):
        response = await self.session.request(
            method,
            url,
            **kwargs,
        )
        if response.status_code not in status_code:
            if response.status_code == 502:
                raise Exception("Bad Gateway")
            if response.status_code == 504:
                raise Exception("Gateway Timeout")
            if response.status_code == 521:
                logger.error("Server Down")
                exit(0)
            raise Exception(f"status_code: {response.status_code} {response.text}")
        if "cloudflare" in response.text:
            raise Exception(f"cloudflare: {response.text}")
        return response

    async def accounts(self):
        return await self._request(
            "GET", "https://blockjoker.org/api/v2/accounts", (200,)
        )

    async def version(self):
        return await self._request(
            "GET", "https://blockjoker.org/api/v2/version", (200,)
        )

    @retry()
    async def missions(self, cf_response=""):
        return await self._request(
            "POST",
            "https://blockjoker.org/api/v2/missions",
            (200,),
            json={"cf_response": cf_response},
        )

    async def pow_records(self):
        return await self._request(
            "GET", "https://blockjoker.org/api/v2/missions/pow-records", (200,)
        )

    @retry()
    async def nonce(self, nonce, pow_id=None):
        json_data = {"nonce": nonce}
        if pow_id:
            json_data["pow_id"] = pow_id
        response = await self._request(
            "POST",
            "https://blockjoker.org/api/v2/missions/nonce",
            (200,),
            json=json_data,
        )
        result = response.json()
        return result


async def work(user_jwt):
    async with AsyncSession(
        impersonate="chrome124",
        headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7",
            "authorization": "Bearer " + user_jwt,
            "content-type": "application/json",
            "origin": "https://blockjoker.org",
            "priority": "u=1, i",
            "referer": "https://blockjoker.org/home",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        },
        timeout=60,
    ) as session:
        joker = Joker(session)
        last_pow_id = None
        first_capsolver = await joker.capsolver()
        pow_records = await joker.pow_records()

        if not pow_records.json()["result"]:
            logger.warning(f"Failed to get pow_records: {pow_records.text}")
        else:
            last_pow_id = pow_records.json()["result"][0]["pow_id"]

        while True:
            try:
                # get mission
                start_info = await joker.missions(first_capsolver)
                result = start_info.json().get("result")
                if not result:
                    logger.warning(f"Failed to get mission: {start_info.text}")
                    continue
                payload, require = result["payload"], result["require"]
                logger.info(f"Received mission: {payload} / {require}")

                # generate nonce and hash
                # nonce, hash = generate(payload, require)
                start_time = time.time()
                result = subprocess.run(
                    ["./find", payload, require, "12"],
                    stdout=subprocess.PIPE,
                )
                nonce = result.stdout.decode().strip()
                logger.info(f"Found nonce: {nonce} / Time: {time.time() - start_time:.2f}s")  # fmt: skip
                # push nonce to server
                if last_pow_id:
                    push_info = await joker.nonce(nonce, last_pow_id)
                else:
                    push_info = await joker.nonce(nonce)

                if not push_info.get("result"):
                    continue
                else:
                    # system rewards every 5 minutes, and change pow_id
                    last_pow_id = push_info["result"][0]["pow_id"]
                    rewards = push_info["result"][0]["rewards"]
                    logger.success(f"Pushed nonce: {nonce} / Reward: {rewards}")  # fmt: skip
                # get accounts and version
                accounts = await joker.accounts()
                point = accounts.json()["result"]["point"]
                logger.success(f"Current point: {point}")
                version = await joker.version()
            except Exception as e:
                logger.error(e)


async def main():
    auth_list = open("auth.txt", "r").read().splitlines()
    tasks = [asyncio.create_task(work(auth)) for auth in auth_list]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
