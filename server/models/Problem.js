import mongoose from 'mongoose';

const problemSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  platform: { type: String, enum: ['CodeChef', 'Codeforces', 'LeetCode'], required: true },
  problemName: { type: String, required: true, trim: true },
  problemId: { type: String, trim: true },
  difficulty: { type: String, default: 'Unknown' },
  rating: { type: Number, default: 0 },
  tags: [{ type: String }],
  language: { type: String, default: '' },
  solutionCode: { type: String, default: '' },
  submissionTime: { type: Date, default: Date.now },
  problemUrl: { type: String, default: '' },
  status: { type: String, default: 'accepted' },
  metadata: { type: Object, default: {} }
}, { timestamps: true });

problemSchema.index({ userId: 1, platform: 1, problemId: 1 }, { unique: false });

export default mongoose.model('Problem', problemSchema);
