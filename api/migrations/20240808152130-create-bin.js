'use strict';

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Bins', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      name: {
        type: Sequelize.STRING, // Use STRING if the text is not expected to be very long
        allowNull: false // Consider adding this if 'name' should not be null
      },
      assignee: {
        type: Sequelize.STRING, // Use STRING if the text is not expected to be very long
        allowNull: true // Can be null if the field is optional
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.NOW // Set default value to now for auto-populating the timestamp
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE,
        defaultValue: Sequelize.NOW // Set default value to now for auto-populating the timestamp
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Bins');
  }
};

