# linuxdeploy_sendSms

> 本工具实现了将Android手机短信发送到企业微信/邮箱的功能
> 前期准备工作请参考[这里](https://www.yrblog.cn/category/%e7%bc%96%e7%a8%8b/android%e4%b8%8a%e7%9a%84linux/ "这里")

### 使用方法
克隆到本地后，编辑sendWechat.py文件
首先找到短信db位置并填写，随后选择发送方式
```sendWechat.py
Dbpath = "/mnt/data/com.android.providers.telephony/databases/mmssms.db"#数据库地址，记得必须挂载
useWechat = True #@TRUE = 使用企业微信信息 @False=使用邮件发送信息
```
随后编辑企业微信配置或邮箱配置,如果不懂如何填写企业微信配置，请点击[这里](https://www.yrblog.cn/2019/08/21/androidlinux03/ "这里")具体学习。
```sendWechat.py
#企业微信配置
AgentId = ""
CropId = ""
Secret = ""
Touser = ""

#邮箱配置，以163为例
smtpHost = 'smtp.163.com'#邮箱发送配置
neateasyUser = 'xxx@163.com'# 163用户名
neateaseCode = ''# s授权码
sendEmail = 'xxxx@163.com'# 邮件发送方邮箱地址
receiveEmails = ['xxx@qq.com','xxx@gmail.com']#可以写多个接收方 qq邮箱记得添加白名单
```
接下来编辑sqlpy.py文件的sql语句。这里需要根据你的手机短信db结构来填写
```sqlpy.py
writeSql = "UPDATE sms SET seen = 1 ,read = 1 WHERE seen =0"#更改已经发送短信的读取状态
readSql = "SELECT address,body FROM sms WHERE seen=0"#将未读取短信提取
```
**更改完毕后在Android手机上使用supervisor或其他工具来运行sendWechat.py即可。**

### 关于作者
还有其他有趣的小项目会陆续在[这里](https://www.yrblog.cn/ "这里")更新的，希望大家关注。<br>
微信搜索yrtools关注我的公众号，或者下面的二维码。有一些例如京东返利工具的小工具会在上面运行。<br>
[![yrtools](https://www.yrblog.cn/wp-content/uploads/2019/08/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190821220711.png "yrtools")](https://www.yrblog.cn/wp-content/uploads/2019/08/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20190821220711.png "yrtools")


