'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Logs', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      id: {
        type: Sequelize.INTEGER
      },
      timestamp: {
        type: Sequelize.TEXT
      },
      bin_id: {
        type: Sequelize.INTEGER
      },
      raw_picture: {
        type: Sequelize.BLOB
      },
      filtered_picture: {
        type: Sequelize.BLOB
      },
      estimated_amts_of_food: {
        type: Sequelize.TEXT
      },
      change_in_weight: {
        type: Sequelize.FLOAT
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Logs');
  }
};
