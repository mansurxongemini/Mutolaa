import asyncio
from playwright.async_api import async_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkxOTE3MzU5LCJpYXQiOjE3ODkzMjUzNTksImp0aSI6IjBiZTc0MTQ1MTMxMTQwMTdhZGEwNDM1NzNlMjJmZDViIiwidXNlcl9pZCI6IjI2ODY2MTIiLCJkZXZpY2VfaWQiOiI1NTEyMTU2OC0wMGNjLTQwYmQtOTI0Zi0yMzM5YjhjNzIyNTQifQ.-9-1-9AknpXaa6jOs0wKmR-pDZaeaHclcWf8LDYa9Tw"

async def main():
    async with async_playwright() as p:
        # Brauzerni xotirani tejash parametrlari bilan ishga tushiramiz
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        )
        
        await context.add_cookies([
            {"name": "access_token", "value": ACCESS_TOKEN, "domain": ".mutolaa.com", "path": "/"},
            {"name": "mutolaa_device_id", "value": "55121568-00cc-40bd-924f-2339b8c72254", "domain": ".mutolaa.com", "path": "/"}
        ])

        page = await context.new_page()
        print("Kitob sahifasi ochilmoqda...")
        await page.goto("https://mutolaa.com/uz/reader/ulug-bek-xazinasi", wait_until="networkidle")
        print("Sahifa ochildi. 24/7 faollik boshlandi...")

        # Cheksiz sikl (24/7 to'xtovsiz qimirlatib turadi)
        while True:
            try:
                await page.mouse.wheel(0, 150)
                await asyncio.sleep(20)
                await page.mouse.wheel(0, -150)
                await asyncio.sleep(20)
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")
                await page.reload(wait_until="networkidle")
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
