import { Octokit } from 'octokit';

export const syncToGitHub = async (repoData) => {
  if (!process.env.GITHUB_TOKEN || !process.env.GITHUB_OWNER || !process.env.GITHUB_REPO) {
    return { message: 'GitHub integration is not configured' };
  }

  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  const path = `Competitive-Programming/${repoData.platform}/${repoData.folder}/${repoData.fileName}`;

  try {
    await octokit.rest.repos.createOrUpdateFileContents({
      owner: process.env.GITHUB_OWNER,
      repo: process.env.GITHUB_REPO,
      path,
      message: `Solved ${repoData.problemName} on ${repoData.platform}`,
      content: Buffer.from(repoData.content).toString('base64')
    });

    return { message: 'GitHub sync successful' };
  } catch (error) {
    return { message: error.message };
  }
};
