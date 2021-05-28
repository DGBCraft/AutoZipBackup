import datetime
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from mcdreforged.api.all import *

PLUGIN_ID = 'auto_zip_backup'
PLUGIN_METADATA = {
    'id': PLUGIN_ID,
    'version': '1.0.0',
    'name': 'AutoZipBackup',
    'description': '定时自动备份与防熊备份',
    'author': [
        'Sanluli36li'
    ],
    'dependencies': {
        'mcdreforged': '>=1.2.0',
        'minecraft_data_api': '*',
        'permanent_backup': '>=1.0.0'
	}
}

config = {
    'new_player_backup': True,          # 当新玩家登录时执行一次备份
    'daily_backup': True,               # 每日定时执行备份
    'daily_backup_time': '02:00:00',    # 自动备份时间
    'minimum_backup_interval': 600,     # 备份最小执行间隔, 默认为10分钟 (仅针对新玩家备份)
    'require_player_online': True       # 如果上次备份后没有任何玩家在线过，则不再执行备份
}
player_list = []

default_config = config.copy()
CONFIG_FILE = os.path.join('config', PLUGIN_ID, 'config.json')
PLAYER_LIST_FILE = os.path.join('config', PLUGIN_ID, 'players.json')

player_logged = False
last_backup_time = 0

def make_backup(server: ServerInterface, comment: str, boardcast: bool = True):
    global last_backup_time, player_logged

    if boardcast:
        server.say('正在执行备份: {}'.format(comment))

    server.execute_command('!!backup make {}'.format(comment))
    last_backup_time = datetime.datetime.now().timestamp()

    players = server.get_plugin_instance('minecraft_data_api').get_server_player_list()
    if players[0] == 0:
        player_logged = False
    else:
        player_logged = True

def daily_backup(server: ServerInterface):
    global config, player_logged
    if not config['require_player_online'] or player_logged:
        make_backup(server, 'daily')

####################
#  Scheduler
####################

scheduler = None

def init_scheduler(server: ServerInterface):
    global config, scheduler
    if scheduler:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
        del scheduler
    scheduler = BackgroundScheduler()
    hour, min, sec = config['daily_backup_time'].split(':')
    scheduler.add_job(daily_backup, 'cron', args = [server], id = 'daily_backup', 
        hour = int(hour), minute = int(min), second = int(sec))
    scheduler.start()
    
def drop_scheduler():
    global scheduler
    if scheduler:
        scheduler.remove_all_jobs()
        scheduler.shutdown()
        del scheduler

####################
#  MCDR Events
####################

def on_load(server: ServerInterface, old):
    global config, players, player_logged, scheduler
    load_config(server)
    load_players()

    player_logged = True

    if config['daily_backup']:
        init_scheduler(server)

def on_remove(server: ServerInterface):
    drop_scheduler()

def on_unloaded(server: ServerInterface):
    drop_scheduler()

def on_player_joined(server: ServerInterface, player: str, info: Info):
    global config, last_backup_time, player_list, player_logged

    player_logged = True
    # 新玩家加入游戏
    if config['new_player_backup'] and player not in player_list:
        player_list.append(player)
        save_players()
        
        # 仅超过备份时间间隔才可再次执行备份
        if datetime.datetime.now().timestamp() - last_backup_time > config['minimum_backup_interval']:
            make_backup(server, 'NEW-PLAYER-' + player, False)

####################
#  Config
####################

def load_config(server, source: CommandSource or None = None):
    global config
    try:
        config = {}
        with open(CONFIG_FILE) as file:
            json_data = json.load(file)
        for key in default_config.keys():
            config[key] = json_data[key]
    except:
        server.logger.info('Fail to read config file, using default value')
        config = default_config
        with open(CONFIG_FILE, 'w') as file:
            json.dump(config, file, indent=4)

def load_players():
    global player_list
    try:
        with open(PLAYER_LIST_FILE) as file:
            player_list = json.load(file)
    except:
        with open(PLAYER_LIST_FILE, 'w') as file:
            json.dump([], file, indent=4)

def save_players():
    global player_list
    with open(PLAYER_LIST_FILE, 'w') as file:
        json.dump(player_list, file, indent=4)

