import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import rateLimit from 'express-rate-limit';
import authRoutes from './routes/authRoutes.js';
import dashboardRoutes from './routes/dashboardRoutes.js';
import { connectDB } from './config/db.js';

const app = express();

app.use(cors());
app.use(cookieParser());
app.use(express.json({ limit: '10mb' }));
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 300 }));

app.get('/health', (req, res) => res.json({ status: 'ok' }));
app.use('/api/auth', authRoutes);
app.use('/api', dashboardRoutes);

let connectPromise = null;
export const initDatabase = async () => {
  if (!connectPromise) {
    connectPromise = connectDB();
  }
  return connectPromise;
};

initDatabase().catch((error) => {
  console.error('MongoDB initialization failed:', error.message);
});

export default app;
