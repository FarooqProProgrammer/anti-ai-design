#!/usr/bin/env node
/**
 * Serve plan HTML, accept annotations, write them back for Cursor.
 * Usage: node serve-open.js <path-to-html> [--port N] [--once]
 */
const http = require("http");
const fs = require("fs");
const path = require("path");
const { execFile, exec } = require("child_process");
const net = require("net");

const args = process.argv.slice(2);
const once = args.includes("--once");
const portIdx = args.indexOf("--port");
let port = portIdx >= 0 ? Number(args[portIdx + 1]) : 0;
const htmlArg = args.find((a, i) => {
  if (a.startsWith("--")) return false;
  if (portIdx >= 0 && i === portIdx + 1) return false;
  return true;
});
if (!htmlArg) {
  console.error("Usage: node serve-open.js <path-to-html> [--port N] [--once]");
  process.exit(1);
}

const repoRoot = process.cwd();
const htmlPath = path.resolve(repoRoot, htmlArg);
if (!fs.existsSync(htmlPath)) {
  console.error("HTML not found:", htmlPath);
  process.exit(1);
}

const serveRoot = path.dirname(htmlPath);
const fileName = path.basename(htmlPath);
const defaultSlug = path.basename(fileName, path.extname(fileName));

function getFreePort() {
  return new Promise((resolve, reject) => {
    const s = net.createServer();
    s.listen(0, "127.0.0.1", () => {
      const p = s.address().port;
      s.close(() => resolve(p));
    });
    s.on("error", reject);
  });
}

const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
};

function openChrome(url) {
  const platform = process.platform;
  if (platform === "win32") {
    const candidates = [
      process.env.PROGRAMFILES + "\\Google\\Chrome\\Application\\chrome.exe",
      process.env["PROGRAMFILES(X86)"] + "\\Google\\Chrome\\Application\\chrome.exe",
      process.env.LOCALAPPDATA + "\\Google\\Chrome\\Application\\chrome.exe",
    ];
    const chrome = candidates.find((c) => c && fs.existsSync(c));
    if (chrome) {
      execFile(chrome, [url], () => {});
      return;
    }
    exec(`start "" "${url}"`);
    return;
  }
  if (platform === "darwin") {
    execFile("open", ["-a", "Google Chrome", url], (err) => {
      if (err) execFile("open", [url]);
    });
    return;
  }
  execFile("google-chrome", [url], (err) => {
    if (err) {
      execFile("chromium-browser", [url], (err2) => {
        if (err2) execFile("xdg-open", [url]);
      });
    }
  });
}

function safeSlug(slug) {
  const s = String(slug || defaultSlug).replace(/[^a-zA-Z0-9._-]+/g, "-").replace(/^-+|-+$/g, "");
  return s || defaultSlug;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function writeFile(file, content) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, content, "utf8");
}

function annotationsToMarkdown(payload) {
  const lines = [
    `# Plan annotations - ${payload.slug}`,
    "",
    `Sent: ${payload.sentAt}`,
    payload.title ? `Title: ${payload.title}` : "",
    "",
    "Review these in Cursor before Implement. Kinds: comment | change | approve | block.",
    "",
  ].filter(Boolean);

  (payload.annotations || []).forEach((a, i) => {
    lines.push(`## ${i + 1}. [${a.kind}] ${a.section || "General"}`);
    if (a.quote) {
      lines.push("");
      lines.push(`> ${String(a.quote).replace(/\n/g, "\n> ")}`);
    }
    lines.push("");
    lines.push(a.note || "");
    lines.push("");
    lines.push(`_id: ${a.id || "n/a"} | ${a.createdAt || ""}_`);
    lines.push("");
  });

  return lines.join("\n");
}

function inboxMarkdown(payload) {
  const blocks = (payload.annotations || []).filter((a) => a.kind === "block").length;
  const changes = (payload.annotations || []).filter((a) => a.kind === "change").length;
  const approves = (payload.annotations || []).filter((a) => a.kind === "approve").length;
  return [
    `# Cursor inbox - plan feedback`,
    "",
    `- **Slug:** \`${payload.slug}\``,
    `- **Sent:** ${payload.sentAt}`,
    `- **Counts:** ${payload.annotations.length} total | ${changes} change | ${blocks} block | ${approves} approve`,
    "",
    "Open:",
    `- \`plans/html/${payload.slug}.annotations.md\``,
    `- \`.cursor/plans/html/${payload.slug}.annotations.md\``,
    "",
    "Agent: apply change/block items, regenerate html-plan if the plan text changes, then confirm in chat.",
    "",
  ].join("\n");
}

