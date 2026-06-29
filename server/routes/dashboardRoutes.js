import express from 'express';
import { getDashboard } from '../controllers/dashboardController.js';
import { authenticate } from '../utils/auth.js';

const router = express.Router();
router.get('/dashboard', authenticate, getDashboard);

export default router;
