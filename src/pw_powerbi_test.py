# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 20:18:00 2023

@author: Joseph Bedford
"""
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://app.powerbi.com/view?r=eyJrIjoiMjA1ODM0ZWEtMmMyMS00ZDVjLTg1MzctODFkZDVhZDVmZGNlIiwidCI6ImExMmNlNTRiLTNkM2QtNDM0Ni05NWVmLWZmMTNjYTVkZDQ3ZCJ9")
    expect(page).to_have_title(re.compile("Microsoft Power BI"))
    page.get_by_role("combobox", name="Commodity").locator("i").wait_for()
    page.get_by_role("combobox", name="Commodity").locator("i").click()
   #page.mouse.wheel(0, 1000) doesn't work
    page.get_by_role("option", name="London Wheat", exact=True).locator("div span").click()
    page.get_by_role("option", name="Paris Rapeseed").locator("div span").click()
    page.get_by_role("combobox", name="Delivery Month").locator("i").click()
    page.get_by_text("2023 05 May, Paris Rapeseed").click()
    page.get_by_role("menuitem", name="Show as a table").click()
    #need wait
    page.screenshot(path="example.png")
    #no idea how to get values from table
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
    
    