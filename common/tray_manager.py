import sys
import threading
import time
from typing import Callable, Optional

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

class TrayManager:
    """通用的系统托盘管理器"""
    
    def __init__(self, title: str = "自动化脚本", icon_letter: str = "A"):
        self.title = title
        self.icon_letter = icon_letter
        self.icon = None
        self.paused = False
        self.app = None
        self._running = False
        
    def set_app(self, app):
        """设置应用实例"""
        self.app = app
        
    def create_image(self, color="blue"):
        """创建图标"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        dc = ImageDraw.Draw(image)
        
        if color == "blue":
            bg_color = (66, 133, 244)
        elif color == "yellow":
            bg_color = (251, 188, 5)
        elif color == "red":
            bg_color = (234, 67, 53)
        else:
            bg_color = (66, 133, 244)
        
        dc.ellipse([4, 4, width-4, height-4], fill=bg_color)
        dc.text((width//2-12, height//2-16), self.icon_letter, fill=(255, 255, 255), font=None)
        
        return image
        
    def on_start(self, icon, item):
        if self.app and not self.app.running:
            self.app.start()
            self.update_icon()
        
    def on_pause_resume(self, icon, item):
        if not self.app:
            return
        if self.paused:
            self.app.resume()
            self.paused = False
        else:
            self.app.pause()
            self.paused = True
        self.update_icon()
        
    def on_exit(self, icon, item):
        if self.app:
            self.app.stop()
        icon.stop()
        
    def get_status_text(self, icon=None, item=None):
        if not self.app:
            return "服务状态: 未加载"
        if not self.app.running:
            return "服务状态: 已停止"
        elif self.paused:
            return "服务状态: 已暂停"
        else:
            return "服务状态: 运行中"
        
    def update_icon(self):
        if self.icon:
            if not self.app or not self.app.running:
                self.icon.icon = self.create_image("red")
            elif self.paused:
                self.icon.icon = self.create_image("yellow")
            else:
                self.icon.icon = self.create_image("blue")
                
    def setup_menu(self):
        return pystray.Menu(
            pystray.MenuItem(self.get_status_text, lambda icon, item: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("启动服务", self.on_start),
            pystray.MenuItem("暂停/恢复", self.on_pause_resume),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("退出", self.on_exit)
        )
        
    def run(self):
        """运行系统托盘"""
        if not PYSTRAY_AVAILABLE:
            print("系统托盘不可用，使用命令行模式")
            if self.app:
                self.app.start()
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    self.app.stop()
            return
            
        if self.app:
            self.app.start()
        
        self.icon = pystray.Icon(
            "automation_script",
            self.create_image("blue"),
            self.title,
            self.setup_menu()
        )
        
        def update_loop():
            while self._running:
                self.icon.menu = self.setup_menu()
                self.update_icon()
                time.sleep(1)
                
        self._running = True
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        
        self.icon.run()
        self._running = False
