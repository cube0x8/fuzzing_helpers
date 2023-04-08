# This is a sample Python script.

import logging
import os
import re
import tempfile

OUTDIR = "/tmp/linadump"
PID = "1308"
LAYOUT_FILE = "layout_memory"

"""

# dummy function for testing purposes
def get_proc_mapping():
    content = None
    with open("proc_mapping.txt", "r") as fp:
        content = fp.read()
    return content
"""


class GDBCommandErrorException(Exception):
    def __init__(self, command, exc):
        self.command = command
        self.msg = f"Cannot execute the gdb command \"{command}\""
        self.original_exc = exc
        self.proc_mapping_need_pid = False
        if str(exc) == "Can't determine the current process's PID: you must name one.":
            self.proc_mapping_need_pid = True


class ConfigurationError(Exception):
    pass


def execute_output(command):
    # create temporary file for the output
    filename = os.getenv('HOME') + os.sep + 'gdb_output_' + str(os.getpid())
    output = ""

    # execute command
    try:
        output = gdb.execute(command, to_string=True)
    except gdb.MemoryError as exc:
        raise GDBCommandErrorException(command, exc)
    except gdb.error as exc:
        raise GDBCommandErrorException(command, exc)
    except BaseException as exc:
        print(f"Unexpected error: {str(exc)}")

    output = output.splitlines()

    return output


def process_mappings(regex=''):
    mappings = list()

    ipm_command = 'info proc mapping '
    # get process mappings
    if PID is not None:
        ipm_command += PID

    print(f"Executing gdb command: {ipm_command}")
    output = execute_output(ipm_command)

    # parse processes mappings info
    for line in output:

        # only right lines
        if re.compile('^\s+0x[0-9a-f]+').search(line):
            field = re.compile('\s+').split(line)

            # provide the last field if not present (memory area name)
            if len(field) < 6:
                field.append('')

            # exclude memory areas that don't match the regexp
            if regex != '':
                if not re.search(regex, field[5]):
                    continue

            # add mapping info to the list
            mappings.append({
                'start': int(field[1], 16),
                'end': int(field[2], 16),
                'size': int(field[3], 16),
                'offset': int(field[4], 16),
                'objfile': field[5]
            })

    return mappings


if OUTDIR == "":
    raise(ConfigurationError(f"Please, define the OUTDIR variable with a valid directory."))

if not os.path.isdir(OUTDIR):
    raise(ConfigurationError(f"The specified output directory \"{OUTDIR}\" does not exist."))

layout_file_abs_path = OUTDIR + "/" + LAYOUT_FILE

print(f"Dumping process memory to directory {OUTDIR}")

fp = open(layout_file_abs_path, "w")
try:
    proc_map = process_mappings()
except GDBCommandErrorException as exc:
    if exc.proc_mapping_need_pid:
        raise ConfigurationError(f"{exc.command} command requires PID. Please initialize it.")
    else:
        raise ConfigurationError(f"Unhandled error while running: {exc.command}.")

print(f"Dumping {len(proc_map)} memory region(s). This might take awhile...")
for mapping in proc_map:
    dump_filename = tempfile.NamedTemporaryFile(dir=OUTDIR, prefix='dump_').name + ".bin"
    mapping["dump_filename"] = dump_filename
    dump_command = f"dump binary memory {dump_filename} " \
                   f"{mapping['start']} {mapping['end']}"

    print(f"Dumping memory region {mapping['start']} {mapping['end']} "
          f"of {mapping['size']} bytes to the file '{dump_filename}'")

    try:
        dump_result = execute_output(dump_command)
    except GDBCommandErrorException as e:
        print(f"The memory range {mapping['start']} {mapping['end']} ({mapping['objfile']}) cannot be dumped.\n"
              f"It won't be stored in the layout file.")
        continue

    # objfile can be empty. in that case, we replace it with the empty string (""),
    # so strtok() works properly
    if mapping["objfile"] == "":
        mapping["objfile"] = '""'

    fp.writelines(f"{mapping['start']},{mapping['end']},{mapping['size']},{mapping['offset']},{mapping['objfile']},"
                  f"{mapping['dump_filename']}\n")

print(f"Memory regions dump completed.")

fp.close()
print(f"Memory mapping layout stored in {layout_file_abs_path}")
