import logging

"""
乳提，怎麼用log
"""

logging.basicConfig(
    filename='hh.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.debug('debug')
    logger.info('info')
    logger.warning('eqweqw')
    logger.warning('eqweqdasdasdw')
    logger.warning('eqweqwasdasdasdas')
    logger.error('error')
    logger.critical('critical')
print("123")
print(__name__)