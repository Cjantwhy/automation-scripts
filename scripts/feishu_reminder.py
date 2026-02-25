import json
import time
import threading
import requests
from datetime import datetime
from croniter import croniter

class FeishuReminderApp:
    """飞书定时提醒应用"""
    
    def __init__(self, config):
        self.config = config
        self.running = False
        self.thread = None
        self.pause_event = threading.Event()
        self.pause_event.set()
        
    def send_message(self):
        """发送飞书消息"""
        try:
            payload = {
                "msg_type": "text",
                "content": {
                    "text": f"{self.config['message_title']}\n{self.config['message_content']}\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            }
            response = requests.post(self.config['webhook_url'], json=payload, timeout=10)
            response.raise_for_status()
            print(f"消息发送成功: {datetime.now()}")
        except Exception as e:
            print(f"消息发送失败: {e}")
    
    def get_next_run_time(self):
        """计算下一次执行时间"""
        now = datetime.now()
        itr = croniter(self.config['cron_expression'], now)
        return itr.get_next(datetime)
    
    def run_scheduler(self):
        """定时任务循环"""
        while self.running:
            if self.pause_event.is_set():
                next_run = self.get_next_run_time()
                wait_seconds = (next_run - datetime.now()).total_seconds()
                
                if wait_seconds > 0:
                    start_time = time.time()
                    while time.time() - start_time < wait_seconds:
                        if not self.running:
                            return
                        if not self.pause_event.is_set():
                            break
                        time.sleep(0.5)
                    
                    if self.pause_event.is_set() and self.running:
                        self.send_message()
                else:
                    time.sleep(1)
            else:
                time.sleep(0.5)
    
    def start(self):
        """启动提醒服务"""
        if not self.running:
            self.running = True
            self.pause_event.set()
            self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            print("提醒服务已启动")
    
    def pause(self):
        """暂停提醒服务"""
        self.pause_event.clear()
        print("提醒服务已暂停")
    
    def resume(self):
        """恢复提醒服务"""
        self.pause_event.set()
        print("提醒服务已恢复")
    
    def stop(self):
        """停止提醒服务"""
        self.running = False
        self.pause_event.set()
        if self.thread:
            self.thread.join(timeout=2)
        print("提醒服务已停止")

if __name__ == "__main__":
    from common.config_loader import load_feishu_config
    
    config = load_feishu_config()
    app = FeishuReminderApp(config)
    app.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        app.stop()
