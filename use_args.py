from itertools import zip_longest
import logging
import multiprocessing
import sys

from plugins import get_function, PluginRegistry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if len(sys.argv) > 1 and sys.argv[1] == 'fork':
    multiprocessing.set_start_method('fork')
    logger.info('set_start_method: fork')


def load_plugins():
    plugin_registry = PluginRegistry()
    plugin_registry.func0 = get_function('plugins.func0')
    plugin_registry.func1 = get_function('plugins.func1')
    logger.info('plugin loaded.')
    return plugin_registry


def process(tpl):
    plugin_registry = tpl[0]
    i = tpl[1]
    remainder = i % 2
    return plugin_registry.process(remainder, i)


def main():
    pluginRegistry = load_plugins()
    pool = multiprocessing.Pool(2)
    result = pool.map(
        process,
        zip_longest(
            (pluginRegistry,),
            list(range(10)),
            fillvalue=pluginRegistry,
        )
    )
    pool.close()
    pool.join()
    return result


if __name__ == '__main__':
    logger.info(main())
