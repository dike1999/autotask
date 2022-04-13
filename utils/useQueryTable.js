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

module.exports = {
  useQueryTable,
};
