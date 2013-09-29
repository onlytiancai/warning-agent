### 配置详解

请参考*src/config.ini*，里面有详细的注释。

### 基本原理

1. 定时通过counter来获取CPU,内存，磁盘使用率, 磁盘IO，网络IO以及你想收集的任何计数信息。
1. 获取到的计数信息会通过logger保存到磁盘或数据库中，以后排查问题可以使用，类似sar。
1. 当获取到新的计数信息时，会根据用户定义好的rule来判断当前系统和业务是否出现异常。
1. 如果rule发现异常，就会调用sender把报警发送给你，具体怎么发送你可以完全定制。

### 插件机制

这是一个极度可扩展的软件，可以写如下插件来满足您的需求：

* logger: 用来存取各种性能计数信息，默认以文本形式保存，你可以写插件保存到redis,mysql里。
* counter: 用来产生各种计数，默认只获取cpu,mem,io等信息，你可以写插件来获取redis,mysql,nginx，以及你的业务计数。
* rule: 用来实现报警判断逻辑，默认只对系统性能进行报警，你可以写插件实现各种报警规则。
* sender: 用来实现报警的发送，默认是发送到warnings.sinaapp.com，你可以写插件来发到你的邮箱，微信，短信。

src目录下的loggers,counters, rules, senders子目录各有一个插件的示例，照猫画虎一般5分钟就可以写一个插件来满足你的需求了。

### 日志

1. /var/log/wawa-warning-agent.log: 保存程序运行的日志，如果程序运行出错，可以看这里。
   该日志没有设置自动滚动，请自行用logrotate来滚动压缩该日志。
1. /var/log/wawa-warning-agent-counter.log: 该文件是默认logger保存计数信息的地方，会自动滚动。
