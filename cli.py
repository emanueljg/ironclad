import click

@click.group()
def cli():
    """Ironclad - a small program for getting shit done"""
    pass

@cli.command()
def do():
    click.echo('I did')

@cli.group()
def schedule():
    """new test group"""
    pass

@schedule.command()
def aaa():
    click.echo('woah you di dit')

if __name__ == '__main__':
    cli()
