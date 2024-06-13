import pathlib
import logging
import click
import os

@click.group()
def app():
    intro = """
        _______  _________________________________._______  ________________________________
        \      \ \_   _____/\__    ___/\_   _____/|   \   \/  /  _____/\______   \__    ___/
        /   |   \ |    __)_   |    |    |    __)  |   |\     /   \  ___ |     ___/ |    |   
        /    |    \|        \  |    |    |     \   |   |/     \    \_\  \|    |     |    |   
        \____|__  /_______  /  |____|    \___  /   |___/___/\  \______  /|____|     |____|   
                \/        \/                 \/              \_/      \/                     
    """
    click.echo(
        click.style(
            intro, fg="bright_blue"
        )
    )

def main():
    app(standalone_mode=True)

if __name__ == "__main__":
    main()
