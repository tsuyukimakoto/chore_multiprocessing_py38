import logging
import multiprocessing
import sys

from plugins import get_function, PluginRegistry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if len(sys.argv) > 1 and sys.argv[1] == 'fork':
    multiprocessing.set_start_method('fork')
    logger.info('set_start_method: fork')


plugin_registry = None


def load_plugins():
    global plugin_registry
    plugin_registry = PluginRegistry()
    plugin_registry.func0 = get_function('plugins.func0')
    plugin_registry.func1 = get_function('plugins.func1')
    logger.info('plugin loaded.')


def process(i):
    remainder = i % 2
    return plugin_registry.process(remainder, i)


def main():
    pool = multiprocessing.Pool(2)
    result = pool.map(
        process,
        list(range(10))
    )
    pool.close()
    pool.join()
    return result


if __name__ == '__main__':
    load_plugins()
    logger.info(main())
