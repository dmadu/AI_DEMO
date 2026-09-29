import app from './app';
import { logger } from './utils/logger';

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  logger.info('Application startup', {
    port: PORT,
    env: process.env.NODE_ENV || 'development',
  });
});
