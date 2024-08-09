'use strict';

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Bin', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER,
      },
      name: {
        type: Sequelize.TEXT,
        allowNull: true,
      },
      assignee: {
        type: Sequelize.TEXT,
        allowNull: true,
      }
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable('Bin');
  },
};
