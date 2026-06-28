function info(message) {
  console.log(`[INFO] ${new Date().toISOString()} ${message}`);
}

function error(message, details = '') {
  const suffix = details ? `: ${details}` : '';
  console.error(`[ERROR] ${new Date().toISOString()} ${message}${suffix}`);
}

module.exports = { info, error };
