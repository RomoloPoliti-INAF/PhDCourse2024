#! /usr/bin/env python3

import rich_click as click
def print_version(ctx,param,value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

@click.command()
@click.option('-f','--foo',default='1')
@click.option('-z','--zoo','park',default='park')
@click.option('--a',type=int,default=None)
@click.option('--f',type=click.File(),default=None)
@click.option('--b', is_flag=True, help="Flag example")
@click.option('-c','--c',count=True,default=None)
@click.option('--shout/--no-shout')
#@click.option('-n','--n',prompt=True)
@click.option('--version',is_flag=True,callback=print_version)
def example(foo,park,a,f,b,c,shout,n):
    print(foo)
    print(park)
    if not a is None:
        print(a)
    if not f is None:
        print(type(f))
    print(b)
    if not c is None:
        print(c)
    print(shout)
    pass


if __name__ == "__main__":
    example()