// Deterministic frame capture of an animated mockup via Playwright.
// usage: node mockups/capture.js <html> <durationSec> <fps> <framesDir>
// Chromium is resolved from $CHROME_PATH, else the pre-installed Playwright build.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function resolveChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  try {
    const dir = fs.readdirSync(base).filter(d => d.startsWith('chromium-') && !d.includes('headless')).sort().pop();
    if (dir) {
      const p = path.join(base, dir, 'chrome-linux', 'chrome');
      if (fs.existsSync(p)) return p;
    }
  } catch (e) {}
  return undefined; // fall back to Playwright's bundled browser if present
}

(async () => {
  const [html, durS, fpsS, dir] = process.argv.slice(2);
  const dur = parseFloat(durS), fps = parseInt(fpsS);
  fs.mkdirSync(dir, { recursive: true });
  const executablePath = resolveChrome();
  const browser = await chromium.launch({ executablePath, args: ['--no-sandbox', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  const N = Math.round(dur * fps);
  for (let i = 0; i < N; i++) {
    await page.evaluate((t) => window.renderAt(t), i / fps);
    await page.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.png` });
  }
  await browser.close();
  console.log('captured', N, 'frames ->', dir);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
