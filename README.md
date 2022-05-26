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

### 已知问题
- [ ] 生成的PDF不支持中文
- [ ] 不支持资源问题，如图片等添加至报告中渲染
- [ ] 报告和报告的jrxml必须方式在ENV_REPORTS_DIR设定下(默认为工作目录下的reports路径),容器环境中一定为/opt/reports
