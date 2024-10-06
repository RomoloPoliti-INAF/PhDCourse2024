#! /usr/bin/env python3
import rich_click as click
@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx,debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    ctx.ensure_object(dict)
    ctx.obj['DEBUG']=debug


@cli.command()
@click.pass_context
@click.option('-v','--verbose',is_flag=True,help="Enable verbose")  
def sync(ctx,verbose):
    """Perform the sync"""
    click.echo('Syncing')
    if verbose:
        click.echo("Verbose on")
    if ctx.obj['DEBUG']:
        click.echo("Debug ON")
    
if __name__ == "__main__":
    cli()
