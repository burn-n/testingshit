import random

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

    main()
