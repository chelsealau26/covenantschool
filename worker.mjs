import { EMPLOYMENT_FORM_PATH, handleEmploymentForm } from "./employment-form.mjs";
import { hasEnded, isFundraiserPath, removeBanner, removeSitemapEntry, CLOSED_PAGE } from "./assets/fundraiser-lifecycle.mjs";
import { isLaunched, isPreview, isEftcPath, hideEftc, hideEftcSitemap, NOT_FOUND_PAGE, showLiveCredit, pickCreditVersion, redesignFor, isRedesignPath } from "./assets/eftc-launch.mjs";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    if (path === EMPLOYMENT_FORM_PATH) return handleEmploymentForm(request, env);
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
      return new Response(request.method === "HEAD" ? null : text, {status:response.status, headers});
    }
    return response;
  }
};
