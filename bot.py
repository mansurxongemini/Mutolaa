import asyncio
from aiohttp import web
from playwright.async_api import async_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkxOTE3MzU5LCJpYXQiOjE3ODkzMjUzNTksImp0aSI6IjBiZTc0MTQ1MTMxMTQwMTdhZGEwNDM1NzNlMjJmZDViIiwidXNlcl9pZCI6IjI2ODY2MTIiLCJkZXZpY2VfaWQiOiI1NTEyMTU2OC0wMGNjLTQwYmQtOTI0Zi0yMzM5YjhjNzIyNTQifQ.-9-1-9AknpXaa6jOs0wKmR-pDZaeaHclcWf8LDYa9Tw"

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
    """Har 25 daqiqada brauzerni noldan ochib-yopib xotirani (RAM) tozalaydi"""
    async with async_playwright() as p:
        # Xotirani tejovchi parametrlar
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
            timezone_id="Asia/Tashkent"
        )
        
        await context.add_cookies([
            {"name": "access_token", "value": ACCESS_TOKEN, "domain": ".mutolaa.com", "path": "/"},
            {"name": "mutolaa_device_id", "value": "55121568-00cc-40bd-924f-2339b8c72254", "domain": ".mutolaa.com", "path": "/"}
        ])

        page = await context.new_page()
        
        # Keraksiz rasm va shriftlarni yuklamaslik orqali RAM tejash
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "media", "font"] else route.continue_())

        print("Yangi sessiya ochilmoqda...", flush=True)
        await page.goto("https://mutolaa.com/uz/reader/ulug-bek-xazinasi", wait_until="domcontentloaded")
        print("Sahifa faol. O'qish boshlandi...", flush=True)

        # 25 daqiqa (50 ta 30 soniyalik sikl) ishlab, keyin brauzerni yopadi
        for _ in range(50):
            await page.mouse.wheel(0, 100)
            await asyncio.sleep(15)
            await page.mouse.wheel(0, -100)
            await asyncio.sleep(15)

        print("25 daqiqa o'tdi. RAM'ni tozalash uchun brauzer yopilmoqda...", flush=True)
        await browser.close()

async def run_mutolaa_bot():
    while True:
        try:
            await run_single_session()
            await asyncio.sleep(5)  # 5 soniya xotira bo'shashini kutadi
        except Exception as e:
            print(f"Sessiyada xatolik: {e}, 10 soniyadan so'ng qayta boshlanadi...", flush=True)
            await asyncio.sleep(10)

async def main():
    await start_web_server()
    await run_mutolaa_bot()

if __name__ == "__main__":
    asyncio.run(main())
