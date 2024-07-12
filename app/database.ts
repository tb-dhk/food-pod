import { Sequelize } from 'sequelize-typescript';
import { SQL_PASSWORD } from '@env';

const sequelize = new Sequelize({
  dialect: 'mssql',
  host: 'food-pod.database.windows.net',
  username: 'foodpod',
  password: SQL_PASSWORD,
  database: 'food-pod',
});

export default sequelize;
