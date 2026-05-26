import random
import string
import requests
import time
import json
import datetime
import sys
from colorama import Fore, init

init(autoreset=True)

__version__ = "GitHub Actions DSV 2.0"
__github__ = "https://github.com/suenerve"

# =========================
# CONFIG
# =========================
CONFIG = {
    "TOKEN": "PUT_YOUR_DISCORD_TOKEN_HERE",
    "MULTI_TOKEN": True,
    "TOKENS": [
        "NjY4Mzk4OTMyNDUxMjYyNDk1.GbJkyR.ai5jaYNMXaXcqDkHP-eQeA7chfQWF3cqsF4WDc",
        "NzI0OTc5MDI2ODkyMDMwMDM0.GTQLnN.X-vC3GsnbdaJ3LQHMI0vrOh3cdOZhrD-MuUixE"
    ],
    "WEBHOOK_URL": "https://discord.com/api/webhooks/1508590349713408231/CIljNz9hoywwrkH9ZJ7cjWVwUi5gogPNdGlWXzYucncqQb13qZZpB6D-Vi6wCSaeZ4WT",
    "DEFAULT_DELAY": 4,
    "STRING": True,
    "DIGITS": True,
    "PUNCTUATION": False,
    "MODE": 1,
    "USERNAME_LENGTH": 4,
    "GENERATE_COUNT": 15,
    "USERNAME_LIST": [
        "testuser",
        "example123"
    ]
}

# =========================
# GLOBALS
# =========================
available_usernames = []
integ_0 = 0
sample_0 = "_."

sys_url = "https://discord.com/api/v9/users/@me"
URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

# =========================
# TOKEN HANDLING
# =========================
def avail_tokens():
    return CONFIG["TOKENS"]


def s_sys_h():
    global integ_0

    if CONFIG["MULTI_TOKEN"]:
        tokens = avail_tokens()
        token = tokens[integ_0]
    else:
        token = CONFIG["TOKEN"]

    return {
        "Content-Type": "application/json",
        "Origin": "https://discord.com/",
        "Authorization": token
    }

def sys_c_t():
    if CONFIG["MULTI_TOKEN"]:
        if len(avail_tokens()) == 0:
            print("[ERROR] MULTI_TOKEN is enabled but no tokens were supplied.")
            sys.exit(1)
    else:
        if CONFIG["TOKEN"] == "PUT_YOUR_DISCORD_TOKEN_HERE" or not CONFIG["TOKEN"]:
            print("[ERROR] No Discord token configured.")
            sys.exit(1)

# =========================
# CONFIG SETUP
# =========================
def setconf():
    global string_0
    global digits_0
    global punctuation_0
    global webhook_0

    sat_string = CONFIG["STRING"]
    sat_digits = CONFIG["DIGITS"]
    sat_punct = CONFIG["PUNCTUATION"]

    webhook_0 = CONFIG["WEBHOOK_URL"] != ""

    string_0 = string.ascii_lowercase if sat_string else ""
    digits_0 = string.digits if sat_digits else ""
    punctuation_0 = sample_0 if sat_punct else ""

    if not string_0 and not digits_0 and not punctuation_0:
        string_0 = string.ascii_lowercase

# =========================
# MAIN
# =========================
def main():
    print("=" * 80)
    print(__version__)
    print(__github__)
    print("=" * 80)

    sys_c_t()
    setconf()

    try:
        user = requests.get(sys_url, headers=s_sys_h()).json()
        print(f"[INFO] Connected as: {user.get('username')}#{user.get('discriminator')}")
    except Exception as e:
        print(f"[ERROR] Failed to fetch account info: {e}")

    print(f"[INFO] Delay: {CONFIG['DEFAULT_DELAY']}s")
    print(f"[INFO] String chars: {CONFIG['STRING']}")
    print(f"[INFO] Digits: {CONFIG['DIGITS']}")
    print(f"[INFO] Punctuation: {CONFIG['PUNCTUATION']}")
    print(f"[INFO] Multi-token: {CONFIG['MULTI_TOKEN']}")

    if CONFIG["MODE"] == 1:
        opt1func(CONFIG["GENERATE_COUNT"], CONFIG["USERNAME_LENGTH"])
    elif CONFIG["MODE"] == 2:
        validate_names(2, CONFIG["USERNAME_LIST"])

