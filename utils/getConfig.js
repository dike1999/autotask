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

module.exports = {
  getConfig,
};
