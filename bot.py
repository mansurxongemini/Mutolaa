import asyncio
from aiohttp import web
from playwright.async_api import async_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkyMDI5OTAzLCJpYXQiOjE3ODk0Mzc5MDMsImp0aSI6ImQxOGQ4NGRmNGZlMjRmMmI4YjA1MjQxYzY3NjgxYmNiIiwidXNlcl9pZCI6IjI2ODY2MTIiLCJkZXZpY2VfaWQiOiI1ZDc3Yjk3NS1kN2FhLTRhMTgtOWRjZi03M2FkYWZjZjg0ZTgifQ.zgiagZRTyYLvI2elcKjLq8qVZKQrUP--N4sDygPiyFw"
DEVICE_ID = "5d77b975-d7aa-4a18-9dcf-73adafcf84e8"
BOOK_URL = "https://mutolaa.com/uz/reader/orzular-ortidan-quvib"

async def handle_ping(request):
    return web.Response(text="Bot faol ishlamoqda!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("Veb-server 10000-portda ishga tushdi.", flush=True)

async def run_single_session():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--js-flags=--max-old-space-size=128",
                "--renderer-process-limit=1"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            timezone_id="Asia/Tashkent",
            locale="uz-UZ"
        )
        
        await context.add_cookies([
            {"name": "access_token", "value": ACCESS_TOKEN, "domain": ".mutolaa.com", "path": "/"},
            {"name": "mutolaa_device_id", "value": DEVICE_ID, "domain": ".mutolaa.com", "path": "/"}
        ])

        page = await context.new_page()
        
        # RAM tejash: faqat rasm va video to'xtatiladi, shrift va scriptlar faol qoladi
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media"] else route.continue_())

        print("Sahifa darhol ochilmoqda...", flush=True)
        await page.goto(BOOK_URL, wait_until="networkidle", timeout=60000)
        
        # Sahifa ochilishi bilanoq darhol o'qishni boshlash (harakat triggeri)
        print("Sahifa ochildi! Darhol o'qish harakatlari boshlandi...", flush=True)
        await page.mouse.click(200, 300)
        await page.keyboard.press("PageDown")
        await page.mouse.wheel(0, 150)

        # 25 daqiqa davomida uzluksiz o'qish sikli
        for _ in range(50):
            await asyncio.sleep(15)
            await page.keyboard.press("PageDown")
            await page.mouse.wheel(0, 120)
            await asyncio.sleep(15)
            await page.keyboard.press("ArrowDown")
            await page.mouse.wheel(0, -50)

        print("Sessiya yakunlandi. Xotirani tozalab qayta ulanadi...", flush=True)
        await browser.close()

async def run_mutolaa_bot():
    while True:
        try:
            await run_single_session()
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Kutilmagan xatolik: {e}, 5 soniyadan so'ng qayta ochiladi...", flush=True)
            await asyncio.sleep(5)

async def main():
    await start_web_server()
    await run_mutolaa_bot()

if __name__ == "__main__":
    asyncio.run(main())
