/**
 * Chrome浏览器启动配置
 * @returns
 */
async function getChromeOptions() {
  const { Options } = require("selenium-webdriver/chrome");
  const chrome_options = new Options();
  // chrome_options.addArguments("--headless");
  chrome_options.addArguments("--disable-gpu");
  chrome_options.addArguments("--no-sandbox");
  chrome_options.addArguments("--disable-dev-shm-usage");

  return chrome_options;
}

/**
 * 获取env环境变量
 * @returns
 */
async function getConfig() {
  const { config } = require("dotenv");
  config();
  return {
    host: process.env.HOST,
    port: process.env.PORT,
    database: process.env.DATABASE,
    table: process.env.TABLE,
    username: process.env.USERNAME,
    password: process.env.PASSWORD,
  };
}

/**
 * 查表
 * @param {*} config
 * @returns
 */
async function useQueryTable(config) {
  const { Sequelize } = require("sequelize");
  const db = new Sequelize({
    dialect: "mysql",
    host: config.host,
    port: config.port,
    database: config.database,
    username: config.username,
    password: config.password,
    pool: {
      max: 5,
      idle: 30000,
      acquire: 60000,
    },
  });
  const [results] = await db.query(`SELECT * FROM ${config.table}`, {});
  await db.close();

  return results;
}

/**
 * 发送邮件
 * @param {*} email
 * @param {*} content
 */
async function sendEmail(email, content) {
  const nodemailer = require("nodemailer");
  const serveremail = {
    user: "dike1138832931@126.com",
    password: "GVVEZOBIJCRVNQWO",
    service: "smtp.126.com",
  };

  nodemailer.createTestAccount((err, account) => {
    const transporter = nodemailer.createTransport({
      host: serveremail.service, // 邮件服务地址 可在126后台查看
      port: 465, // port
      secure: true, // true for 465, false for other ports
      auth: {
        user: serveremail.user, // generated ethereal user
        pass: serveremail.password, // generated ethereal password
      },
    });

    // setup email data with unicode symbols
    const mailOptions = {
      from: serveremail.user, // sender address
      to: email, // list of receivers 接收者地址
      subject: "Node邮件服务: 疫情打卡", // Subject line                      // 邮件标题
      text: "this is nodemailer text", // plain text body
      html: `
        <div>
          <h4>${content.name}</h4>
          <p>${content.content}</p>
        </div>
      `, // html body   //邮件内容
    };

    transporter.sendMail(mailOptions, (error, info) => {
      //发送邮件
      if (error) {
        return console.log(error);
      }
      console.log("Message sent: %s", info.messageId); //成功回调
      console.log("Preview URL: %s", nodemailer.getTestMessageUrl(info));
    });
  });
}

module.exports = {
  getChromeOptions,
  getConfig,
  useQueryTable,
  sendEmail,
};
