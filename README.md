# 自动化脚本工具集

存放各类自动化脚本的仓库，每个脚本独立管理，共享公共组件。

## 快速开始

### 环境要求

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装

```bash
# 克隆仓库
git clone <repo-url>
cd automation-scripts

# 同步依赖（创建虚拟环境并安装依赖）
uv sync
```

### 配置

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入实际配置：

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

或者直接编辑 `configs/feishu.toml` 配置文件。

### 运行

```bash
# 前台运行（可查看日志输出）
uv run python run_feishu.py

# 后台运行（Windows，无控制台窗口）
.venv\Scripts\pythonw.exe run_feishu.py
```

## 目录结构

```
automation-scripts/
├── common/                    # 公共组件
│   ├── __init__.py
│   ├── config_loader.py      # 配置加载器
│   └── tray_manager.py       # 系统托盘管理器
├── configs/                   # 配置文件
│   └── feishu.toml           # 飞书提醒配置
├── scripts/                   # 脚本目录
│   ├── __init__.py
│   └── feishu_reminder.py    # 飞书定时提醒
├── run_feishu.py             # 飞书提醒启动入口
├── pyproject.toml            # 项目配置（uv/依赖管理）
├── .env.example              # 环境变量模板
└── README.md                 # 说明文档
```

## 添加新脚本

1. 在 `scripts/` 创建脚本文件
2. 在 `configs/` 创建对应的 TOML 配置
3. 在项目根目录创建启动入口（如 `run_xxx.py`）
4. 在 `common/config_loader.py` 添加配置加载函数

**示例模板：**

```python
# scripts/my_script.py
class MyScriptApp:
    def __init__(self, config):
        self.config = config
        self.running = False
    
    def start(self):
        self.running = True
    
    def pause(self):
        pass
    
    def resume(self):
        pass
    
    def stop(self):
        self.running = False
```

```toml
# configs/my_script.toml
[my_script]
key = "value"
```

```python
# run_my_script.py
from common.tray_manager import TrayManager
from scripts.my_script import MyScriptApp
from common.config_loader import load_toml_config

def main():
    config = load_toml_config("configs/my_script.toml")["my_script"]
    app = MyScriptApp(config)
    tray = TrayManager(title="我的脚本", icon_letter="M")
    tray.set_app(app)
    tray.run()

if __name__ == "__main__":
    main()
```

## 飞书定时提醒

### 配置

编辑 `configs/feishu.toml` 或设置环境变量：

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| webhook_url | FEISHU_WEBHOOK_URL | 飞书群机器人 webhook |
| cron_expression | - | Cron 定时表达式 |
| message_title | - | 消息标题 |
| message_content | - | 消息内容 |

### 控制

右键点击系统托盘图标：暂停/恢复/退出

## Cron 表达式参考

格式：`分 时 日 月 周`

| 表达式 | 含义 |
|--------|------|
| `*/5 * * * *` | 每5分钟 |
| `0 9 * * 1-5` | 工作日9:00 |
| `0 */2 * * *` | 每2小时 |
