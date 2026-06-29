import cron from 'node-cron';
import { collectSolvedProblems } from '../services/collectorService.js';
import User from '../models/User.js';

export const startAutomation = () => {
  cron.schedule('*/5 * * * *', async () => {
    try {
      const users = await User.find();
      for (const user of users) {
        await collectSolvedProblems(user._id);
      }
      console.log('Automation cycle completed');
    } catch (error) {
      console.error('Automation cycle failed:', error.message);
    }
  });
};
