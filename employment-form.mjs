// Handles job applications from the Employment Opportunities page.
// Checks the Turnstile spam challenge, then emails the application
// (with the résumé attached) through Resend.
//
// Required Worker secrets (Cloudflare → Workers → covenantschool → Settings → Variables and Secrets):
//   RESEND_API_KEY        – Resend API key with sending access for covenantschool.com
//   TURNSTILE_SECRET_KEY  – secret key of the "Employment form" Turnstile widget

export const EMPLOYMENT_FORM_PATH = "/api/employment-application";

const RECIPIENT = "fboren@covenantschool.com";
const SENDER = "Covenant School Website <website@covenantschool.com>";
const FALLBACK = "Please email us directly at fboren@covenantschool.com.";
const MAX_RESUME_BYTES = 5 * 1024 * 1024;
const ALLOWED_EXTENSIONS = ["pdf", "doc", "docx", "rtf", "txt", "odt"];
const POSITIONS = ["Preschool Teacher (K3/K4)", "Kindergarten Teacher (K5)", "Elementary Teacher (1st–5th)", "Middle School Teacher (6th–8th)", "Specials Teacher", "Substitute Teacher", "Aftercare Staff", "Coach", "Office / Administrative Staff", "Other"];
const LIMITS = { full_name: 120, email: 200, phone: 40, position: 150, comments: 5000 };

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function toBase64(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 0x8000) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  }
  return btoa(binary);
}

async function passedTurnstile(token, ip, secret) {
  if (!token) return false;
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  const outcome = await res.json().catch(() => ({}));
  return outcome.success === true;
}

export async function handleEmploymentForm(request, env) {
  if (request.method !== "POST") {
    return json({ success: false, error: "Method not allowed." }, 405);
  }
  if (!env.RESEND_API_KEY || !env.TURNSTILE_SECRET_KEY) {
    console.error("Employment form: RESEND_API_KEY or TURNSTILE_SECRET_KEY is not set.");
    return json({ success: false, error: `The application form isn't available right now. ${FALLBACK}` }, 503);
  }

  let form;
  try {
    form = await request.formData();
  } catch {
    return json({ success: false, error: "We couldn't read the form. Please try again." }, 400);
  }

  // Hidden field real people never fill in; bots usually do.
  if ((form.get("website") || "").toString().trim()) {
    return json({ success: true });
  }

  const ip = request.headers.get("CF-Connecting-IP");
  if (!(await passedTurnstile(form.get("cf-turnstile-response"), ip, env.TURNSTILE_SECRET_KEY))) {
    return json({ success: false, error: "Please complete the verification check and try again." }, 400);
  }

  const fields = {};
  for (const [key, max] of Object.entries(LIMITS)) {
    fields[key] = (form.get(key) || "").toString().trim().slice(0, max);
  }
  if (Object.values(fields).some((v) => !v)) {
    return json({ success: false, error: "Please fill in all required fields." }, 400);
  }
  if (!POSITIONS.includes(fields.position)) {
    return json({ success: false, error: "Please choose a position from the list." }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email)) {
    return json({ success: false, error: "Please enter a valid email address." }, 400);
  }

  const attachments = [];
  const resume = form.get("resume");
  if (resume && typeof resume === "object" && resume.size > 0) {
    const ext = (resume.name.split(".").pop() || "").toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      return json({ success: false, error: "Please attach your résumé as a PDF or Word document." }, 400);
    }
    if (resume.size > MAX_RESUME_BYTES) {
      return json({ success: false, error: "Your résumé file is too large. Please keep it under 5 MB." }, 400);
    }
    const filename = resume.name.replace(/[^\w.\- ]+/g, "_").slice(0, 100) || `resume.${ext}`;
    attachments.push({ filename, content: toBase64(await resume.arrayBuffer()) });
  }

  const { full_name, email, phone, position, comments } = fields;
  const rows = [["Name", full_name], ["Email", email], ["Phone", phone], ["Position", position]]
    .map(([label, value]) => `<tr><td style="padding:4px 16px 4px 0;font-weight:bold;vertical-align:top">${label}</td><td style="padding:4px 0">${escapeHtml(value)}</td></tr>`)
    .join("");
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;color:#131c24">
<p>New employment application from the Covenant Christian School website.</p>
<table style="border-collapse:collapse">${rows}</table>
<p style="margin-top:20px;font-weight:bold">Comments / qualifications</p>
<p style="white-space:pre-wrap">${escapeHtml(comments)}</p>
<p style="color:#6c6c6c">${attachments.length ? `Résumé attached: ${escapeHtml(attachments[0].filename)}` : "No résumé was attached."} Reply to this email to respond to the applicant.</p>
</div>`;
  const text = `New employment application from the Covenant Christian School website.

Name: ${full_name}
Email: ${email}
Phone: ${phone}
Position: ${position}

Comments / qualifications:
${comments}

${attachments.length ? `Résumé attached: ${attachments[0].filename}` : "No résumé was attached."}`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: SENDER,
      to: [RECIPIENT],
      reply_to: email,
      subject: `Employment Application: ${full_name} — ${position}`.replace(/[\r\n]+/g, " "),
      html,
      text,
      attachments,
    }),
  });

  if (!res.ok) {
    console.error("Employment form: Resend error", res.status, await res.text().catch(() => ""));
    return json({ success: false, error: `We couldn't send your application right now. ${FALLBACK}` }, 502);
  }
  return json({ success: true });
}
