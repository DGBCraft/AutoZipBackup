# AutoZipBackup
一个基于[PermanentBackup](https://github.com/MCDReforged/PermanentBackup)的自动备份[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)插件。  
AutoZipBackup将在每天固定时间使用`!!backup make`命令创建一份永久备份档案。  
此外，AutoZipBackup将在有新玩家加入服务器时创建一次备份。  

## 需求
**需要安装python模块**: `apscheduler`  
```
pip install apscheduler
```
**依赖的MCDR插件**:   
[PermanentBackup](https://github.com/MCDReforged/PermanentBackup) >= 1.0  
[Minecraft Data API](https://github.com/MCDReforged/MinecraftDataAPI) *

## 配置文件
配置文件位为`config/auto_zip_backup/config.json`
```
{
    "new_player_backup": true,
    "daily_backup": true,
    "daily_backup_time": "02:00:00",
    "minimum_backup_interval": 600,
    "require_player_online": true
}
```
`new_player_backup`: 当有新玩家加入游戏时候执行备份  
`daily_backup`: 启用每日备份  
`daily_backup_time`: 执行每日备份的时间  
`minimum_backup_interval`: 执行备份的最小时间间隔  
`require_player_online`: 如果为`true`，则仅当两次备份之间有玩家曾经在线过才会执行备份  

`config/auto_zip_backup/players.json`为曾经登录过的玩家列表