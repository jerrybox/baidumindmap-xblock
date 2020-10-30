### 安装说明

0. 遗留问题
    ```
    图片暂时不能上传，只能使用cms里的上传文件链接
    ```

1. python环境下安装
    - 打包与安装
    ```
    python setup.py bdist_wheel
    pip install --no-deps package.whl
    ```
    - 配置跨域资源白名单
    ```
        sudo vim /edx/app/edxapp/lms.env.json +/ENABLE_CORS_HEADERS  
        sudo vim /edx/app/edxapp/lms.env.json +/CORS_ORIGIN_ALLOW_ALL
        sudo vim /edx/app/edxapp/lms.env.json +/CORS_ORIGIN_WHITELIST
        
        sudo vim /edx/app/edxapp/cms.env.json +/ENABLE_CORS_HEADERS
        sudo vim /edx/app/edxapp/cms.env.json +/CORS_ORIGIN_ALLOW_ALL
        sudo vim /edx/app/edxapp/lms.env.json +/CORS_ORIGIN_WHITELIST
    ```

2. 静态文件处理
    ```
    需要将public下的baidumindmap文件夹放到/edx/var/edxapp/staticfiles下
    ```

3. 配置相关
    ```
    Advanced Module List使用 baidumindmap
    ```
 
4. 使用相关
    ```
    编辑器快捷键：
       保存数据到数据库：crtl + s
       导出脑图为图片： alt + s
    注意：
        保存数据到数据库，cms的发布按钮可能不可用，刷新页面然后可以点击发布
        如果脑图中使用了外部链接的图片，跨域资源可能会导致alt + s无法导出图片
    ```
