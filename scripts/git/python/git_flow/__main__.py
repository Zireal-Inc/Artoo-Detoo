from .cli import CLI

def main():
    cli = CLI()
    return cli.execute()

if __name__ == '__main__':
    exit(main())
