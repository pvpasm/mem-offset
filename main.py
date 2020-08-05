from sys import argv, stderr, stdout
from subprocess import check_output, CalledProcessError
from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.dwarf.dwarfinfo import DWARFInfo
from elftools.dwarf.compileunit import CompileUnit
from elftools.dwarf.die import DIE

def main():
    elf = get_elf_file()

    if (elf is None):
        return
        

    dwarf_info = elf.get_dwarf_info()

    for CU in dwarf_info.iter_CUs():
        for DIE in CU.iter_DIEs():
            if (DIE.tag == 'DW_TAG_structure_type' or DIE.tag == 'DW_TAG_member'):
                print(DIE)
    
    elf.stream.close()

def get_elf_file():
    if (len(argv) > 2):
        print('Please specify only 1 file', file=stderr)
        return

    if (len(argv) == 1):
        print('File is not specified', file=stderr)
        return

    filename = argv[1]

    try:
        stream = _process_file(filename)
        return ELFFile(stream)
    except IOError:
        print('File not found', file=stderr)
        return
    except CalledProcessError:
        print('Compilation error', file=stderr)
        return
    except ValueError:
        print('Filetype is not supported', file=stderr)
        stream.close()
        return



def _process_file(filename):
    if (filename.split('.')[-1] == 'c'):
        output = check_output(['gcc', '-g', '-o', '/dev/stdout', filename])
        stream = BytesIO(output)
    else:
        stream = open(filename, 'rb')
    return stream

if __name__ == '__main__':
    main()
    