# =========================
# VALIDATION
# =========================
def validate_names(opt, usernames):
    global available_usernames
    global integ_0

    if opt == 2:
        for username in usernames:
            validate_single(username)

    elif opt == 1:
        validate_single(usernames)

# =========================
# SINGLE VALIDATION
# =========================
def validate_single(username):
    global integ_0

    body = {
        "username": username
    }

    time.sleep(CONFIG["DEFAULT_DELAY"])

    print(f"[CHECKING] {username}")

    try:
        endpoint = requests.post(URL, headers=s_sys_h(), json=body)
        json_endpoint = endpoint.json()

        print(f"[DEBUG] Status Code: {endpoint.status_code}")
        print(f"[DEBUG] Response: {json.dumps(json_endpoint)}")

        if endpoint.status_code == 429:
            if CONFIG["MULTI_TOKEN"] and len(avail_tokens()) > 1:
                integ_0 = (integ_0 + 1) % len(avail_tokens())
                print(f"[RATE LIMIT] Switched token index to {integ_0}")
                return
            else:
                sleep_time = json_endpoint.get("retry_after", 5)
                print(f"[RATE LIMIT] Sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
                return

        if json_endpoint.get("taken") is False:
            print(f"[AVAILABLE] {username}")
            available_usernames.append(username)
            save(username)
            ch_send_webhook(username)

        elif json_endpoint.get("taken") is True:
            print(f"[TAKEN] {username}")

        else:
            print(f"[ERROR] Unexpected response: {json.dumps(json_endpoint)}")

    except Exception as e:
        print(f"[EXCEPTION] {e}")

# =========================
# SAVE RESULTS
# =========================
def save(content):
    with open("available_usernames.txt", "a", encoding="utf-8") as file:
        file.write(f"{content}\n")

    print(f"[SAVED] {content} -> available_usernames.txt")

# =========================
# WEBHOOK
# =========================
def ch_send_webhook(val0: str):
    if not webhook_0:
        return

    webhook = Discord(url=CONFIG["WEBHOOK_URL"])

    try:
        webhook.post(
            username="DSV",
            embeds=[
                {
                    "title": f"Username: `{val0}` is available.",
                    "timestamp": str(datetime.datetime.utcnow()),
                    "color": 16768000
                }
            ]
        )

        print(f"[WEBHOOK] Sent notification for {val0}")

    except Exception as e:
        print(f"[WEBHOOK ERROR] {e}")

# =========================
# GENERATION
# =========================
def opt1func(v1, v2):
    print(f"[INFO] Generating {v1} usernames with length {v2}")

    for i in range(v1):
        name = get_names(v2)
        print(f"[GENERATED] {name}")
        validate_names(1, name)

    print("=" * 80)
    print(f"[DONE] Found {len(available_usernames)} available usernames")
    print("=" * 80)

# =========================
# RANDOM NAME
# =========================
def get_names(length: int) -> str:
    chars = string_0 + digits_0 + punctuation_0
    return ''.join(random.sample(chars, length))

# =========================
# DISCORD WEBHOOK CLASS
# =========================
class Discord:
    def __init__(self, *, url):
        self.url = url

    def post(
        self,
        *,
        content=None,
        username=None,
        avatar_url=None,
        tts=False,
        file=None,
        embeds=None,
        allowed_mentions=None
    ):
        if content is None and file is None and embeds is None:
            raise ValueError("required one of content, file, embeds")

        data = {}

        if content is not None:
            data["content"] = content

        if username is not None:
            data["username"] = username

        if avatar_url is not None:
            data["avatar_url"] = avatar_url

        data["tts"] = tts

        if embeds is not None:
            data["embeds"] = embeds

        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions

        if file is not None:
            return requests.post(
                self.url,
                {"payload_json": json.dumps(data)},
                files=file
            )
        else:
            return requests.post(
                self.url,
                json.dumps(data),
                headers={"Content-Type": "application/json"}
            )


if __name__ == "__main__":
    main()
