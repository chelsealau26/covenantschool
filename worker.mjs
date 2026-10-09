import { hasEnded, isFundraiserPath, removeBanner, removeSitemapEntry, CLOSED_PAGE } from "./assets/fundraiser-lifecycle.mjs";

export default {
  async fetch(request, env) {
    const path = new URL(request.url).pathname;
    if (hasEnded() && isFundraiserPath(decodeURIComponent(path))) {
      return new Response(request.method === "HEAD" ? null : CLOSED_PAGE, {
        status: 410,
        headers: {"Content-Type":"text/html; charset=utf-8", "Cache-Control":"no-store", "X-Robots-Tag":"noindex"}
      });
    }
    const response = await env.ASSETS.fetch(request);
    const contentType = response.headers.get("Content-Type") || "";
    if (contentType.includes("text/html") || path === "/sitemap.xml") {
      const headers = new Headers(response.headers);
      headers.set("Cache-Control", "no-store");
      headers.delete("Content-Length");
      headers.delete("Content-Encoding");
      headers.delete("ETag");
      let text = await response.text();
      if (hasEnded()) text = path === "/sitemap.xml" ? removeSitemapEntry(text) : removeBanner(text);
      return new Response(request.method === "HEAD" ? null : text, {status:response.status, headers});
    }
    return response;
  }
};
