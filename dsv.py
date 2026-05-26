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
    "MULTI_TOKEN": False,
    "TOKENS": [
        # "token1",
        # "token2"
    ],
    "WEBHOOK_URL": "",
    "DEFAULT_DELAY": 1,
    "STRING": True,
    "DIGITS": True,
    "PUNCTUATION": False,
    "MODE": 1,
    "USERNAME_LENGTH": 4,
    "GENERATE_COUNT": 25,
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
    main()
