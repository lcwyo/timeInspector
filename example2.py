import configparser

config = configparser.ConfigParser()

config['COMMON'] = {'Resizable' : False,
                     'font' : 'Comic Sans',
                     'break' : '50',
                     'start' : '8:00'
                     }
config['LARGE_FONT'] = {'font' : 'Comic Sans',
                        'size': 18}


with open('./res/config/settings.ini', 'w') as configfile:
    config.write(configfile)


