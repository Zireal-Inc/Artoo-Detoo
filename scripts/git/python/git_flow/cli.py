import argparse
from . import __version__
from . import GitFlow
from .commands import InitCommand, FeatureCommand

class CLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.gitflow = GitFlow()

    def _create_parser(self):
        parser = argparse.ArgumentParser(description='Git Flow tool')
        parser.add_argument('--version', action='version', version=f'git-flow {__version__}')
        
        subparsers = parser.add_subparsers(dest='command', help='Git Flow command')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize git-flow')
        init_parser.add_argument('-d', '--defaults', action='store_true', help='Use default branch names')
        
        # Feature command
        feature_parser = subparsers.add_parser('feature', help='Manage feature branches')
        feature_subparsers = feature_parser.add_subparsers(dest='subcommand')
        
        feature_start = feature_subparsers.add_parser('start', help='Start a new feature')
        feature_start.add_argument('name', help='Feature name')
        feature_start.add_argument('base', nargs='?', help='Base branch')
        
        feature_finish = feature_subparsers.add_parser('finish', help='Finish a feature')
        feature_finish.add_argument('name', help='Feature name')
        
        return parser

    def execute(self):
        args = self.parser.parse_args()
        args_dict = vars(args)
        command = args_dict.pop('command')
        subcommand = args_dict.pop('subcommand', None)

        try:
            if command == 'init':
                cmd = InitCommand(self.gitflow)
                cmd.init(defaults=args_dict.get('defaults', False))
                
            elif command == 'feature':
                cmd = FeatureCommand(self.gitflow)
                
                if subcommand == 'start':
                    cmd.start(args_dict.get('name'), args_dict.get('base'))
                elif subcommand == 'finish':
                    cmd.finish(args_dict.get('name'))
                    
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
            
        return 0

if __name__ == '__main__':
    cli = CLI()
    cli.execute()
