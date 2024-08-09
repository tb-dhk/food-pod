require('dotenv').config();
const { Sequelize } = require('sequelize');

// Ensure all required environment variables are defined
const {
  DB_USERNAME,
  DB_PASSWORD,
  DB_DATABASE,
  DB_HOST,
  DB_DIALECT
} = process.env;

if (!DB_USERNAME || !DB_PASSWORD || !DB_DATABASE || !DB_HOST || !DB_DIALECT) {
  throw new Error('Missing required environment variables');
}

// Create a Sequelize instance with individual settings
const sequelize = new Sequelize(DB_DATABASE, DB_USERNAME, DB_PASSWORD, {
  host: DB_HOST,
  dialect: DB_DIALECT, // This should be 'mssql' based on your env file
  logging: false, // Disable logging if not needed
});

module.exports = { sequelize };

