// Convierte cada .html de una carpeta a .pdf (A4) con Chromium/Playwright.
// Uso: node scripts/html_a_pdf.js informes/estaciones
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = path.resolve(process.argv[2]);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.html'))) {
    await page.goto('file://' + path.join(dir, f));
    await page.pdf({ path: path.join(dir, f.replace(/\.html$/, '.pdf')), format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('PDF:', f.replace(/\.html$/, '.pdf'));
  }
  await browser.close();
})();
