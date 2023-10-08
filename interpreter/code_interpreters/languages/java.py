import tempfile
import os
from ..base_code_interpreter import BaseCodeInterpreter
from subprocess import STDOUT, Popen, PIPE
import io
import pexpect

class Java(BaseCodeInterpreter):
    file_extension = "java"
    proper_name = "Java"

    def __init__(self):
        super().__init__()

    def run(self, code):
        # Create a temporary HTML file with the content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".java") as f:
            f.write(code.encode())
        
        class ByteToTextWrapper(io.StringIO):
            def write(self, b):
                # decode bytes to string before writing
                return super().write(b.decode())

        logfile = ByteToTextWrapper()
        child = pexpect.spawn('bash -c \''+"java "+os.path.realpath(f.name)+'\'')
        child.logfile_read = logfile
        child.interact()
        interaction_log = logfile.getvalue()
        os.remove(os.path.realpath(f.name))


        yield {"output": interaction_log}