# -*- coding:utf-8 -*-
import yaml

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigHandler(metaclass=Singleton):
    def __init__(self):
        with open("config.yaml") as file:
            self.content = yaml.load(file)

    def print(self):
        print(self.content)

    def getProperty(self, var1, var2):
         return self.content.get(var1).get(var2)

if __name__ == '__main__':
    configHandler = ConfigHandler()
    configHandler.print()
    print(configHandler.getProperty('remote', 'ip'))
