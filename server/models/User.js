import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  name: { type: String, required: true, trim: true },
  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
  password: { type: String, required: true },
  avatar: { type: String, default: '' },
  country: { type: String, default: '' },
  platformProfiles: {
    codechef: { type: Object, default: {} },
    codeforces: { type: Object, default: {} },
    leetcode: { type: Object, default: {} }
  },
  preferences: {
    theme: { type: String, default: 'dark' },
    notifications: { type: Boolean, default: true }
  }
}, { timestamps: true });

export default mongoose.model('User', userSchema);
