import os
import tomllib
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")


def load_toml_config(config_path: str | Path) -> dict[str, Any]:
    """加载 TOML 配置文件"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")
    
    with open(path, "rb") as f:
        return tomllib.load(f)


def get_env_or_config(env_key: str, config_value: str | None = None) -> str:
    """优先从环境变量获取值，否则使用配置文件中的值"""
    env_value = os.environ.get(env_key, "")
    return env_value if env_value else (config_value or "")


def load_feishu_config() -> dict[str, Any]:
    """加载飞书配置，处理环境变量"""
    config_dir = Path(__file__).parent.parent / "configs"
    config = load_toml_config(config_dir / "feishu.toml")
    
    feishu_config = config.get("feishu", {})
    
    return {
        "webhook_url": get_env_or_config("FEISHU_WEBHOOK_URL", feishu_config.get("webhook_url")),
        "cron_expression": feishu_config.get("cron_expression", "*/5 * * * *"),
        "message_title": feishu_config.get("message_title", "定时提醒"),
        "message_content": feishu_config.get("message_content", ""),
    }
