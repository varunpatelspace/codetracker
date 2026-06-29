import mongoose from 'mongoose';

const contestSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  name: { type: String, required: true },
  platform: { type: String, required: true },
  startTime: { type: Date, required: true },
  endTime: { type: Date, required: true },
  url: { type: String, default: '' },
  status: { type: String, default: 'upcoming' }
}, { timestamps: true });

export default mongoose.model('Contest', contestSchema);
