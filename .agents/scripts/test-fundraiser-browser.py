#!/usr/bin/env python3
"""Real Chromium checks. Run against the existing `python server.py` workflow.

BASE_URL overrides the Replit preview URL. CHROMIUM_PATH overrides system Chromium.
Screenshots and Playwright traces (including failure state) go to /tmp/fundraiser-browser.
No page source, totals, or controller/observer implementations are mocked.
"""
import os
import re
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get("BASE_URL", "https://" + os.environ.get("REPLIT_DEV_DOMAIN", ""))
OUT = Path("/tmp/fundraiser-browser")
OUT.mkdir(exist_ok=True)


def settle(page):
    page.wait_for_timeout(350)


def overflow(page):
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), "Horizontal overflow"


def layout(page, width, contrast):
    overflow(page)
    # Check actual decoded image, proportional rendering, and clipping ancestors.
    izzy = page.locator(".recipe-hero-izzy")
    assert izzy.evaluate("""e => {
      const r=e.getBoundingClientRect();
      if(!e.complete || !e.naturalWidth || r.width<80 ||
         Math.abs(r.width/r.height-e.naturalWidth/e.naturalHeight)>.02) return false;
      if(r.left<0 || r.right>innerWidth) return false;
      for(let a=e.parentElement;a;a=a.parentElement){
        const s=getComputedStyle(a), b=a.getBoundingClientRect();
        if(/hidden|clip|scroll|auto/.test(s.overflowY) && (r.top<b.top-1 || r.bottom>b.bottom+1))return false;
      } return true;
    }"""), "Chef Izzy/hat is clipped, missing, or distorted"
    assert page.evaluate("""() => {
      const a=document.querySelector('.recipe-hero-izzy').getBoundingClientRect();
      const walker=document.createTreeWalker(document.querySelector('.recipe-hero-copy'),NodeFilter.SHOW_TEXT);
      let n;while(n=walker.nextNode()){
        if(!n.textContent.trim())continue;
        const range=document.createRange();range.selectNodeContents(n);
        for(const b of range.getClientRects()){
          if(a.right>b.left && a.left<b.right && a.bottom>b.top && a.top<b.bottom)return false;
        }
      }return true;
    }"""), "Mascot covers hero copy"
    assert page.locator("#faq").evaluate(
        "e=>getComputedStyle(e,'::before').backgroundImage==='none'"), "FAQ should not regain removed artwork"
    for selector, asset in [("#how-to-help", "whisk-navy"),
                            (".recipe-finish", "mixing-bowl-white")]:
        data = page.locator(selector).evaluate("""e=>{
          const s=getComputedStyle(e,'::before');
          return {display:s.display,image:s.backgroundImage,opacity:+s.opacity,w:parseFloat(s.width),h:parseFloat(s.height)};
        }""")
        if contrast or (width <= 900 and selector == ".recipe-finish"):
            assert data["display"] == "none", data
        else:
            assert asset in data["image"] and data["opacity"] > 0 and data["w"] > 40 and data["h"] > 40, data
            url = data["image"].split('"')[1]
            assert page.evaluate("""url=>new Promise(resolve=>{
              const image=new Image();image.onload=()=>resolve(image.naturalWidth>0);
              image.onerror=()=>resolve(false);image.src=url;
            })""", url), url
            assert page.locator(selector + " > .recipe-wrap").evaluate(
                "e=>+getComputedStyle(e).zIndex>0"), "Artwork must stay behind copy"
    if width <= 600:
        assert page.locator(".fundraiser-season").evaluate("""e=>{
          const r=document.createRange(); r.selectNodeContents(e.firstChild);
          const a=[...r.getClientRects()], span=e.querySelector('.season-dates');
          r.selectNodeContents(span); const b=[...r.getClientRects()];
          return a.length===1 && b.length===1 && b[0].top>a[0].top && b[0].right<=innerWidth;
        }"""), "Season dates must occupy exactly two lines"


def headers(page):
    page.evaluate("scrollTo(0,0)")
    settle(page)
    logos = page.locator('.header-widget .theme-logo img:visible')
    assert logos.count()
    assert logos.first.evaluate("e=>e.complete && e.naturalWidth>0")
    page.evaluate("scrollTo(0,700)")
    settle(page)
    fixed = page.locator(".fixed-header-wrapper")
    expect(fixed).to_have_class(re.compile(r"\bvisible\b"))
    assert fixed.evaluate("""e=>{
      const b=e.getBoundingClientRect(), img=e.querySelector('.theme-logo img'), r=img.getBoundingClientRect();
      return r.top>=b.top-1 && r.bottom<=b.bottom+1 && r.left>=0 && r.right<=innerWidth &&
        getComputedStyle(e).backgroundColor!=='rgba(0, 0, 0, 0)';
    }"""), "Scrolled header must contain the whole logo on an opaque bar"


