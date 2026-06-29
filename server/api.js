import app, { initDatabase } from './app.js';

export default async function handler(req, res) {
  await initDatabase();
  return app(req, res);
}
