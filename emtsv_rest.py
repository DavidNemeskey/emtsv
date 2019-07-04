#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

"""REST interface to emtsv."""

from argparse import ArgumentParser, REMAINDER

from __init__ import init_everything, pipeline_rest_api, jnius_config, tools, presets

def parse_arguments():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--port', '-p', type=int, default=5000,
                        help='The port the Flask server will listen on (5000).')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show warnings')
    parser.add_argument('--conllu-comments', '-c', action='store_true',
                        help='Enable CoNLL-U style comments')

    parser.add_argument(dest='task', nargs=REMAINDER)

    return parser.parse_args()


def main():
    args = parse_arguments()

    jnius_config.classpath_show_warning = args.verbose  # Suppress warning.
    conll_comments = args.conllu_comments
    if len(args.task) > 0:
        used_tools = args.task[0].split(',')
        if len(used_tools) == 1 and used_tools[0] in presets:
            # Resolve presets to module names to init only the needed modules...
            used_tools = presets[used_tools[0]]

        inited_tools = init_everything({k: v for k, v in tools.items() if k in set(used_tools)})
    else:
        inited_tools = init_everything(tools)

    app = pipeline_rest_api(name='e-magyar-tsv', available_tools=inited_tools,
                            presets=presets, conll_comments=conll_comments)
    app.run(port=args.port, debug=True)


if __name__ == '__main__':
    main()
