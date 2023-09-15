import click
import os
from pathlib import Path
import shutil
import subprocess

ghdl_bin = 'ghdl'
gtkwave_bin = 'gtkwave'

def ghdl_installed() -> bool:
    if not shutil.which(ghdl_bin):
        click.echo("GHDL bin not found")
        return False
    else:
        click.echo("Suitible GHDL candidate found")
        return True

def gtkwave_installed() -> bool:
    if not shutil.which(gtkwave_bin):
        click.echo("gtkwave bin not found")
        return False
    else:
        click.echo("Suitible gtkwave candidate found")
        return True

@click.group()
def cli():
    """Wrapper for GHDL and GTKwave to produce easy simulations and
syntax checking."""

@click.command()
@click.option("--file", "-f", "file_",
              help="Checks the specified file for syntax errors.",
              type=click.Path())
def check(file_):
    """Checks files for syntax errors."""
    files = []
    if file_:
        files.append(file_)
    else:
        for file in os.listdir('.'):
            if file.endswith('.vhd') or file.endswith('.vhdl'):
                files.append(file)

    for file in files:
        click.echo(f"Analyzing {file}")
        subprocess.run([ghdl_bin, '-a', file])

@click.command()
@click.argument("testbench",
              type=click.Path(exists=True, path_type=Path))
@click.option("--no-wave", "-nw", "nw",
              help="Indicates that waveforms should not be produced",
              is_flag=True)
def simulate(testbench, nw):
    """Simulates the desired testbench."""
    flag = ""
    if not nw:
        # check if the waveform folder exists
        if not os.path.exists("./waveforms"):
            os.makedirs("./waveforms")

        # get the filename
        tb_name = Path("./waveforms", testbench.stem + ".vcd")

        # add the ghdl flag
        flag = f"--vcd={tb_name}"

    if ghdl_installed:
        click.echo("Runnning ghdl -e")
        subprocess.run([ghdl_bin, '-e', tb_name.stem])
        click.echo("Runnning ghdl -r")
        subprocess.run([ghdl_bin, '-r', tb_name.stem, flag, "--stop-time=1000us"])

    if not nw and gtkwave_installed:
        click.echo("opening gtkwave")
        subprocess.run([gtkwave_bin, tb_name])


cli.add_command(check)
cli.add_command(simulate)
