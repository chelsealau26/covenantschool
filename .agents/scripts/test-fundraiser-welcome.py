"""Homepage welcome regression checks against the existing preview workflow."""
import os
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = "https://" + os.environ["REPLIT_DEV_DOMAIN"]
OUT = Path("/tmp/fundraiser-welcome")
OUT.mkdir(exist_ok=True)
KEY = "covenant:fundraiser-welcome:2026:until"


def visit(browser, width=1200, height=900, init="", route="/", reduced=False):
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              reduced_motion="reduce" if reduced else "no-preference")
    page = ctx.new_page()
    page.clock.set_fixed_time("2026-10-12T15:00:00Z")
    if init:
        page.add_init_script(init)
    page.goto(BASE + route, wait_until="load")
    return ctx, page


with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which("chromium"), args=["--no-sandbox"])
    for width, height in [(1200, 900), (390, 844), (320, 640), (667, 375)]:
        ctx, page = visit(browser, width, height)
        dialog = page.locator("#fundraiser-welcome")
        expect(dialog).to_be_visible(timeout=12000)
        page.wait_for_timeout(350)  # Finish the intentional entrance before geometry checks.
        expect(page.locator(".welcome-close")).to_be_focused()
        assert dialog.evaluate("e=>e.matches(':modal')")
        assert dialog.evaluate("e=>e.scrollWidth<=e.clientWidth+1")
        assert dialog.evaluate("e=>{let r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1}")
        if width < 768:
            assert abs(dialog.bounding_box()["height"] - height) < 2
        expect(page.locator("[data-welcome-raised]")).to_have_text("$11,000")
        expect(page.locator("[data-welcome-goal]")).to_have_text("$50,000")
        expect(page.locator("[data-welcome-percent]")).to_have_text("22%")
        assert page.locator(".welcome-chef img").evaluate("e=>e.complete&&e.naturalWidth>0")
        page.keyboard.press("Shift+Tab")
        assert page.evaluate("document.querySelector('#fundraiser-welcome').contains(document.activeElement)")
        dialog.evaluate("e=>e.scrollTop=e.scrollHeight")
        close = page.locator(".welcome-close").bounding_box()
        assert close["y"] >= 0 and close["y"] + close["height"] <= height
        dialog.evaluate("e=>e.scrollTop=0")
        page.screenshot(path=str(OUT / f"welcome-{width}.png"))
        page.keyboard.press("Escape")
        expect(dialog).not_to_be_visible()
        assert page.evaluate("document.body.style.position") == ""
        assert page.evaluate(f"Number(localStorage.getItem('{KEY}'))-Date.now()") == 604800000
        page.reload(wait_until="load")
        page.wait_for_timeout(2400)
        expect(dialog).not_to_be_visible()
        ctx.close()
        print("PASS layout, focus, dismiss and suppression", width, height, flush=True)

    for route in ["/index", "/index.html"]:
        ctx, page = visit(browser, route=route)
        expect(page.locator("#fundraiser-welcome")).to_be_visible(timeout=12000)
        page.locator(".welcome-cta").click()
        page.wait_for_url("**/fall-fundraiser")
        page.go_back(wait_until="load")
        page.wait_for_timeout(2300)
        expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
        ctx.close()
    for init, route in [
        (f"localStorage.setItem('{KEY}',String(Date.now()+86400000))", "/"),
        ("", "/#main-content"),
        ("", "/ways-to-give"),
    ]:
        ctx, page = visit(browser, init=init, route=route)
        page.wait_for_timeout(2500)
        assert page.locator("#fundraiser-welcome[open]").count() == 0
        ctx.close()
    ctx, page = visit(browser)
    page.keyboard.press("Tab")
    page.wait_for_timeout(2400)
    expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
    ctx.close()
    for mode in ["blocked", "contrast", "expired"]:
        init = ("Storage.prototype.getItem=()=>{throw Error('blocked')};Storage.prototype.setItem=()=>{throw Error('blocked')};"
                if mode == "blocked" else "")
        ctx, page = visit(browser, init=init, reduced=True)
        dialog = page.locator("#fundraiser-welcome")
        if mode == "expired":
            page.clock.set_fixed_time("2026-11-09T21:00:00Z")
            page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
            assert dialog.count() == 0
        else:
            expect(dialog).to_be_visible(timeout=12000)
            assert dialog.evaluate("e=>getComputedStyle(e).animationName") == "none"
            if mode == "contrast":
                page.evaluate("document.body.classList.add('a11y-high-contrast')")
                assert dialog.evaluate("e=>getComputedStyle(e).backgroundColor") == "rgb(0, 0, 0)"
                page.screenshot(path=str(OUT / "contrast.png"))
                page.clock.set_fixed_time("2026-11-09T21:00:00Z")
                page.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
                assert dialog.count() == 0
            else:
                page.locator(".welcome-continue").click()
                expect(dialog).not_to_be_visible()
            assert page.evaluate("document.body.style.position") == ""
        ctx.close()
    ctx, page = visit(browser, init=f"localStorage.setItem('{KEY}',String(Date.now()-1))")
    expect(page.locator("#fundraiser-welcome")).to_be_visible(timeout=12000)
    page.locator(".welcome-close").click()
    expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
    ctx.close()
    ctx, page = visit(browser)
    page.evaluate("document.querySelector('#a11y-panel').classList.add('open')")
    page.wait_for_timeout(2500)
    expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
    ctx.close()
    ctx = browser.new_context(java_script_enabled=False)
    page = ctx.new_page()
    page.goto(BASE, wait_until="load")
    expect(page.locator("#fundraiser-welcome")).not_to_be_visible()
    expect(page.locator(".fundraiser-announcement-cta")).to_be_visible()
    ctx.close()
    browser.close()
print("PASS routes, CTA/back, keyboard interruption, storage errors, reduced motion, contrast and open-tab expiry")
