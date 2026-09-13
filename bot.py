import asyncio
from playwright.async_api import async_playwright

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkxOTE3MzU5LCJpYXQiOjE3ODkzMjUzNTksImp0aSI6IjBiZTc0MTQ1MTMxMTQwMTdhZGEwNDM1NzNlMjJmZDViIiwidXNlcl9pZCI6IjI2ODY2MTIiLCJkZXZpY2VfaWQiOiI1NTEyMTU2OC0wMGNjLTQwYmQtOTI0Zi0yMzM5YjhjNzIyNTQifQ.-9-1-9AknpXaa6jOs0wKmR-pDZaeaHclcWf8LDYa9Tw"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        )
        
        # Brauzerga hisob tokeningizni yuklaymiz
        await context.add_cookies([
            {"name": "access_token", "value": ACCESS_TOKEN, "domain": ".mutolaa.com", "path": "/"},
            {"name": "mutolaa_device_id", "value": "55121568-00cc-40bd-924f-2339b8c72254", "domain": ".mutolaa.com", "path": "/"}
        ])

        page = await context.new_page()
        print("Kitob sahifasi ochilmoqda...")
        await page.goto("https://mutolaa.com/uz/reader/ulug-bek-xazinasi", wait_until="networkidle")
        
        print("Sahifa faol ushlab turilmoqda (WebSocket va Ping ishlayapti)...")
        # 5 soat davomida har 30 soniyada sahifani biroz qimirlatib turadi
        for _ in range(600):
            await page.mouse.wheel(0, 100)
            await asyncio.sleep(15)
            await page.mouse.wheel(0, -100)
            await asyncio.sleep(15)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
