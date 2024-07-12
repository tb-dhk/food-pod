import knex from 'knex';
import {SQL_PASSWORD} from "@env"

// Database configuration
const knexConfig = {
  client: 'mssql',
  connection: {
    server: 'food-pod.database.windows.net',
    user: 'foodpod',
    password: SQL_PASSWORD,
    database: 'food-pod',
    options: {
      encrypt: true, // For Azure SQL Database
      trustServerCertificate: false, // Change to true for local development
    },
  },
};

// Initialize Knex instance
const db = knex(knexConfig);

export default db;
