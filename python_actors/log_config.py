import logging

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

actor_logger = logging.getLogger('actor_logger')
actor_file = logging.FileHandler('actor.log')
actor_file.setFormatter(formatter)
actor_logger.addHandler(actor_file)
