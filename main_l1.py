import click

from lab1 import simulate


@click.group()
def os_cli():
    pass


@click.command()
@click.option("-n", "--process_count", default=20)
@click.option("--min_ex_t", default=20)
@click.option("--max_ex_t", default=200)
@click.option("--max_toa", default=5000)
@click.option("-v", "--verbose", default=False, type=bool, is_flag=True)
def lab1(**data):
    simulate(data)


@click.command()
def lab2():
    click.echo("Not implemented :D")


os_cli.add_command(lab1)
os_cli.add_command(lab2)

if __name__ == '__main__':
    os_cli()
