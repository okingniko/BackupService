# BackupService
A useful backup and download tools, implemented using paramiko and python standard library.
You can easy check errors via log file(default *./backup.log*)

##1. 准备工作
0. 若系统需要代理,则配置好系统的相关代理,例如,在shell中输入：
  ```shell
  export http_proxy="http://username:password@proxy_ip:proxy_port/"
  export https_proxy="http://username:password@proxy_ip:proxy_port/"
  ```

1. 克隆此项目：`git clone https://github.com/okingniko/BackupService.git`
2. 自动更新所需的paramiko库：`git submodule update --init --recursive`
3. 若系统未安装paramiko库,则使用以下命令安装：

  ```shell
  cd paramiko
  sudo python setup.py install
  ```

##2. 配置MainConf.json文件
###2.1 backup method
```json
"backup_conf" : [
    {
      "server_ip": "211.65.193.193",
      "remote_dir": "/root/backuptest",
      "user_name": "root",
      "user_password": "XXXXXXX",
      "local_dir": "/home/monster/BackupService",
      "local_files": ["/home/monster/bro_start.sh", 
                      "/home/monster/paramiko.tar.gz",
                      "/home/monster/bucunzaidewenjian"]
    }
   ]
```
其中：
- *server_ip*：远端(备份)服务器的ip
- *~~server_port~~*： 远端(备份)服务器为22,即ssh端口。
- *remote_dir*: 远端(备份)服务器的目的目录, 程序将自动根据当前日期创建子目录。
- *user_name*: 登录远端服务器的账户名
- *user_password*: 登录远端服务器的密码
- *local_dir*: 本地备份文件夹的位置
- *local_files*: 本地备份文件的位置

**技术细节注解:**
> 1. 文件夹的路径可以随意设置,但最好是你需要备份的目录位置(最后的分隔符选择加与不加都随意).

> 2. 本地可以为任意平台(E.g. windows, linux), 备份服务器需为linux系统.

> 3. 通过拷贝黏贴, 你可以轻松的配置多台服务器的备份工作, 
如果您不小心配置错误了,没有关系，程序将通过**日志记录**和**命令行输出**的形式为您提供充足的追查手段。

###2.2 Download method
**建设中...**

##3. 设置定时备份

使用编辑器(E.g. vim)打开`/etc/crontab` 文件，加入以下一行内容
```shell
0 2 * * * python path-to-the-backupservice -b > /dev/null
```
> - path-to-backupservice: 为BackupService.py在你系统上的绝对路径(E.g. /home/monster/BackupService/BackupService.py)
> - 上述行的意思是： 每日凌晨两点执行代码备份工作（crontab中有相应说明）
> - 若想查看BackService.py的完整用法，可使用`-h`或`--help`参数查看

##4. Debug version Demo
###4.1 Windows 
![Windows backup](/media/window_backup.gif)

###4.2 Linux 
![Linux backup](/media/linux_backup.gif)

##4. TODO：
1. Add Download Mode.
2. ~~Add CMD Argument parsing Or Add Graphical interface.~~
3. Etc.

##5. 参考链接
- [python paramiko简介和使用方法](http://www.codexiu.cn/python/blog/127/)
- [Paramiko Documentation](http://docs.paramiko.org/en/1.16/)
