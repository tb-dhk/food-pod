'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class BinStatus extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  BinStatus.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true
    },
    bin_id: DataTypes.INTEGER,
    status: DataTypes.TEXT,
    timestamp: DataTypes.TEXT
  }, {
    sequelize,
    modelName: 'BinStatus',
  });
  return BinStatus;
};
