const express = require('express');
const https = require('https');
const fs = require('fs');
const cors = require('cors');
const { Binstatus, Bins, Food, Logs } = require('./models');

const app = express();

// Apply CORS middleware
app.use(cors({
  origin: 'https://localhost:5173' // Adjust according to your setup
}));

app.use(express.json());

// sample endpoint
app.get('/api/test', async (req, res) => {
  try {
    res.json({message: "yass!"});
  } catch (err) {
    console.log(err)
    res.status(500).json({ error: err });
  }
})

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

const httpsOptions = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
};

https.createServer(httpsOptions, app).listen(5000, () => {
  console.log('HTTPS Server running on port 5000');
});
