#!./env/bin/python

from sys import argv, stderr, stdout
from subprocess import check_output, CalledProcessError
from io import BytesIO

from elftools.elf.elffile import ELFFile
from elftools.dwarf.dwarfinfo import DWARFInfo
from elftools.dwarf.compileunit import CompileUnit
from elftools.dwarf.die import DIE

def main(filename):
    elf = _get_elf_file(filename)

    if (elf is None):
        return

    dwarf_info = elf.get_dwarf_info()

    for CU in dwarf_info.iter_CUs():
        for DIE in CU.iter_DIEs():
            if (DIE.tag == 'DW_TAG_structure_type'):
                name = str(DIE.attributes['DW_AT_name'].value, 'utf-8')
                size = DIE.attributes['DW_AT_byte_size'].value
                print(f"struct {name}:\t\t\t({size})")
                parse_struct_and_children(DIE, CU, 1)
    
    elf.stream.close()


def parse_struct_and_children(struct, CU, depth): 
    if (struct.has_children):
        for member in struct.iter_children():
            tabs = '    ' * depth
            name = str(member.attributes['DW_AT_name'].value, 'utf-8')
            if ((base_type := _get_base_type(member, CU)) != None):
                base = str(base_type.attributes['DW_AT_name'].value, 'utf-8')
                size = base_type.attributes['DW_AT_byte_size'].value
                is_struct = base_type.tag == 'DW_TAG_structure_type'
                print(f"{tabs}{'struct ' if is_struct else ''}{base} {name}\t\t\t{size}")
            else:
                print(f"Weird case here!")
            parse_struct_and_children(member, CU, depth + 1)

def _get_base_type(die, CU):
    if 'DW_AT_type' in die.attributes:
        type = die.attributes['DW_AT_type']
        if (type.form == 'DW_FORM_ref4'):
            return CU.get_DIE_from_refaddr(type.value)

def _get_elf_file(filename):
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
    if (len(argv) > 2):
        print('Please specify only 1 file', file=stderr)
    elif (len(argv) == 1):
        print('File is not specified', file=stderr)
    else:
        filename = argv[1]
        main(filename)
    
