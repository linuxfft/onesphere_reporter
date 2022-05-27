# onesphere_reporter

## 开发前准备

```bash
git submodule update --init --recursive

pip install -r requirements.txt -i https://pypi.douban.com/simple

```

### 环境变量

```bash
ENV_REPORTS_DIR: reporters_dir路径, 默认为工作目录下的reports路径
ENV_HTTP_MAX_SIZE: HTTP Client Size, 单位为mb
ENV_RUNTIME: runtime 环境, 默认为dev
```

### 注意：

1. 图片渲染
    1. 确保jrxml中包含的静态资源为绝对路径。
    2. 绝对路径，在宿主机上，应用程序有访问权限
    3. 程序样例中操作方式(Linux)平台:
        1. 将图片放置在/opt/assets路径下
        2. 修改jrxml，将图片都写为绝对路径方式: /opt/assets/{图片文件名}

### 已知问题

- [ ] 生成的PDF不支持中文
- [X] 不支持资源问题，如图片等添加至报告中渲染
- [ ] 报告和报告的jrxml必须放置在ENV_REPORTS_DIR设定下(默认为工作目录下的reports路径),容器环境中一定为/opt/reports
