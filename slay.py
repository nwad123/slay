import click
import os
from pathlib import Path
import shutil
import subprocess
from typing import List

ghdl_bin = 'ghdl'
gtkwave_bin = 'gtkwave'

def is_installed(binary: str) -> bool:
    """Checks if a given binary is installed or not"""
    if not shutil.which(binary):
        click.echo(f"No candidate for {binary} found")
        return False
    else:
        return True

def get_src_files(*, path: Path = os.getcwd()) -> List[str]:
    """Returns a list of all the .vhd or .vhdl files in a directory"""
    vhdl_files: List[Path] = []

    # find all the VHDL files and append them along with their path to the list
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".vhd") or file.endswith(".vhdl"):
                vhdl_files.append(Path(os.path.join(root, file)))

    return vhdl_files

@click.group()
def cli():
    """Wrapper for GHDL and GTKwave to produce easy simulations and syntax checking."""

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
        files = get_src_files()

    click.echo(f"Analyzing file(s)...")
    for file in files:
        subprocess.run([ghdl_bin, '-s', "--work=work", file])

@click.command()
@click.argument("testbench",
                nargs=-1,
                type=click.Path(exists=True, path_type=Path))
@click.option("--no-wave", "-n", "no_wave",
              help="Indicates that waveforms should not be produced",
              is_flag=True)
def simulate(testbench, no_wave):
    """Simulates the desired testbench."""
    # get a list of the testbenches to run
    testbenches: List[Path] = []
    for tb in testbench:
        testbenches.append(tb)

    # perform analysis on all of the files
    testbenches_str: List[str] = []
    for tb in testbenches:
        testbenches_str.append(str(tb))

    sp_opts = [ghdl_bin, '-a', "--work=work"] + testbenches_str
    subprocess.run(sp_opts)

    # perform elaboration and simulation on each of the desired top level units
    for tb in testbenches:
        # elaboration
        sp_opts = [ghdl_bin, '-e', '--work=work', tb.stem]
        subprocess.run(sp_opts)

        # simulation
        if no_wave:
            sp_opts = [ghdl_bin, '-r', '--work=work', tb.stem, "--stop-time=100us"]
        else:
            sp_opts = [ghdl_bin, '-r', '--work=work', tb.stem, f'--vcd=./waveforms/{tb.stem}.vcd', "--stop-time=100us"]
        subprocess.run(sp_opts)

        # waveform viewer
        if not no_wave:
            click.echo("GTKWave Not implemented yet")

cli.add_command(check)
cli.add_command(simulate)
