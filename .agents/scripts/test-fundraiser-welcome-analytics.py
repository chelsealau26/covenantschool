"""Optional analytics must report outcomes once and never control popup behavior."""
import os
import shutil
from playwright.sync_api import sync_playwright, expect

BASE = "https://" + os.environ["REPLIT_DEV_DOMAIN"]
STUB = """window.events=[];
window.umami={track:(name,data)=>{events.push({name,data});return Promise.resolve();}};"""

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which("chromium"), args=["--no-sandbox"])
    for width, action in [(1200, "escape"), (390, "continue"), (1200, "close"), (390, "click"), (1200, "expire")]:
        ctx = browser.new_context(viewport={"width": width, "height": 900})
        page = ctx.new_page()
        page.clock.set_fixed_time("2026-10-12T15:00:00Z")
        page.add_init_script(STUB)
        page.goto(BASE)
        expect(page.locator("#fundraiser-welcome")).to_be_visible(timeout=15000)
        device = "mobile" if width < 768 else "desktop"
        events = [{"name": "fundraiser_popup_impression", "data": {"device": device}}]
        assert page.evaluate("events") == events
        if action == "escape":
            page.keyboard.press("Escape")
        elif action == "close":
            page.locator(".welcome-close").click()
        elif action == "continue":
            page.locator("[data-welcome-dismiss]").last.click()
        elif action == "click":
            # Cancel only the test's navigation; production link behavior is unchanged.
            page.evaluate("document.querySelector('.welcome-cta').addEventListener('click', e=>e.preventDefault())")
            page.locator(".welcome-cta").click()
        else:
            page.evaluate("document.dispatchEvent(new Event('fundraiser:ended'))")
        expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
        if action != "expire":
            data = {"device": device}
            if action != "click":
                data["method"] = action
            events.append({"name": "fundraiser_popup_click" if action == "click" else "fundraiser_popup_dismiss", "data": data})
        assert page.evaluate("events") == events
        page.goto(BASE + "/ways-to-give")
        page.goto(BASE + "/")
        page.wait_for_timeout(2600)
        expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
        assert page.evaluate("events") == []
        ctx.close()

    for tracker in [
        "delete window.umami",
        "window.umami={track(){throw Error('tracker failure')}}",
        "window.umami={track(){return Promise.reject(Error('tracker rejection'))}}",
    ]:
        ctx = browser.new_context()
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.clock.set_fixed_time("2026-10-12T15:00:00Z")
        page.add_init_script(tracker)
        page.goto(BASE)
        expect(page.locator("#fundraiser-welcome")).to_be_visible(timeout=15000)
        page.keyboard.press("Escape")
        expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
        page.wait_for_timeout(100)
        assert not errors, errors
        assert page.evaluate("Number(localStorage.getItem('covenant:fundraiser-welcome:2026:until')) > Date.now()")
        assert page.evaluate("document.body.style.position") != "fixed"
        ctx.close()
    browser.close()
print("PASS: impression, dismissal methods, CTA, device, deduplication, suppression, expiry and tracker failures")
