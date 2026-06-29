import Problem from '../models/Problem.js';

export const getDashboard = async (req, res) => {
  try {
    const userId = req.user.id;
    const problems = await Problem.find({ userId }).sort({ submissionTime: -1 });

    const totalSolved = problems.length;
    const difficulties = problems.reduce((acc, item) => {
      acc[item.difficulty] = (acc[item.difficulty] || 0) + 1;
      return acc;
    }, {});

    const recent = problems.slice(0, 10);
    res.json({
      totalSolved,
      difficulties,
      recent,
      problems
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
