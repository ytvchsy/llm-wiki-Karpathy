# Cloud Deployment

本方案支持把 Hermes/OpenClaw 和 llm-wiki 部署到云服务器：云端负责开发、飞书同步和 wiki 更新，GitHub 负责同步，你的电脑只需要 `git pull` 后用 Obsidian 浏览。

## 目标架构

```text
Feishu / code tasks / prompts
            │
            ▼
Cloud server: Hermes / OpenClaw / llm-wiki
            │
            │ update raw/ and wiki/
            ▼
Git commit + git push
            │
            ▼
GitHub: ytvchsy/llm-wiki-Karpathy
            │
            │ git pull
            ▼
Mac / Obsidian local vault
```

## 云服务器职责

- 运行 Hermes/OpenClaw 开发环境。
- 同步飞书资料到 `raw/feishu/`。
- 调用 LLM/Codex/Hermes 把开发进度、功能、架构和使用说明写入 `wiki/project/`。
- 执行 `python3 tools/wiki.py index` 和 `python3 tools/wiki.py lint`。
- 提交并推送 wiki 更新到 GitHub。

## 本地电脑职责

- 用 Obsidian 打开本地仓库。
- 定期 `git pull` 拉取云端更新。
- 审阅、补充或修正文档。
- 避免和云端同时编辑同一个 wiki 文件。

## 云服务器准备

推荐 Ubuntu 22.04/24.04 或 Debian 12。

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip curl ca-certificates
```

配置 Git 身份：

```bash
git config --global user.name "ytvchsy"
git config --global user.email "2305492203@qq.com"
```

配置 SSH key 并加入 GitHub：

```bash
ssh-keygen -t ed25519 -C "2305492203@qq.com"
cat ~/.ssh/id_ed25519.pub
ssh -T git@github.com
```

克隆 wiki：

```bash
git clone git@github.com:ytvchsy/llm-wiki-Karpathy.git
cd llm-wiki-Karpathy
python3 tools/wiki.py lint
```

## 飞书配置

在云服务器创建 `.env`：

```bash
cp .env.example .env
```

写入：

```bash
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx
```

不要提交 `.env`。

同步飞书文档：

```bash
python3 tools/feishu_sync.py fetch "https://example.feishu.cn/docx/xxxxxxxxxxxxxxxx" --title "项目会议"
```

## Hermes/OpenClaw 部署

Hermes/OpenClaw 作为云端开发代理运行。由于实际安装方式取决于你的 Hermes/OpenClaw 发行包或仓库，本仓库先固定部署契约：

```text
/opt/hermes-openclaw/         Hermes/OpenClaw 运行目录
/opt/hermes-openclaw/work/    项目代码工作区
/opt/llm-wiki/                本仓库 clone 目录
```

推荐目录：

```bash
sudo mkdir -p /opt/hermes-openclaw /opt/hermes-openclaw/work /opt/llm-wiki
sudo chown -R "$USER":"$USER" /opt/hermes-openclaw /opt/llm-wiki
```

部署 Hermes/OpenClaw 项目代码时，建议使用独立仓库，不要直接混进 llm-wiki：

```bash
cd /opt/hermes-openclaw/work
git clone <your-hermes-project-repo-url> project
```

如果 Hermes/OpenClaw 以 Docker Compose 运行，建议将配置写在 Hermes 项目仓库，并只把运行结论、架构说明和使用方法沉淀到本 wiki。

## Hermes/OpenClaw 开发后更新 wiki

开发任务完成后，云端代理必须更新：

- `wiki/project/project-progress.md`
- `wiki/project/project-features.md`
- `wiki/project/project-architecture.md`
- `wiki/project/project-usage.md`
- `wiki/project/project-decisions.md`

然后执行：

```bash
scripts/wiki_commit_push.sh "Update project wiki after Hermes development"
```

脚本会执行：

1. `git pull --rebase`
2. `python3 tools/wiki.py index`
3. `python3 tools/wiki.py lint`
4. `git add -A`
5. `git commit`
6. `git push`

如果没有文件变化，脚本会直接退出，不创建空提交。

## 本地 Obsidian 同步

你的电脑已经有本地仓库：

```bash
cd /Users/totus/data/llm-wiki
git pull
```

然后在 Obsidian 里打开：

```text
/Users/totus/data/llm-wiki
```

推荐本地只做阅读和小修；主要自动化更新由云服务器完成。

## 冲突处理原则

- 云端开发前先 `git pull --rebase`。
- 本地编辑前先 `git pull`。
- 不要让云端和本地同时改 `wiki/project/` 同一文件。
- 如果出现冲突，优先保留有来源、有日期、有决策上下文的内容。
- 冲突解决后运行 `python3 tools/wiki.py index` 和 `python3 tools/wiki.py lint`。

## 安全

- `.env`、API key、SSH 私钥只保存在云服务器，不提交 GitHub。
- GitHub remote 使用 SSH。
- 飞书应用权限只开所需文档读取权限。
- 云服务器建议只开放 SSH，并用密钥登录。

