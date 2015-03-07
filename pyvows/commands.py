import subprocess
import distutils.cmd
import distutils.log


class VowsCommand(distutils.cmd.Command):
    """Custom command to run pyvows vows"""

    description = 'Run pyvows tests'
    user_options = [
        ('pyvows-path=', None, 'Directory or file to search for vows.'),
        ('pyvows-pattern=', None, 'Pattern for filtering vows files'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        self.pyvows_pattern = '*_vows.py'
        self.pyvows_path = 'tests/'

    def finalize_options(self):
        pass

    def run(self):
        cmd = 'pyvows -p "{pattern}" {path}'.format(
            path=self.pyvows_path,
            pattern=self.pyvows_pattern
        )
        self.announce('Executing ' + cmd, level=distutils.log.INFO)
        subprocess.call(cmd, shell=True)
