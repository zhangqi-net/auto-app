# Flask 示例应用

这是一个使用 Flask 框架构建的简单网页应用。

## 功能特点

- 响应式设计
- 简洁的导航菜单
- 首页和关于页面

## 安装步骤

1. 克隆项目到本地
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行应用

1. 确保已激活虚拟环境
2. 运行应用：
   ```bash
   python app.py
   ```
3. 在浏览器中访问：`http://localhost:5000`

## 项目结构

```
.
├── app.py              # 主应用文件
├── requirements.txt    # 项目依赖
├── static/            # 静态文件目录
│   └── css/
│       └── style.css  # 样式文件
└── templates/         # 模板目录
    ├── index.html     # 首页模板
    └── about.html     # 关于页面模板
``` 