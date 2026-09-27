const app = require('./app');
const logger = require('./utils/logger');

const PORT = process.env.PORT || 3000;

const server = app.listen(PORT, () => {
  logger.info(`Application started successfully on port ${PORT}`, {
    event: 'server_started',
    port: PORT
  });
});

module.exports = server;
