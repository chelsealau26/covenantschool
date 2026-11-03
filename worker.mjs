import { EMPLOYMENT_FORM_PATH, handleEmploymentForm } from "./employment-form.mjs";
import { hasEnded, isFundraiserPath, removeBanner, removeSitemapEntry, CLOSED_PAGE } from "./assets/fundraiser-lifecycle.mjs";
import { PREVIEW_CSS_VERSION } from "./assets/preview-version.mjs";
import { isLaunched, isPreview, isEftcPath, hideEftc, hideEftcSitemap, NOT_FOUND_PAGE, showLiveCredit, pickCreditVersion, redesignFor, isRedesignPath } from "./assets/eftc-launch.mjs";

const SUPPLY_LISTS_URL = "https://sis.factsmgt.com/accounts/Account/Login?ReturnUrl=%2Faccounts%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DfamilyPortalCode%26redirect_uri%3Dhttps%253A%252F%252Fsis.factsmgt.com%252Ffamily-portal%252Fsignin-oidc%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520familyPortalUserInfo%2520familyPortalUserConfig%2520offline_access%2520ftApi%26code_challenge%3DFiul3nN-aztKjGsczQavRZoVMLWZuxwkV5-Mm89Hp18%26code_challenge_method%3DS256%26response_mode%3Dform_post%26nonce%3D639080670995718110.ZDQyODQ0NmUtYWEzMS00OGU5LWFjN2ItMjRiMjk4MTg5MGI1NmE5ZTA1YjMtYjE1NS00NzkwLWJmMWEtMzM3MGJiMmU0N2Vk%26state%3DCfDJ8Lq1N5Cgm6tFnilnlNGlkcEod0V-wCTGxmw71V0Ux6x0cT40BqsZUZKtA5B8_yAnDYQLGNuzKV1VrllGwfqni1QHIX5H9utq8LNhcc9Bd6PPmf33REHdGqkwHkGnIjPPtu8c-N5Aj204dBYeJ7722Rl8O02GXGlKnnvw22icE117EKUsj_phuldyGYYj_aF3InNQp3JeAe3AvqpJhxxoFZoAXeZhT2gpzxB7pWyj3fQRlzibUr1VuvW7sFAURLWIJObzjAMCRZu0N0XH3bLQDx_tr3JWVOIeTYvOGN6FrJjauybBdnZ95Oala1No5BUYaSk942NFX6-0fyHIYavB6DG-eloKjrip56N7qi1B64iUcxT2DZFwrhvEn6Asl3xolG413HM-KPT_lELYIfIhub17SsYmOFUP_DtfNqOxlxyDgyPttuqttx6Q4VMDwvpmDEY1O_PX7flIna8V7CYc_HnqGZgqOK8KteLJFpn2P426-c4tXI8gbN_STDeK8cx-yA%26x-client-SKU%3DID_NET9_0%26x-client-ver%3D8.15.0.0";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === EMPLOYMENT_FORM_PATH) return handleEmploymentForm(request, env);
    // Redesign (preview only): the School Supplies page is retired; supply lists live in the Family Portal.
    if (isPreview(url) && /^\/school-supplies(\.html)?\/?$/i.test(path)) return Response.redirect(SUPPLY_LISTS_URL, 302);
    if (hasEnded() && isFundraiserPath(decodeURIComponent(path))) {
      return new Response(request.method === "HEAD" ? null : CLOSED_PAGE, {
        status: 410,
        headers: {"Content-Type":"text/html; charset=utf-8", "Cache-Control":"no-store", "X-Robots-Tag":"noindex"}
      });
    }
    // Federal Tax Credit page is hidden until its launch time, except via the preview link.
    const eftcHidden = !isLaunched() && !isPreview(url);
    if (eftcHidden && isEftcPath(decodeURIComponent(path))) {
      return new Response(request.method === "HEAD" ? null : NOT_FOUND_PAGE, {
        status: 404,
        headers: {"Content-Type":"text/html; charset=utf-8", "Cache-Control":"no-store", "X-Robots-Tag":"noindex"}
      });
    }
    // Redesigned pages: hidden unless on a preview link, where they replace the current page.
    const decoded = decodeURIComponent(path);
    if (isRedesignPath(decoded) && !isPreview(url)) {
      return new Response(request.method === "HEAD" ? null : NOT_FOUND_PAGE, {
        status: 404,
        headers: {"Content-Type":"text/html; charset=utf-8", "Cache-Control":"no-store", "X-Robots-Tag":"noindex"}
      });
    }
    const redesign = isPreview(url) ? redesignFor(decoded) : null;
    let response = await env.ASSETS.fetch(redesign ? new Request(new URL(redesign, url), request) : request);
    // A preview must never redirect the visitor to the internal /redesign/ path (it would drop the preview key).
    if (redesign && response.status >= 300 && response.status < 400 && response.headers.get("Location")) {
      response = await env.ASSETS.fetch(new Request(new URL(response.headers.get("Location"), url), request));
    }
    const contentType = response.headers.get("Content-Type") || "";
    if (contentType.includes("text/html") || path === "/sitemap.xml") {
      const headers = new Headers(response.headers);
      headers.set("Cache-Control", "no-store");
      headers.delete("Content-Length");
      headers.delete("Content-Encoding");
      headers.delete("ETag");
      if (!isLaunched() && isPreview(url)) headers.set("X-Robots-Tag", "noindex");
      let text = await response.text();
      if (hasEnded()) text = path === "/sitemap.xml" ? removeSitemapEntry(text) : removeBanner(text);
      if (eftcHidden) text = path === "/sitemap.xml" ? hideEftcSitemap(text) : hideEftc(text);
      if (path !== "/sitemap.xml") text = pickCreditVersion(text, showLiveCredit(url));
      if (redesign) headers.set("X-Robots-Tag", "noindex");
      // Refreshed design (not yet approved): its sitewide styles load only on preview links.
      if (isPreview(url) && path !== "/sitemap.xml") {
        text = text.replace("</head>", `<link rel="stylesheet" href="/assets/preview.css?v=${PREVIEW_CSS_VERSION}"></head>`);
        headers.set("X-Robots-Tag", "noindex");
      }
      return new Response(request.method === "HEAD" ? null : text, {status:response.status, headers});
    }
    return response;
  }
};
