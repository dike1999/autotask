const { Builder, By, Key, until } = require("selenium-webdriver");
const {
  useQueryTable,
  getChromeOptions,
  getConfig,
  sendEmail,
} = require("./utils");

(async function index() {
  sendEmail("1138832931@qq.com", {
    name: "狄克",
    content: "打卡成功",
  });
  const config = await getConfig();
  const students = await useQueryTable(config);
  const chrome_options = getChromeOptions();
  const driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(chrome_options)
    .build();
  // 开始执行任务
  try {
    await driver.get("http://login.cuit.edu.cn/Login/xLogin/Login.asp");
  } finally {
    setTimeout(() => driver.quit(), 2000);
  }
})();
