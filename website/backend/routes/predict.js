const express = require('express');

const { predict } = require('../controllers/predictController');
const upload = require('../middleware/upload');

const router = express.Router();

router.post('/predict', upload, predict);

module.exports = router;
