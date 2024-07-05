from datetime import datetime

class TimeUtil:
    def getNowFormatTimeString(self):
        # 获取当前时间
        now = datetime.now()
        # 格式化时间为 '年-月-日 时:分:秒' 的形式
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time