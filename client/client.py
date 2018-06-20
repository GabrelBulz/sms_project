import ConfigParser

config = ConfigParser.ConfigMachine('conf.ini')

config.parse_conf()
print(config.id_node)
print(config.metrics)
print(config.interval)

exit()