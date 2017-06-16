from .slack import Slack
import toml
import os
import sys


def register_emoji(team, mail, password, name, path):
    if not os.path.isfile(path):
        raise RuntimeError('{} is not existing or not file'.format(path))  # TODO: use User-defined Exception
    with Slack(team) as s:
        if not s.login(mail, password):
            raise RuntimeError('Failed to login')  # TODO: use User-defined Exception
        s.register_emoji(name, path)


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--configuration-file', default=os.path.expanduser('~/.config/slack.toml'))
    p.add_argument('-t', '--team-name')
    p.add_argument('emoji_name')
    p.add_argument('emoji_path')
    args = p.parse_args()

    try:
        config = toml.load(args.configuration_file)
        team = args.team_name or config['default_team']
        c = config[team]
        mail = c['mail']
        password = c['password']
        register_emoji(team, mail, password, args.emoji_name, args.emoji_path)
    except Exception as err:
        print('{}: {}'.format(type(err).__name__, err), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
