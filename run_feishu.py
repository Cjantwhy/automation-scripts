"""
飞书提醒启动入口
使用系统托盘管理器运行
"""
from common.tray_manager import TrayManager
from scripts.feishu_reminder import FeishuReminderApp
from common.config_loader import load_feishu_config


def main():
    config = load_feishu_config()
    app = FeishuReminderApp(config)
    tray = TrayManager(title="飞书提醒服务", icon_letter="F")
    tray.set_app(app)
    tray.run()


if __name__ == "__main__":
    main()