function writeAnnotationsBack(payload) {
  const slug = safeSlug(payload.slug);
  payload.slug = slug;
  const json = JSON.stringify(payload, null, 2);
  const md = annotationsToMarkdown(payload);
  const inbox = inboxMarkdown(payload);

  const targets = [
    path.join(repoRoot, "plans", "html", `${slug}.annotations.json`),
    path.join(repoRoot, "plans", "html", `${slug}.annotations.md`),
    path.join(repoRoot, ".cursor", "plans", "html", `${slug}.annotations.json`),
    path.join(repoRoot, ".cursor", "plans", "html", `${slug}.annotations.md`),
    path.join(repoRoot, ".cursor", "plans", "inbox", `${slug}-feedback.md`),
  ];

  writeFile(targets[0], json);
  writeFile(targets[1], md);
  writeFile(targets[2], json);
  writeFile(targets[3], md);
  writeFile(targets[4], inbox);

  const pluginRoot = path.join(
    process.env.USERPROFILE || process.env.HOME || "",
    ".cursor",
    "plugins",
    "local",
    "the-developer"
  );
  if (pluginRoot && fs.existsSync(path.join(pluginRoot, ".cursor-plugin"))) {
    writeFile(path.join(pluginRoot, "plans", "html", `${slug}.annotations.json`), json);
    writeFile(path.join(pluginRoot, "plans", "html", `${slug}.annotations.md`), md);
    writeFile(path.join(pluginRoot, ".cursor", "plans", "inbox", `${slug}-feedback.md`), inbox);
  }

  return {
    slug,
    inbox: `.cursor/plans/inbox/${slug}-feedback.md`,
    files: targets.map((t) => path.relative(repoRoot, t)),
  };
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function sendJson(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  });
  res.end(body);
}

(async () => {
  if (!port) port = await getFreePort();
  const url = `http://127.0.0.1:${port}/${fileName}`;

  const server = http.createServer(async (req, res) => {
    const method = req.method || "GET";
    let reqPath = decodeURIComponent((req.url || "/").split("?")[0]);

    if (method === "OPTIONS") {
      sendJson(res, 204, {});
      return;
    }

    if (method === "POST" && reqPath === "/api/annotations") {
      try {
        const raw = await readBody(req);
        const payload = JSON.parse(raw || "{}");
        if (!Array.isArray(payload.annotations) || !payload.annotations.length) {
          sendJson(res, 400, { error: "annotations array required" });
          return;
        }
        payload.sentAt = payload.sentAt || new Date().toISOString();
        const result = writeAnnotationsBack(payload);
        console.log("Annotations sent to Cursor:", result.inbox);
        sendJson(res, 200, { ok: true, ...result });
      } catch (err) {
        console.error(err);
        sendJson(res, 500, { error: err.message || String(err) });
      }
      return;
    }

    if (reqPath === "/") reqPath = "/" + fileName;
    const safe = path.normalize(reqPath).replace(/^(\.\.[/\\])+/, "");
    const file = path.join(serveRoot, safe);
    if (!file.startsWith(serveRoot) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }
    const ext = path.extname(file).toLowerCase();
    res.writeHead(200, { "Content-Type": mime[ext] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });

  server.listen(port, "127.0.0.1", () => {
    console.log("Serving", serveRoot);
    console.log("Annotations API: POST /api/annotations → .cursor/plans/inbox/");
    console.log("Opening", url);
    openChrome(url);
    if (once) {
      console.log("Warning: --once closes quickly; annotate/send-back needs a lasting server.");
      setTimeout(() => {
        server.close();
        process.exit(0);
      }, 3000);
    } else {
      console.log("Server running. Annotate in Chrome → Send to Cursor. Ctrl+C to stop.");
    }
  });
})();
