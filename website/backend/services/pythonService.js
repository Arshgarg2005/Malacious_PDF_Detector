const path = require('path');
const { spawn } = require('child_process');

function runPrediction(pdfPath) {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '..', 'predict.py');
    const python = spawn('python3', [scriptPath, pdfPath], {
      cwd: path.join(__dirname, '..')
    });

    let stdout = '';
    let stderr = '';

    python.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    python.stderr.on('data', (chunk) => {
        const msg = chunk.toString();
        console.error(msg);   // <-- print it to the Node terminal
        stderr += msg;
    });

    python.on('error', (err) => {
      reject(new Error(`Failed to start Python process: ${err.message}`));
    });

    python.on('close', (code) => {
      if (code !== 0) {
        const details = stderr.trim() || `Python exited with code ${code}`;
        reject(new Error(details));
        return;
      }

      const payload = stdout.trim();
      try {
        const parsed = JSON.parse(payload);
        resolve(parsed);
      } catch (err) {
        reject(new Error(`Invalid JSON from Python: ${payload || err.message}`));
      }
    });
  });
}

module.exports = { runPrediction };
