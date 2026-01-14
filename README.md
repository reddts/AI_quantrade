<p align="center">
	<img alt="logo" src="../main/show_pic/logo_120.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">AI-Quantrade</h1>
<h4 align="center">AI-Quantrade 是一个基于 FastAPI 构建的智能量化交易辅助平台，融合 AI 资讯分析与多策略支持，面向用户提供从策略研发到实盘部署的一体化解决方案。</h4>
<p align="center">
	<a href="https://github.com/reddts/AI-Quantrade"><img src="https://img.shields.io/github/stars/reddts/AI-Quantrade?style=social"></a>
	<a href="https://github.com/reddts/AI-Quantrade"><img src="https://img.shields.io/badge/AI__Quantrade-v1.0.0-brightgreen.svg"></a>
	<a href="https://github.com/reddts/AI-Quantrade/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
    <img src="https://img.shields.io/badge/python-≥3.10.15-blue">
    <img src="https://img.shields.io/badge/MySQL-≥5.7-blue">
</p>

## 平台简介

本平台是一款基于 Python 开发的通用人工智能平台，采用 FastAPI 框架，专注于智能分析功能的构建，作为未来多款智能产品的核心技术基础。平台推出的量化交易辅助应用 **AI-Quantrade**，融合了聚宽、米筐、雪球等主流量化平台的设计理念，重点聚焦于财经资讯 AI 解读与智能交易策略辅助。

**AI-Quantrade** 支持对财经新闻与行业资讯的语义分析，识别其对相关行业、板块、个股或指数的潜在影响，提供清晰的策略方向与市场情绪分析。用户可通过点击个股，查看该股票的 AI 智能评估，包括：是否具有投资价值、建议买卖点位、持有周期等个性化参考建议。

系统内置多种经典和前沿的交易策略，如：

- 阿隆指标策略（Aroon Indicator）  
- 动态资产平衡策略（Dynamic Asset Allocation）  
- ATR 波动率突破策略（Average True Range）  
- 海龟交易法则（Turtle Trading）  
- Alpha 因子驱动策略  
- 多因子模型策略（结合价值、成长、动量等因子）  
- 基于 XGBoost、LightGBM 等机器学习模型的预测性选股策略  

同时，平台支持用户自定义策略的编写与测试，兼容主流深度学习框架（如 TensorFlow、PyTorch），可在服务器端运行策略回测，确保运行稳定、结果可追溯。未来版本将集成实盘交易功能，打通从策略开发到实盘执行的完整流程。

平台采用 Web 应用架构，提升可用性与可访问性，并通过高效的信息交互机制，显著降低对本地 QMT 环境与第三方依赖的要求，为量化研究者和个人投资者提供一体化、智能化的量化交易实验与部署环境。


### 目前规划的功能
* 智能选股，通过股票综合信息由AI推理结果
* 量化交易建议，通过内置的量化交易策略分析选定股票的交易时机
* 用户中心，用户自建交易策略，并交由云端运行
* 策略交易，用户自建的交易策略可以在策略中心进行交易
* 策略回测，在用户中心中，用户自建的交易策略可以进行回测，在交易建议中，也可以针对选中股票进行阶段性回测
* 实盘交易接口，实盘交易接口仅针对提供python支持的QMT实盘交易软件进行开发



### 技术架构与用户体验
AI-Quantrade 的后端基于 FastAPI 开发，通过高效 API 服务支撑深度学习量化交易，支持与多种 AI 接口对接，websocket通信，实现资讯和行情按需推送，提升分析精度和个性化体验。管理端采用VUE构建，便于后台数据管理与扩展。用户端采用 UniApp 开发，支持小程序与 H5 平台，随时随地接入服务。
用户UI采用了uniapp的框架uni-plus，界面采用WOT UI框架，清新简约，注重用户体验，采用了ECharts可交互（拖动缩放）K 线图做为图表前端。


