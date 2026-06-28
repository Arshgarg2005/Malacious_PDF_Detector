const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');

const predictRoutes = require('./routes/predict');
const logger = require('./utils/logger');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

app.use('/api', predictRoutes);
app.use('/', predictRoutes);

app.use((err, req, res, next) => {
  logger.error('Unhandled error', err);
  return res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  logger.info(`Server listening on http://127.0.0.1:${PORT}`);
});
