const express = require('express');
const { Binstatus, Bins, Food, Logs } = require('./models'); // Import all models

const app = express();
app.use(express.json());

// Sample GET endpoint to fetch all binstatus
app.get('/api/binstatus', async (req, res) => {
  try {
    const binstatus = await Binstatus.findAll();
    res.json(binstatus);
  } catch (err) {
    res.status(500).json({ error: err });
  }
});

// Endpoint to fetch all bins
app.get('/api/bins', async (req, res) => {
  try {
    const bins = await Bins.findAll();
    res.json(bins);
  } catch (err) {
    res.status(500).json({ error: err });
  }
});

// Endpoint to fetch all food items
app.get('/api/food', async (req, res) => {
  try {
    const foodItems = await Food.findAll();
    res.json(foodItems);
  } catch (err) {
    res.status(500).json({ error: err });
  }
});

// Endpoint to fetch all logs
app.get('/api/logs', async (req, res) => {
  try {
    const logs = await Logs.findAll();
    res.json(logs);
  } catch (err) {
    console.log(err)
    res.status(500).json({ error: err });
  }
});


const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

