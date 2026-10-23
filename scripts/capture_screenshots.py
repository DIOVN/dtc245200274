import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="msedge", headless=True)
        except Exception:
            try:
                browser = await p.chromium.launch(headless=True)
            except Exception as e:
                print("Failed to launch browser:", e)
                return

        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        
        # 1. Frontend Guest
        page = await context.new_page()
        print("Navigating to http://localhost:3001/...")
        try:
            await page.goto("http://localhost:3001/", wait_until="networkidle", timeout=15000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path="docs/images/hinh4_giaodien_datphong.png")
            print("Captured hinh4_giaodien_datphong.png")
        except Exception as e:
            print("Error capturing guest frontend:", e)

        # 2. Frontend Admin Login & Dashboard
        try:
            await page.evaluate("""() => {
                localStorage.setItem('sun_hotel_admin_token', 'mock_or_real_token');
                localStorage.setItem('sun_hotel_admin_user', JSON.stringify({
                    username: 'admin',
                    fullName: 'Phùng Thiên Trường - Quản Trị Viên',
                    role: 'admin'
                }));
            }""")
            await page.goto("http://localhost:3001/?view=admin", wait_until="networkidle", timeout=15000)
            await page.wait_for_timeout(2000)
            await page.screenshot(path="docs/images/hinh5_admin_dashboard.png")
            print("Captured hinh5_admin_dashboard.png")
        except Exception as e:
            print("Error capturing admin dashboard:", e)

        # 3. Prometheus Targets
        try:
            page2 = await context.new_page()
            await page2.goto("http://localhost:9090/targets", wait_until="networkidle", timeout=15000)
            await page2.wait_for_timeout(2000)
            await page2.screenshot(path="docs/images/hinh7_prometheus_targets.png")
            print("Captured hinh7_prometheus_targets.png")
            await page2.close()
        except Exception as e:
            print("Error capturing prometheus:", e)

        # 4. Grafana Dashboard / Login
        try:
            page3 = await context.new_page()
            await page3.goto("http://localhost:3000/login", wait_until="networkidle", timeout=15000)
            await page3.wait_for_timeout(1000)
            # Login to Grafana
            try:
                await page3.fill('input[name="user"]', 'admin')
                await page3.fill('input[name="password"]', 'RSCZrbHMtKiC')
                await page3.click('button[type="submit"]')
                await page3.wait_for_timeout(3000)
            except Exception as e:
                print("Grafana login form note:", e)
            await page3.screenshot(path="docs/images/hinh6_grafana_dashboard.png")
            print("Captured hinh6_grafana_dashboard.png")
            await page3.close()
        except Exception as e:
            print("Error capturing grafana:", e)

        await browser.close()
        print("Done capturing screenshots!")

if __name__ == "__main__":
    asyncio.run(capture())
