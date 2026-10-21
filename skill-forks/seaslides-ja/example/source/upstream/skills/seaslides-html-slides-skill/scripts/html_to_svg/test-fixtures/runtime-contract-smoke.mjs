import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const [runtimeOwnedPath, themeOwnedPath] = process.argv.slice(2);
if (!runtimeOwnedPath || !themeOwnedPath) {
  throw new Error('Usage: node runtime-contract-smoke.mjs <runtime-owned.html> <theme-owned.html>');
}

const browser = await chromium.launch({ headless: true });
try {
  const reducedContext = await browser.newContext({ reducedMotion: 'reduce' });
  const runtimePage = await reducedContext.newPage();
  await runtimePage.goto(pathToFileURL(runtimeOwnedPath).href, { waitUntil: 'load' });
  await runtimePage.evaluate(() => window.SeaSlidesRuntime.ready);
  let state = await runtimePage.evaluate(() => ({
    lowPower: window.SeaSlidesRuntime.lowPower,
    legacy: window.__lowPowerMode,
    body: document.body.classList.contains('low-power')
      && document.body.classList.contains('seaslides-low-power'),
  }));
  if (!state.lowPower || !state.legacy || !state.body) {
    throw new Error(`Reduced-motion low-power state did not synchronize: ${JSON.stringify(state)}`);
  }

  await runtimePage.keyboard.press('Escape');
  state = await runtimePage.evaluate(() => {
    const overview = document.querySelector('[data-seaslides-overview="runtime"]');
    return { exists: !!overview, open: !!overview && !overview.hidden };
  });
  if (!state.exists || !state.open) throw new Error('Runtime-owned ESC overview did not open.');

  await runtimePage.keyboard.press('Escape');
  await runtimePage.keyboard.press('b');
  state = await runtimePage.evaluate(() => ({
    lowPower: window.SeaSlidesRuntime.lowPower,
    legacy: window.__lowPowerMode,
    classes: document.body.classList.contains('low-power')
      === window.SeaSlidesRuntime.lowPower
      && document.body.classList.contains('seaslides-low-power')
      === window.SeaSlidesRuntime.lowPower,
  }));
  if (state.lowPower !== state.legacy || !state.classes) {
    throw new Error(`Keyboard low-power state did not synchronize: ${JSON.stringify(state)}`);
  }
  const diagnostics = await runtimePage.evaluate(() => (
    window.SeaSlidesRuntime.settleForExport({ timeout: 5000 })
  ));
  if (diagnostics.frames !== 2 || diagnostics.images.broken.length) {
    throw new Error(`Export settlement failed: ${JSON.stringify(diagnostics)}`);
  }
  await reducedContext.close();

  const themeContext = await browser.newContext();
  const themePage = await themeContext.newPage();
  await themePage.goto(pathToFileURL(themeOwnedPath).href, { waitUntil: 'load' });
  await themePage.evaluate(() => window.SeaSlidesRuntime.ready);
  await themePage.keyboard.press('Escape');
  state = await themePage.evaluate(() => ({
    themeOpen: document.getElementById('overview').dataset.open === 'true',
    runtimeOverview: !!document.querySelector('[data-seaslides-overview="runtime"]'),
  }));
  if (!state.themeOpen || state.runtimeOverview) {
    throw new Error(`Theme-owned overview did not retain keyboard ownership: ${JSON.stringify(state)}`);
  }
  await themeContext.close();
} finally {
  await browser.close();
}

process.stdout.write('runtime contract smoke passed\n');
