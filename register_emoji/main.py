from .slack import Slack
import toml
import os
import sys


def register_emoji(team, name, path, cookie=None, mail=None, password=None, debug=False):
    if cookie is None and (mail is None or password is None):
        raise ValueError('either cookie or mail/password pair must be filled')
    if not os.path.isfile(path):
        raise RuntimeError('{} is not existing or not file'.format(path))  # TODO: use User-defined Exception
    with Slack(team, not debug) as s:
        if cookie:
            s.add_cookies(cookie)
        elif not s.login(mail, password):
            raise RuntimeError('Failed to login')  # TODO: use User-defined Exception
        s.register_emoji(name, path)


def load_netscape_cookies_txt(fpath):
    retval = []
    with open(os.path.expanduser(fpath)) as fp:
        for line in fp:
            if line[0] == '#' or line.strip() == '':
                continue
            retval.append(parse_line(line[:-1]))
    return retval


def parse_line(line):
    fields = line.split('\t')
    return {
        'domain': fields[0],
        'path': fields[2],
        'secure': fields[3] == 'TRUE',
        'expiry': fields[4],
        'name': fields[5],
        'value': fields[6]}


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--configuration-file', default=os.path.expanduser('~/.config/slack.toml'))
    p.add_argument('-t', '--team-name')
    p.add_argument('--debug', action='store_true')
    p.add_argument('emoji_name')
    p.add_argument('emoji_path')
    args = p.parse_args()

    try:
        config = toml.load(args.configuration_file)
        team = args.team_name or config['default_team']
        c = config[team]
        cookie = load_netscape_cookies_txt(c['cookie']) if 'cookie' in c else None
        mail = c.get('mail')
        password = c.get('password')
        register_emoji(team, args.emoji_name, args.emoji_path, cookie, mail, password, debug=args.debug)
    except Exception as err:
        print('{}: {}'.format(type(err).__name__, err), file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
