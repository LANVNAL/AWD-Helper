> 19年1月写的代码，当时的一个想法就顺手写了个半成品，后来找不到了，今天又翻出来了，有空了要推倒重写（提示代码质量😢）

# 攻击
## 目标主机管理
• 主机发现，（端口探测），手动添加/nmap扫描\
• 按服务分类主机，定时检测是否在线\
• 显示端口信息，编辑备注\
• 定时检测主机是否在线，shell是否还在\
• 在思考：端口扫描如果每个主机都进行一次，频率像检测是否在线一样的话会花费大量的时间。端口扫描一遍会花费不少时间，是开始每个主机扫一遍就记录还是经常扫描只是每个服务只扫一个主机呢？
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548673486772-ab1676c5-5649-407b-9528-be8794ae95fd.png)
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548673538233-c904b948-e260-4e56-87ab-61655f6cd164.png)

## shell管理
• shell管理\
• 批量种内存马（骑一句话）\
• 上大马\
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548673686719-b69673a6-73d6-4d08-8192-4fc48e862caa.png)
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548673696300-39203c3d-8643-452a-82dc-cd4732a6e235.png)

## flag提交
• 目前思考有三种方式的flag提交（获取flag内容本机提交，目标机提交，payload一把梭）\
• 1.flag提交方式多样2.多种方式的处理 3.效率可能不如写脚本（这是目前在思考的问题，所以这个模块不是很完善）\
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548673891713-d4a7bd8a-b4cf-429a-bf05-566e7eb37e2d.png)

# 防御

## 文件监控
• 监控和保护维护主机的文件变化，显示文件的变化日志\
• 考虑遇到被写马等危险情况进行弹警告。\
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548674204880-9f4019b3-6681-4aef-975a-bba1b9fb5c1a.png)

## 流量log
• 在思考：1.访问流量很大，只是记录日志没意义（量大在平台分析不如直接看文件） 2.考虑只对非正常访问（攻击，带flag等）记录并转发过来\

## 进程log
• 记录进程的变化情况
![](https://cdn.nlark.com/yuque/0/2019/png/239512/1548674398796-1b10f452-dd8f-4ff8-b7e5-c5c87e58bd16.png)
