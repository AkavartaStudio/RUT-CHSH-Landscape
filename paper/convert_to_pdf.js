const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Load the HTML file
  await page.goto(`file://${path.resolve('PAPER1_COMPLETE_DRAFT.html')}`, {
    waitUntil: 'networkidle0'
  });

  // Wait for MathJax to render
  await page.waitForFunction(() => {
    return typeof MathJax !== 'undefined' && MathJax.typesetPromise !== undefined;
  }, { timeout: 10000 }).catch(() => console.log('MathJax not found, continuing...'));

  // Additional wait to ensure rendering is complete
  await page.evaluate(() => {
    if (typeof MathJax !== 'undefined' && MathJax.typesetPromise) {
      return MathJax.typesetPromise();
    }
  }).catch(() => {});

  // Wait a bit more to be sure
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Generate PDF
  await page.pdf({
    path: 'PAPER1_FINAL.pdf',
    format: 'A4',
    margin: {
      top: '1in',
      right: '1in',
      bottom: '1in',
      left: '1in'
    },
    printBackground: true
  });

  console.log('PDF generated successfully!');
  await browser.close();
})();
