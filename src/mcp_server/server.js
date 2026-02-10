#!/usr/bin/env node

/**
 * GitHub MCP Server for ANSYS Fluent Integration
 * 提供与 GitHub 交互的 MCP 工具
 */

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { Octokit } = require("@octokit/rest");
const fs = require('fs').promises;
const path = require('path');
require('dotenv').config();

// 加载配置
const config = require('../../config/mcp_config.json');

// 初始化 GitHub 客户端
const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
  baseUrl: config.github.api_url
});

// 创建 MCP Server
const server = new Server(
  {
    name: config.server.name,
    version: config.server.version
  },
  {
    capabilities: {
      tools: {},
      resources: {}
    }
  }
);

/**
 * 工具: 创建 GitHub 仓库
 */
server.setRequestHandler("tools/call", async (request) => {
  const { name, params } = request.params;

  try {
    switch (name) {
      case "create_repository":
        return await createRepository(params);
      
      case "push_files":
        return await pushFiles(params);
      
      case "create_pull_request":
        return await createPullRequest(params);
      
      case "create_issue":
        return await createIssue(params);
      
      case "list_repositories":
        return await listRepositories(params);
      
      case "get_repository":
        return await getRepository(params);
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

/**
 * 列出可用工具
 */
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "create_repository",
        description: "创建新的 GitHub 仓库",
        inputSchema: {
          type: "object",
          properties: {
            name: {
              type: "string",
              description: "仓库名称"
            },
            description: {
              type: "string",
              description: "仓库描述"
            },
            private: {
              type: "boolean",
              description: "是否私有",
              default: false
            }
          },
          required: ["name"]
        }
      },
      {
        name: "push_files",
        description: "推送文件到 GitHub 仓库",
        inputSchema: {
          type: "object",
          properties: {
            owner: {
              type: "string",
              description: "仓库所有者"
            },
            repo: {
              type: "string",
              description: "仓库名称"
            },
            branch: {
              type: "string",
              description: "分支名称",
              default: "main"
            },
            files: {
              type: "array",
              description: "要推送的文件列表",
              items: {
                type: "object",
                properties: {
                  path: {
                    type: "string",
                    description: "文件路径"
                  },
                  content: {
                    type: "string",
                    description: "文件内容"
                  }
                }
              }
            },
            message: {
              type: "string",
              description: "提交消息"
            }
          },
          required: ["owner", "repo", "files", "message"]
        }
      },
      {
        name: "create_pull_request",
        description: "创建 Pull Request",
        inputSchema: {
          type: "object",
          properties: {
            owner: {
              type: "string",
              description: "仓库所有者"
            },
            repo: {
              type: "string",
              description: "仓库名称"
            },
            title: {
              type: "string",
              description: "PR 标题"
            },
            body: {
              type: "string",
              description: "PR 描述"
            },
            head: {
              type: "string",
              description: "源分支"
            },
            base: {
              type: "string",
              description: "目标分支",
              default: "main"
            }
          },
          required: ["owner", "repo", "title", "head"]
        }
      },
      {
        name: "create_issue",
        description: "创建 Issue",
        inputSchema: {
          type: "object",
          properties: {
            owner: {
              type: "string",
              description: "仓库所有者"
            },
            repo: {
              type: "string",
              description: "仓库名称"
            },
            title: {
              type: "string",
              description: "Issue 标题"
            },
            body: {
              type: "string",
              description: "Issue 内容"
            },
            labels: {
              type: "array",
              description: "标签",
              items: { type: "string" }
            }
          },
          required: ["owner", "repo", "title"]
        }
      },
      {
        name: "list_repositories",
        description: "列出用户的仓库",
        inputSchema: {
          type: "object",
          properties: {
            type: {
              type: "string",
              description: "仓库类型 (all, owner, member)",
              default: "owner"
            }
          }
        }
      },
      {
        name: "get_repository",
        description: "获取仓库信息",
        inputSchema: {
          type: "object",
          properties: {
            owner: {
              type: "string",
              description: "仓库所有者"
            },
            repo: {
              type: "string",
              description: "仓库名称"
            }
          },
          required: ["owner", "repo"]
        }
      }
    ]
  };
});

// 工具实现函数