* 管理前端采用VUE 。
* 后端采用FastAPI、sqlalchemy、MySQL（PostgreSQL）、Redis、OAuth2 & Jwt。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 前端采用uniapp（vue + echarts 5）
* 支持多种AI接口，目前支持openai等，更多的ai接口接入中
* 特别鸣谢：<u>[insistence](https://github.com/insistence/RUOYI-FastAPI-Admin)</u> 提供的底盘，以及造轮子的前辈们 。

## 版本更迭记录
* v1.0.0 完成基本框架
* v1.0.1 完成后台会员数据管理


## 后台管理功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
3.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
4.  部门管理：配置系统组织机构（公司、部门、小组）。
5.  岗位管理：配置系统用户所属担任职务。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
14. 缓存监控：对系统的缓存信息查询，命令统计等。
15. 系统接口：根据业务代码自动生成相关的api接口文档。
18. AI 管理：  提供模型分类，模型管理，以及key池的管理

## 前端uniapp功能，前端PC版的功能相同
1. 资讯:  实时采集各类新闻资讯，陆续完善各类资讯采集和接口，对于资讯类内容提供AI分析，分析这类资讯对于各类市场和潜在股票板块的影响，后续扩展，扩展增加历史记忆，时间序列分析一个月以来相关资讯的共同影响作用，扩展2，增加对某个自选股票的影响，扩展3，增加多条件因素综合分析
2. 市场: 以列表的形式列出实时的股市行情数据，每个股票下方点击后显示该股的AI操作策略，分析数据时间间隔为1周，扩展1，增加分时段分析，比如1天，1个月，3个月等，时间粒度待定
3. 自选:  用户可以自己选定自己关注的股票，提供对这些股票的数据的AI分析，扩展，结合资讯数据进行分析。扩展2，扩展时段的时间序列分析
4. 策略： 内置系统策略，提供策略列表，通过点击策略列表提供策略套用股票回测，以及策略对股票的后续操作判断，高级用户提供自定义策略。
5. 我的： 会员中心，提供个人信息查看，系统语言设置等功能，高级用户支持实盘接口。

# 实盘接口 
需要支持QMT的实盘客户端，开发中


## 开发进度
| 序号 | 开发内容 | 完成情况 | 备注 |
| --- | --- | --- | --- |
| 1 | 后台框架的修改适配 | 已完成 |   |
| 2 | 会员管理功能 | 已完成 |   |
| 3 | AI接口的配置 | 已完成 |    |
| 4 | AI接口的开发 | 待开发 |   |
| 5 | 支付功能的开发 | 待开发 |   |
| 6 | 前端API接口框架开发 | 待开发 |   |
| 7 | 前端API接口功能开发 | 待开发 |   |
| 8 | 前端界面的开发 | 待开发 |   |


## 演示图
___

<table>
    <tr>
        <td><img src="../main/show_pic/admin_login.png"/></td>
        <td><img src="../main/show_pic/admin_perm.png"/></td>
    </tr>
    <tr>
        <td><img src="../main/show_pic/front_login_zh.png"/></td>
        <td><img src="../main/show_pic/front_login_en.png"/></td>
    </tr>
    <tr>
        <td><img src="../main/show_pic/front_uc_zh.png"/></td>
        <td><img src="../main/show_pic/front_uc_en.png"/></td>
    </tr>
</table>

https://github.com/reddts/AI-Quantrade/blob/main/

## 管理端在线体验（基本开发完成后会开放体验）
- *账号：admin*
- *密码：admin123*
- 演示地址：<a href="https://admin.ai-Quantrade.info">AI-Quantrade管理中心<a> 演示地址暂未启用

## 项目开发及发布

```bash
# 克隆项目
git clone https://github.com/reddts/AI-Quantrade.git

# 进入项目根目录
cd AI-Quantrade

# 如果使用的是MySQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements.txt
# 如果使用的是PostgreSQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements-pg.txt
```

### 关于项目文件结构的说明


#### 前端
前端包含两个部分，admin文件夹中是管理前端，app文件夹中是应用前端，这里就不分开写了统一给出运行代码
```bash
# 进入前端目录
cd fastapi-frontend/admin
#或者
cd fastapi-frontend/app

# 安装依赖
npm install 或 yarn --registry=https://registry.npmmirror.com

# 建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev 或 yarn dev
```

#### 服务端API，包含管理端API和前端API
通过不同的模块进行区分
```bash
# 进入服务端目录
cd fastapi-backend

# 配置环境
1.在.env.dev文件中配置开发模式的数据库环境
2.在.env.dev文件中配置开发模式的redis环境

# 运行sql文件
1.新建数据库ai-Quantrade(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-Quantrade.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-Quantrade-pg.sql

# 运行服务端
python3 app.py --env=dev
```

### 发布

本应用发布建议使用宝塔面板，或者DOCKER均可


#### 前端部分
不管是管理端前端还是应用前端，都是采用vue开发
```bash
# 构建测试环境
npm run build:stage 或 yarn build:stage

# 构建生产环境
npm run build:prod 或 yarn build:prod
```

#### 服务端API
```bash
# 进入服务端目录
cd fastapi-backend

# 配置环境
1.在.env.prod文件中配置生产模式的数据库环境
2.在.env.prod文件中配置生产模式的redis环境

# 运行sql文件
1.新建数据库ai-Quantrade(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-Quantrade.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-Quantrade-pg.sql

# 运行服务端API
python3 app.py --env=prod
```

### 访问
```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://127.0.0.1:8088
```

## 交流与赞助
如果有对本项目及FastAPI和AI感兴趣的朋友，欢迎入群交流。如果你觉得这个项目帮助到了你，你可以请作者喝杯咖啡表示鼓励☕。扫描下面微信二维码加入QQ群，加群请备注AI-Quantrade。请作者喝咖啡也请备注AI-Quantrade。

| QQ交流群 | 支付宝 |
|---|---|
| ![QQ交流群](https://github.com/reddts/AI-Quantrade/blob/main/show_pic/qqqun.png) | ![支付宝](https://github.com/reddts/AI-Quantrade/blob/main/show_pic/zfb.jpg) |
| QQ交流群 | 支付宝 |
