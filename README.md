# Target_tracking
# 🎯 视频处理与追踪应用

一个基于 Gradio + OpenCV 的网页应用，支持上传视频、打标追踪，并输出处理后的视频结果。

## 功能特点

- 上传视频
- 选择追踪算法（CSRT、KCF、MOSSE）
- 在第一帧打标选定目标
- 实时生成并展示追踪结果
- 动态渐变背景，界面友好美观

## 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/luckylukechan/Target_tracking.git
cd Target_tracking
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3.运行项目
```bash
python main.py
```


---

### 4. .gitignore

```gitignore
__pycache__/
*.pyc
dist/
build/
*.spec
*.mp4
*.avi
temp/
```

# 🔥 注意事项
部分使用者第一次使用需要额外下载软件包，按照命令提示窗口操作即可
打标窗口出现时，选好目标后按Enter键确认。
如遇运行代码无法自动跳转网页，可点击输出的网址手动跳转
不要开VPN，不要开VPN，不要开VPN
处理完的视频会自动显示在网页界面上。
支持常见视频格式，如 .mp4、.avi 等。
