"""Glue the app together."""


# ------ Importing modules ------
from modules import *
from yaml import safe_load


# ------ Loading files ------
with open('config.yaml', 'r') as file:
    conf = safe_load(file)


# ------ Initialising loggers ------
loggers = conf['loggers']
log_folder = loggers['folder']

discord_handler_logger_attr = {
    "name": loggers['discord_handler']['name'],
    "log_folder": log_folder,
    "log_level": loggers['discord_handler']['log_level']
}

png_generator_logger_attr = {
    "name": loggers['png_generator']['name'],
    "log_folder": log_folder,
    "log_level": loggers['png_generator']['log_level']
}

main_logger_attr = {
    "name": loggers['default']['name'],
    "log_folder": log_folder,
    "log_level": loggers['default']['log_level']
}

discord_handler_logger = init_logger(**discord_handler_logger_attr)
png_generator_logger = init_logger(**png_generator_logger_attr)
main_logger = init_logger(**main_logger_attr)