def dialogs(page):
    buttons = page.locator(".calendar-entry-button")
    assert buttons.count() == 6
    dialog = page.locator("#calendar-event-dialog")
    for index in range(6):
        button = buttons.nth(index)
        for method in ("x", "escape", "backdrop"):
            button.evaluate("e=>e.scrollIntoView({block:'center',behavior:'instant'})")
            settle(page)
            before = page.evaluate("({y:scrollY,body:document.body.style.overflow,root:document.documentElement.style.overflow})")
            title = button.get_attribute("data-event-title")
            box = button.bounding_box()
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            expect(dialog).to_be_visible()
            expect(page.locator("#calendar-dialog-title")).to_have_text(title)
            assert dialog.evaluate("e=>e.matches(':modal')"), "Must be a native modal"
            expect(page.locator(".calendar-dialog-close")).to_be_focused()
            readable(page)
            assert dialog.evaluate("e=>e.scrollWidth<=e.clientWidth+1"), "Dialog content overflows"
            assert dialog.evaluate("""e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight}""")
            assert page.evaluate("getComputedStyle(document.body).overflow==='hidden'")
            modal_y = page.evaluate("scrollY")
            page.mouse.wheel(0, 400)
            settle(page)
            assert abs(page.evaluate("scrollY") - modal_y) <= 1, "Background scrolled under modal"
            # Exercise internal scrolling and retain an accessible close button.
            dialog.evaluate("e=>e.scrollTop=e.scrollHeight")
            close = page.locator(".calendar-dialog-close").bounding_box()
            assert close and close["y"] >= 0 and close["y"] + close["height"] <= page.viewport_size["height"]
            if method == "x":
                page.locator(".calendar-dialog-close").click()
            elif method == "escape":
                page.keyboard.press("Escape")
            else:
                box = dialog.bounding_box()
                assert box["x"] > 2, "No reachable backdrop"
                page.mouse.click(box["x"] / 2, box["y"] + box["height"] / 2)
            expect(dialog).not_to_be_visible()
            expect(button).to_be_focused()
            settle(page)
            after = page.evaluate("({y:scrollY,body:document.body.style.overflow,root:document.documentElement.style.overflow})")
            assert after == before, ("Scroll/overflow not restored", index, method, before, after)


def jug(page, reduced):
    assert page.evaluate("FundraiserSchoolGoal.getState().raised") is None
    expect(page.locator("[data-school-goal-total]")).to_be_hidden()
    assert page.locator("[data-measuring-glass]").get_attribute("role") == "img"
    assert "not a reported fundraising total" in page.locator("[data-measuring-glass]").get_attribute("aria-label")
    if reduced:
        assert page.evaluate("FundraiserSchoolGoal.getFill()") == .12
        return
    assert page.evaluate("FundraiserSchoolGoal.getFill()") == 0
    page.evaluate("""() => {
      const r=document.querySelector('.measuring-fill-trigger').getBoundingClientRect();
      scrollTo(0,scrollY+r.top-innerHeight-40);
    }""")
    settle(page)
    assert page.evaluate("FundraiserSchoolGoal.getFill()") == 0, "Fill starts before the bottom enters"
    page.evaluate("scrollBy(0,100)")
    page.wait_for_function("FundraiserSchoolGoal.getFill()>0")
    assert page.evaluate("FundraiserSchoolGoal.getFill()") < .12, "Expected gradual fill"
    page.wait_for_function("FundraiserSchoolGoal.getFill()===0.12", timeout=6000)
    expect(page.locator("[data-school-goal-total]")).to_be_hidden()


def readable(page):
    # Composite ancestor backgrounds and test actual computed text colors.
    failures = page.locator(".recipe-lede,.recipe-btn,.fundraiser-season,.calendar-entry-title,.calendar-entry-preview,.calendar-dialog-content p,.calendar-dialog-content li").evaluate_all("""es=>{
      function rgb(s){return (s.match(/[\\d.]+/g)||[]).map(Number)}
      function lum(c){return c.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0)}
      return es.filter(e=>e.getClientRects().length).flatMap(e=>{
        let bg=[255,255,255], chain=[];for(let a=e;a;a=a.parentElement)chain.unshift(a);
        for(const a of chain){const c=rgb(getComputedStyle(a).backgroundColor),alpha=c[3]??1;bg=bg.map((v,i)=>c[i]*alpha+v*(1-alpha))}
        const s=getComputedStyle(e), fg=rgb(s.color), l1=lum(fg),l2=lum(bg),ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
        const large=parseFloat(s.fontSize)>=24 || (parseFloat(s.fontSize)>=18.66 && +s.fontWeight>=700);
        return ratio+0.01<(large?3:4.5)?[{text:e.textContent.slice(0,60),ratio}]:[];
      });
    }""")
    assert not failures, ("Unreadable text contrast", failures)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or shutil.which("chromium"),
                                    args=["--no-sandbox"])
        for width, height in [(1440, 1000), (390, 844), (320, 740)]:
            for contrast in (False, True):
                name = f"{width}-{'contrast' if contrast else 'normal'}"
                context = browser.new_context(viewport={"width": width, "height": height})
                # Keep lightweight action traces; capture full-page screenshots
                # only after geometry and scroll measurements.
                context.tracing.start(screenshots=False, snapshots=False, sources=True)
                page = context.new_page()
                try:
                    page.goto(BASE + "/fall-fundraiser", wait_until="networkidle")
                    page.evaluate("document.fonts.ready")
                    if contrast:
                        page.locator("#a11y-btn").click()
                        page.locator("#a11y-btn-contrast").click()
                        page.locator("#a11y-btn").click()
                    jug(page, False)
                    headers(page)
                    layout(page, width, contrast)
                    readable(page)
                    dialogs(page)
                    page.evaluate("scrollTo(0,0)")
                    settle(page)
                    page.screenshot(path=str(OUT / (name + ".png")), full_page=True)
                    print("PASS", name, flush=True)
                except Exception:
                    page.screenshot(path=str(OUT / (name + "-failure.png")))
                    raise
                finally:
                    context.tracing.stop(path=str(OUT / (name + ".zip")))
                    context.close()
        for width in (1440, 390):
            page = browser.new_page(viewport={"width": width, "height": 844}, reduced_motion="reduce")
            page.goto(BASE + "/fall-fundraiser", wait_until="networkidle")
            jug(page, True)
            assert page.locator(".measuring-liquid").evaluate("e=>getComputedStyle(e,'::before').animationName") == "none"
            page.close()
            print("PASS reduced motion", width, flush=True)
        browser.close()


if __name__ == "__main__":
    main()
