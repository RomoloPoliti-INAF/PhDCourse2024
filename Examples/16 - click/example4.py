#! /usr/bin/env python3
import rich_click as click
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()  
def sync():
    """Perform the sync"""
    click.echo('Syncing')
    
if __name__ == "__main__":
    cli()
