import asyncio
from playwright.async_api import async_playwright, expect

async def run() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)        # show the browser
        page = await browser.new_page()

        # 1️.  open the login page
        await page.goto("http://10.10.1.102:6001/")
        print("URL hit successfully")

        # 2️.  log in -----------------------------------------------------------
        await page.fill('input[name="username"]', "Tanay1")
        print("User name entered")
        await page.fill('//*[@id="password"]', "Cir@123")
        print("Password entered")
        await page.locator('//input[@value="Login"]').click()
        print("Login button clicked")

        # Wait until the page that contains the nav‑bar is fully ready
        # (network idle OR the Masters tab becomes present).
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("//ul[@class='navbar-nav mr-auto']//span[@class='masters' " "and normalize-space()='Masters']" )

        # 3️.  click the **Masters** tab ---------------------------------------
        await page.locator( "//ul[@class='navbar-nav mr-auto']//span[@class='masters' ""and normalize-space()='Masters']").click()
        print("Masters tab clicked")

        # Wait until the page that contains the nav‑bar is fully ready
        # (network idle OR the Masters tab becomes present).
        await page.wait_for_load_state("networkidle")
        #await page.wait_for_selector("//li[@class='active mb5']//a[normalize-space()='BOP']")

        #  4️. Click the *BOP* master
        await page.locator("//li[@class='null mb5']//a[normalize-space()='BOP']").click()
        print("BOP master clicked")

        # Wait until the page that contains the nav‑bar is fully ready
        # (network idle OR the Masters tab becomes present).
        await page.wait_for_load_state("networkidle")
        await page.wait_for_selector("//li[@class='active mb5']//a[normalize-space()='BOP']")

        # 5. Click the + icon to add BOP
        await page.locator("//div[@class='plus mr-0']").click()
        print("Add Clicked")

        # 6. Wait and assert that 'Add BOP (Domestic)' is visible on the screen
        locator = page.locator("text='Add BOP (Domestic)'")
        await expect(locator).to_be_visible()
        print("✅ Assertion Passed: 'Add BOP (Domestic)' is visible.")

        # 7. BOP Form
        await page.locator("//input[@id='bop_part_name_form_zero_based']").fill("Test Part 001")
        print("Entered text into BOP Part Name field")
        await page.locator("//input[@id='AddBOPDomestic_BOPCategory']").fill("BOP")

        # keep the browser open a little while so you can see the result
        await asyncio.sleep(5)
        await browser.close()

# kick it off
asyncio.run(run())
