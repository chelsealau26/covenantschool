import assert from "node:assert/strict";
import fs from "node:fs";
import worker from "../../worker.mjs";
import {END_TIME, hasEnded, removeBanner} from "../../assets/fundraiser-lifecycle.mjs";
const end = Date.parse(END_TIME);
assert.equal(hasEnded(end - 1), false);
assert.equal(hasEnded(end), true);
assert.equal(hasEnded(end + 1), true);
for (const file of fs.readdirSync("pages").filter(f => f.endsWith(".html"))) {
  const html = fs.readFileSync("pages/" + file, "utf8");
  assert.equal(html.includes('<aside class="fundraiser-announcement"'), file !== "fall-fundraiser.html", "Banner placement: " + file);
  assert.equal(removeBanner(html).includes('<aside class="fundraiser-announcement"'), false, file);
  assert.equal((html.match(/class="fundraiser-footer-link"/g) || []).length, 1, file);
  assert.ok(!removeBanner(html).includes('class="fundraiser-footer-link"'), file);
  const expectedFooter = html.match(/<footer[\s\S]*?<\/footer>/)?.[0].replace(/<p class="fundraiser-footer-link"[^>]*>[\s\S]*?<\/p>/g, "");
  assert.equal(removeBanner(html).match(/<footer[\s\S]*?<\/footer>/)?.[0], expectedFooter);
}
const realNow = Date.now;
const html = fs.readFileSync("pages/index.html", "utf8");
const env = {ASSETS: {fetch: async request => new Response(
  request.url.endsWith("/sitemap.xml") ? fs.readFileSync("pages/sitemap.xml","utf8") : html,
  {headers: {"Content-Type": request.url.endsWith("/sitemap.xml") ? "application/xml" : "text/html"}}
)}};
try {
  Date.now = () => end - 1;
  assert.equal((await worker.fetch(new Request("https://example.com/fall-fundraiser"),env)).status,200);
  Date.now = () => end;
  for (const path of ["/fall-fundraiser", "/fall-fundraiser.html", "/fall-fundraiser/?test=1"]) {
    const response = await worker.fetch(new Request("https://example.com"+path),env);
    assert.equal(response.status,410);
    assert.equal(response.headers.get("X-Robots-Tag"),"noindex");
    assert.ok(!(await response.text()).includes("Recipe for Success"));
  }
  const home = await worker.fetch(new Request("https://example.com/"),env);
  assert.equal(home.status,200);
  assert.ok(!(await home.text()).includes('<aside class="fundraiser-announcement"'));
  const sitemap = await worker.fetch(new Request("https://example.com/sitemap.xml"),env);
  assert.ok(!(await sitemap.text()).includes("/fall-fundraiser"));
} finally { Date.now = realNow; }
console.log("PASS: exact cutoff, banner on other pages only, page aliases/410, sitemap removal and intact footers.");
