const { Builder, By, Key, until } = require("selenium-webdriver");

/**
 * Chrome浏览器启动配置
 * @returns
 */
async function getOptions() {
  const { Options } = require("selenium-webdriver/chrome");
  const chrome_options = new Options();
  // chrome_options.addArguments("--headless");
  chrome_options.addArguments("--disable-gpu");
  chrome_options.addArguments("--no-sandbox");
  chrome_options.addArguments("--disable-dev-shm-usage");

  return chrome_options;
}

(async function index() {
  const { useQueryTable } = require("./utils/useQueryTable");
  const { getConfig } = require("./utils/getConfig");
  const config = await getConfig();
  const res = await useQueryTable(config);
  console.log(res);
  // const chromeOptions = await getOptions();
  // const driver = await new Builder()
  //   .forBrowser("chrome")
  //   .setChromeOptions(chromeOptions)
  //   .build();
  // try {
  //   await driver.get("http://login.cuit.edu.cn/Login/xLogin/Login.asp");
  // } finally {
  //   setTimeout(() => driver.quit(), 5000);
  // }
})();