async function createRepository(params) {
  const { name, description, private: isPrivate } = params;
  
  const response = await octokit.repos.createForAuthenticatedUser({
    name,
    description,
    private: isPrivate || false,
    auto_init: true
  });
  
  return {
    content: [
      {
        type: "text",
        text: `✅ 仓库创建成功!\n\n` +
              `名称: ${response.data.name}\n` +
              `URL: ${response.data.html_url}\n` +
              `克隆: ${response.data.clone_url}`
      }
    ]
  };
}

async function pushFiles(params) {
  const { owner, repo, branch = "main", files, message } = params;
  
  // 获取最新提交
  const { data: ref } = await octokit.git.getRef({
    owner,
    repo,
    ref: `heads/${branch}`
  });
  
  const commitSha = ref.object.sha;
  
  // 获取最新提交的树
  const { data: commit } = await octokit.git.getCommit({
    owner,
    repo,
    commit_sha: commitSha
  });
  
  // 创建文件 blobs
  const blobs = await Promise.all(
    files.map(async (file) => {
      const { data: blob } = await octokit.git.createBlob({
        owner,
        repo,
        content: Buffer.from(file.content).toString('base64'),
        encoding: 'base64'
      });
      
      return {
        path: file.path,
        mode: '100644',
        type: 'blob',
        sha: blob.sha
      };
    })
  );
  
  // 创建新树
  const { data: tree } = await octokit.git.createTree({
    owner,
    repo,
    base_tree: commit.tree.sha,
    tree: blobs
  });
  
  // 创建新提交
  const { data: newCommit } = await octokit.git.createCommit({
    owner,
    repo,
    message,
    tree: tree.sha,
    parents: [commitSha]
  });
  
  // 更新引用
  await octokit.git.updateRef({
    owner,
    repo,
    ref: `heads/${branch}`,
    sha: newCommit.sha
  });
  
  return {
    content: [
      {
        type: "text",
        text: `✅ 文件推送成功!\n\n` +
              `提交: ${newCommit.sha}\n` +
              `消息: ${message}\n` +
              `文件数: ${files.length}`
      }
    ]
  };
}

async function createPullRequest(params) {
  const { owner, repo, title, body, head, base = "main" } = params;
  
  const response = await octokit.pulls.create({
    owner,
    repo,
    title,
    body,
    head,
    base
  });
  
  return {
    content: [
      {
        type: "text",
        text: `✅ Pull Request 创建成功!\n\n` +
              `标题: ${response.data.title}\n` +
              `编号: #${response.data.number}\n` +
              `URL: ${response.data.html_url}`
      }
    ]
  };
}

async function createIssue(params) {
  const { owner, repo, title, body, labels } = params;
  
  const response = await octokit.issues.create({
    owner,
    repo,
    title,
    body,
    labels: labels || []
  });
  
  return {
    content: [
      {
        type: "text",
        text: `✅ Issue 创建成功!\n\n` +
              `标题: ${response.data.title}\n` +
              `编号: #${response.data.number}\n` +
              `URL: ${response.data.html_url}`
      }
    ]
  };
}

async function listRepositories(params) {
  const { type = "owner" } = params;
  
  const response = await octokit.repos.listForAuthenticatedUser({
    type,
    per_page: 30,
    sort: "updated"
  });
  
  const repoList = response.data
    .map(repo => `- ${repo.full_name} (${repo.private ? '私有' : '公开'})`)
    .join('\n');
  
  return {
    content: [
      {
        type: "text",
        text: `📚 仓库列表 (${response.data.length}):\n\n${repoList}`
      }
    ]
  };
}

async function getRepository(params) {
  const { owner, repo } = params;
  
  const response = await octokit.repos.get({
    owner,
    repo
  });
  
  const data = response.data;
  
  return {
    content: [
      {
        type: "text",
        text: `📦 仓库信息:\n\n` +
              `名称: ${data.full_name}\n` +
              `描述: ${data.description || '无'}\n` +
              `URL: ${data.html_url}\n` +
              `Stars: ${data.stargazers_count}\n` +
              `Forks: ${data.forks_count}\n` +
              `语言: ${data.language || '未知'}\n` +
              `创建时间: ${data.created_at}\n` +
              `最后更新: ${data.updated_at}`
      }
    ]
  };
}

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("✅ Fluent GitHub MCP Server 已启动");
  console.error(`📡 Server: ${config.server.name} v${config.server.version}`);
  console.error(`🔧 GitHub API: ${config.github.api_url}`);
}

main().catch((error) => {
  console.error("❌ Server error:", error);
  process.exit(1);
});
