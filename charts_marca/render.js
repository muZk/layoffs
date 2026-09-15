const { chromium } = require('playwright');

const PORT = process.env.PORT || 8899;
const jobs = [
  { url: `http://localhost:${PORT}/mapa.html`,    out: 'mapa.png' },
  { url: `http://localhost:${PORT}/embudo.html`,  out: 'embudo.png' },
  { url: `http://localhost:${PORT}/tornado.html`, out: 'tornado.png' },
];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  for (const j of jobs) {
    await page.goto(j.url, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(350);
    const card = await page.locator('.card');
    await card.screenshot({ path: j.out });
    console.log('ok', j.out);
  }
  await browser.close();
})();
