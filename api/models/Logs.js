'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  @Table({ timestamps: false })
  class Logs extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      // define association here
    }
  }
  Logs.init({
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true
    },
    time: DataTypes.DATE,
    bin_id: DataTypes.INTEGER,
    raw_picture: DataTypes.BLOB,
    filtered_picture: DataTypes.BLOB,
    estimated_amts_of_food: DataTypes.TEXT,
    change_in_weight: DataTypes.FLOAT
  }, {
    sequelize,
    modelName: 'Logs',
  });
  return Logs;
};
