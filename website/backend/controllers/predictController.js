const fs = require('fs/promises');

const { runPrediction } = require('../services/pythonService');
const logger = require('../utils/logger');

async function safeUnlink(filePath) {
  if (!filePath) return;
  try {
    await fs.unlink(filePath);
  } catch (err) {
    logger.error(`Failed to delete temp file ${filePath}`, err.message);
  }
}

async function predict(req, res) {
  const uploadedFiles = req.files || [];
  const file = uploadedFiles.find((f) => f.fieldname === 'pdf') || uploadedFiles.find((f) => f.fieldname === 'file');

  if (!file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }

  try {
    const result = await runPrediction(file.path);
    return res.json(result);
  } catch (err) {
    logger.error('Prediction failed', err.message);
    return res.status(500).json({ error: `Prediction failed: ${err.message}` });
  } finally {
    await safeUnlink(file.path);
  }
}

module.exports = { predict };
