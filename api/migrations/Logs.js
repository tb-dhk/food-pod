'use strict';

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Logs', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER,
      },
      time: {
        type: Sequelize.DATE,
        allowNull: true,
      },
      bin_id: {
        type: Sequelize.INTEGER,
        allowNull: true,
      },
      raw_picture: {
        type: Sequelize.BLOB('long'),
        allowNull: true,
      },
      filtered_picture: {
        type: Sequelize.BLOB('long'),
        allowNull: true,
      },
      estimated_amts_of_food: {
        type: Sequelize.JSON,
        allowNull: true,
      },
      change_in_weight: {
        type: Sequelize.FLOAT,
        allowNull: true,
      },
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable('Logs');
  },
};
