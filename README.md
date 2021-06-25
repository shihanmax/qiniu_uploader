## Uploading files to Qiniu with CURL

1. 在根目录创建配置文件`config.py`，填写七牛相关信息：
```Python
# config.py
access_key = 'your_ak'
secret_key = 'you_sk'
domain = "your_domain"
bucket = "your_bucket"
```


2. 进入`serve`，修改`serve.sh`中的ip，端口配置，启动服务监听post请求：

```bash
bash serve.sh
```

3. 使用CURL或其他工具进行图片上传：


```bash
curl -X POST -F 'image=@hello.png' http://localhost:8088
```

如果成功，返回图片在七牛的外链地址等：
```json
{
    "html_link":"<img src='http://your_domain/you_img.png' alt='you_img.jng' style='zoom:67%;' />",
    "link":"http://your_domain/you_img.jng",
    "markdown_link":"![you_img.jng](http://your_domain/you_img.jng)",
    "status_code":200,
}
```

失败时返回状态码和相关附加信息：
```json
{
    "status_code": 404,
    "info": "error info",
}
```
