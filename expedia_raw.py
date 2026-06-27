from playwright.sync_api import sync_playwright
import json
import time

raw_responses = []

def capture_response(response):
    try:
        url = response.url
        if any(keyword in url for keyword in [
            'hotel-search', 'properties', 'lodging',
            'graphql', 'api.expedia', 'hotelSearch'
        ]):
            if response.status == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type or 'graphql' in url:
                    try:
                        body = response.json()
                        raw_responses.append({
                            'url': url,
                            'status': response.status,
                            'body': body
                        })
                        print(f"[CAPTURED] {url}")
                    except Exception:
                        pass
    except Exception as e:
        print(f"[SKIP] {e}")

def get_browser_context_and_page(playwright):
    try:
        browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        print("Connected to existing Chrome via CDP.")
        return browser, context, page
    except Exception as e:
        print(f"CDP connection failed ({e}); starting a local browser instead.")
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        return browser, context, page

with sync_playwright() as p:
    browser, context, page = get_browser_context_and_page(p)

    page.on("response", capture_response)

    print("Connected to real Chrome. Opening Expedia...")

    search_url = (
        "https://www.expedia.com/Hotel-Search"
        "?destination=California%2C+United+States+of+America"
        "&startDate=07%2F26%2F2026"
        "&endDate=07%2F30%2F2026"
        "&rooms=1"
        "&adults=1"
    )

    page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
    print(" Page loaded. Waiting for results...")
    time.sleep(8)

    print("Starting scroll and capture...")

    for i in range(40):
        try:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

            try:
                load_more = page.query_selector('button[data-testid="pagination-next-btn"]')
                if load_more:
                    load_more.click()
                    print("Clicked next page")
                    time.sleep(7)
            except Exception:
                pass

            print(f"[INFO] Scroll {i+1} | Captured: {len(raw_responses)}")

            if len(raw_responses) >= 30:
                print("[INFO] Enough captured. Stopping.")
                break

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"\n[DONE] Total captured: {len(raw_responses)}")

    with open('expedia_raw_output.json', 'w', encoding='utf-8') as f:
        json.dump(raw_responses, f, indent=2, ensure_ascii=False)

    print("[SAVED] expedia_raw_output.json")