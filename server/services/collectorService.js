import Problem from '../models/Problem.js';

export const collectSolvedProblems = async (userId) => {
  const mockProblems = [
    {
      platform: 'CodeChef',
      problemName: 'FLOW001',
      problemId: 'FLOW001',
      difficulty: 'Easy',
      rating: 800,
      tags: ['Implementation'],
      language: 'C++',
      solutionCode: '#include <bits/stdc++.h>\nusing namespace std;\nint main(){int a,b;cin>>a>>b;cout<<a+b;}',
      submissionTime: new Date(),
      problemUrl: 'https://www.codechef.com/problems/FLOW001'
    },
    {
      platform: 'Codeforces',
      problemName: 'A. Watermelon',
      problemId: '4A',
      difficulty: 'Easy',
      rating: 800,
      tags: ['Math'],
      language: 'C++',
      solutionCode: 'int main(){int w; cin>>w; cout<<(w>2 && w%2==0?"YES":"NO");}',
      submissionTime: new Date(),
      problemUrl: 'https://codeforces.com/problemset/problem/4A'
    },
    {
      platform: 'LeetCode',
      problemName: 'Two Sum',
      problemId: '1',
      difficulty: 'Easy',
      rating: 1200,
      tags: ['Array', 'Hash Table'],
      language: 'JavaScript',
      solutionCode: 'var twoSum = function(nums, target) { const map = new Map(); for (let i=0;i<nums.length;i++){ const need=target-nums[i]; if(map.has(need)) return [map.get(need),i]; map.set(nums[i],i);} };',
      submissionTime: new Date(),
      problemUrl: 'https://leetcode.com/problems/two-sum/'
    }
  ];

  for (const problem of mockProblems) {
    const exists = await Problem.findOne({ userId, platform: problem.platform, problemId: problem.problemId });
    if (!exists) {
      await Problem.create({ userId, ...problem });
    }
  }

  return { count: mockProblems.length };
};
