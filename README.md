# GitHub Sentinel

GitHub Sentinel 是一个开源的工具，旨在帮助开发者和项目管理人员自动获取并汇总他们关注的 GitHub 仓库的最新动态。该工具支持动态指令输入，使得用户可以方便地管理其订阅，并实时查看更新。

## 功能特性

- **动态订阅管理**：用户可以通过命令行添加或移除仓库订阅。
- **立即获取更新**：允许用户实时获取指定项目的最新更新。
- **后台定期检查**：在后台运行调度程序，定期检查所有订阅仓库的更新，而不会阻塞用户的输入。

## 环境要求

- Python 3.6 及以上版本
- 安装 `PyGithub` 和 `requests` 库

## 安装步骤

1. **克隆此仓库**：

   ```bash
   git clone https://github.com/your_username/GitHubSentinel.git
   cd GitHubSentinel
安装依赖：

使用以下命令安装所需的 Python 依赖：

bash
pip install -r requirements.txt
配置 GitHub 个人访问令牌：

在 GitHub 设置 中生成一个新的个人访问令牌（选择适当的权限）。
将生成的令牌替换到 config.py 中的 GITHUB_TOKEN 变量。
python
# config.py
GITHUB_TOKEN = "your_personal_access_token"  # 替换为你的 GitHub 个人访问令牌
SUBSCRIPTIONS = ["langchain-ai/langchain"]     # 可选，初始订阅的 GitHub 仓库
使用方法
运行程序：

在项目目录中执行以下命令启动工具：

bash
python main.py
可用命令：

在程序运行后，你可以输入以下命令来进行交互：

add \<repository>：添加新的仓库订阅，例如 add langchain-ai/langchain。
remove \<repository>：移除已有的仓库订阅，例如 remove langchain-ai/langchain。
list：列出当前所有订阅的仓库。
update：立即获取并显示所有订阅仓库的最新更新。
exit：退出程序。
示例
请输入命令 (add/remove/list/update/exit): add langchain-ai/langchain
已添加订阅: langchain-ai/langchain

请输入命令 (add/remove/list/update/exit): list
当前订阅的仓库:
- langchain-ai/langchain

请输入命令 (add/remove/list/update/exit): update
**Repository:** langchain-ai/langchain
**Latest Events:**
- PushEvent at 2024-09-20T15:30:00Z
- PullRequestEvent at 2024-09-19T12:15:00Z
**Latest Release:** v0.0.1 - 2024-09-18T10:00:00Z
**Release URL:** [Link](https://github.com/langchain-ai/langchain/releases/tag/v0.0.1)

请输入命令 (add/remove/list/update/exit): exit
退出程序...
贡献
欢迎任何形式的贡献，包括报告问题、提出功能请求和提交代码。
