import time
import random
import uuid
import sys
from curl_cffi import requests

# الروابط والمستهدفات الخاصة بالمنصة
BASE_URL = "https://codemap-25.taqat.academy/"
VOTE_URL = "https://codemap-25.taqat.academy/api/public/showcase/cmqw94mpa0003jb0a6x83rxhk/vote"
PROJECT_ID = "cmp8byr1j0004jm04a7i79hc3"

def print_log(msg):
    """طباعة فورية تظهر مباشرة في سجلات Render/Terminal"""
    print(msg, flush=True)

def get_free_proxies():
    print_log("[*] جاري جلب قائمة بروكسيات مجانية حديثة...")
    try:
        # جلب قائمة البروكسيات باستخدام curl_cffi
        response = requests.get(
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
            timeout=10
        )
        if response.status_code == 200:
            proxies = [p.strip() for p in response.text.strip().split("\r\n") if p.strip()]
            print_log(f"[+] تم جلب {len(proxies)} بروكسي بنجاح!")
            return proxies
    except Exception as e:
        print_log(f"[-] فشل جلب البروكسيات: {e}")
    return []

def simulate_and_vote(project_id, proxy_address):
    # توليد المعرفات الفريدة
    fingerprint = str(uuid.uuid4())
    vote_id = str(uuid.uuid4())

    proxy_config = {
        "http": f"http://{proxy_address}",
        "https": f"http://{proxy_address}"
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
        "Origin": "https://codemap-25.taqat.academy",
        "Referer": "https://codemap-25.taqat.academy/",
        "Sec-CH-UA": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": f"taqat_vote_id={vote_id}; __Secure-authjs.callback-url=https%3A%2F%2Fcodemap-25.taqat.academy"
    }

    try:
        # إنشاء جلسة مع محاكاة متصفح Chrome لتجاوز الـ Anti-Bot
        session = requests.Session(impersonate="chrome120")
        session.proxies = proxy_config
        session.headers.update(headers)

        # 🚀 الخطوة 1: محاكاة زيارة إنسانية مسبقة
        print_log(f"[*] تجربة البروكسي: {proxy_address}")
        init_res = session.get(BASE_URL, timeout=5)
        
        if init_res.status_code != 200:
            return False

        # ⏳ انتظار عشوائي لمحاكاة السلوك البشري
        time.sleep(random.uniform(1.5, 3.0))

        payload = {
            "projectId": project_id,
            "fingerprint": fingerprint
        }

        # 🚀 الخطوة 2: إرسال التصويت
        print_log(f"[*] إرسال طلب التصويت...")
        response = session.post(VOTE_URL, json=payload, timeout=5)
        
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("error") == "ip-cap":
                print_log(f"[-] البروكسي {proxy_address} مستهلك مسبقاً (ip-cap).")
                return False
            else:
                print_log(f"[+] نجاح! تم تسجيل الصوت عبر البروكسي: {proxy_address}")
                return True
        elif response.status_code == 403:
            print_log(f"[-] تم رفض الطلب (403 Forbidden) من السيرفر.")
            return False
        else:
            return False
    except Exception:
        # إهمال البروكسيات البطئية أو الميتة
        return False

if __name__ == "__main__":
    proxy_list = get_free_proxies()
    if not proxy_list:
        print_log("[-] لا توجد بروكسيات للبدء. إغلاق السكربت.")
        sys.exit(1)

    TOTAL_VOTES_NEEDED = 10000  # الهدف
    successful_votes = 0
    proxy_index = 0

    print_log(f"🚀 بدء التشغيل الفوري للسكربت المطور للمشروع: {PROJECT_ID}...")

    while successful_votes < TOTAL_VOTES_NEEDED and proxy_index < len(proxy_list):
        current_proxy = proxy_list[proxy_index]
        proxy_index += 1
        
        print_log(f"\n--- [ محاولة رقم {successful_votes + 1} | البروكسي {proxy_index}/{len(proxy_list)} ] ---")
        success = simulate_and_vote(PROJECT_ID, current_proxy)
        
        if success:
            successful_votes += 1
            sleep_time = random.uniform(4, 8)
            print_log(f"[*] صوت ناجح! انتظار {sleep_time:.2f} ثوانٍ للتمويه...")
            time.sleep(sleep_time)
        else:
            print_log("[*] البروكسي غير صالح أو فشل الطلب، الانتقال للتالي...")

    print_log(f"\n🎉 انتهت العملية! إجمالي الأصوات الناجحة: {successful_votes}")
