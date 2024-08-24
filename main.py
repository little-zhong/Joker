from DrissionPage import WebPage
from logger import logger
import time
import subprocess


ppp = WebPage()
ppp.listen.start()


def func_nonce(authorization, missions, last_pow_id):
    payload = missions["result"]["payload"]
    require = missions["result"]["require"]
    start_time = time.time()
    result = subprocess.run(
        ["./find", payload, require, "12"],
        stdout=subprocess.PIPE,
    )
    nonce = result.stdout.decode().strip()
    logger.info(f"Found nonce: {nonce} / Time: {time.time() - start_time:.2f}s")  # fmt: skip

    js_data = """
        // WARNING: For POST requests, body is set to null by browsers.
var data = JSON.stringify({
  "nonce": "fuck_joker",
  "pow_id": "fuck_again"
});

var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "https://blockjoker.org/api/v2/missions/nonce");
xhr.setRequestHeader("accept", "application/json, text/plain, */*");
xhr.setRequestHeader("accept-language", "zh-CN,zh;q=0.9");
xhr.setRequestHeader("authorization", "Bearer fuckfuck");
xhr.setRequestHeader("content-type", "application/json");
xhr.setRequestHeader("origin", "https://blockjoker.org");
xhr.setRequestHeader("priority", "u=1, i");
xhr.setRequestHeader("referer", "https://blockjoker.org/home");
xhr.setRequestHeader("sec-fetch-dest", "empty");
xhr.setRequestHeader("sec-fetch-mode", "cors");
xhr.setRequestHeader("sec-fetch-site", "same-origin");
xhr.setRequestHeader("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36");

xhr.send(data);
        """
    js_data = js_data.replace("fuck_joker", nonce)
    js_data = js_data.replace("fuck_again", last_pow_id)
    js_data = js_data.replace("fuckfuck", authorization)
    ppp.run_js_loaded(js_data)


def func_missions(authorization) -> dict:
    js_data = """
    // WARNING: For POST requests, body is set to null by browsers.
var data = JSON.stringify({});

var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function() {
  if(this.readyState === 4) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "https://blockjoker.org/api/v2/missions");
xhr.setRequestHeader("accept", "application/json, text/plain, */*");
xhr.setRequestHeader("accept-language", "zh-CN,zh;q=0.9");
xhr.setRequestHeader("authorization", "Bearer fuckfuck");
xhr.setRequestHeader("content-type", "application/json");
// WARNING: Cookies will be stripped away by the browser before sending the request.
xhr.setRequestHeader("origin", "https://blockjoker.org");
xhr.setRequestHeader("priority", "u=1, i");
xhr.setRequestHeader("referer", "https://blockjoker.org/home");
xhr.setRequestHeader("sec-fetch-dest", "empty");
xhr.setRequestHeader("sec-fetch-mode", "cors");
xhr.setRequestHeader("sec-fetch-site", "same-origin");
xhr.setRequestHeader("user-agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36");

xhr.send(data);
"""
    js_data = js_data.replace("fuckfuck", authorization)
    ppp.run_js_loaded(js_data)


def main():
    last_pow_id = None
    while True:
        try:
            res = ppp.listen.wait()

            if res.url == "https://blockjoker.org/api/v2/missions/pow-records":
                authorization = ppp.local_storage()["BLOCK_JOKER_ACCESS_TOKEN"]
                authorization = authorization.replace('"', "")
                last_pow_id = res.response.body["result"][0]["pow_id"]
                func_missions(authorization)

            if res.url == "https://blockjoker.org/api/v2/missions/nonce":
                nonce = res.response.body
                if not nonce.get("result"):
                    continue
                else:
                    last_pow_id = res.response.body["result"][0]["pow_id"]
                    rewards = res.response.body["result"][0]["rewards"]
                    logger.success(f"Pushed pow_id: {last_pow_id} / Reward: {rewards}")  # fmt: skip

            if res.url == "https://blockjoker.org/api/v2/missions":
                func_nonce(authorization, res.response.body, last_pow_id)
                func_missions(authorization)
        except Exception as e:
            ppp.refresh()
            logger.error(e)


if __name__ == "__main__":
    main()
