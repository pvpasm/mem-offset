import sys

from elftools.elf.elffile import ELFFile
from elftools.dwarf.dwarfinfo import DWARFInfo
from elftools.dwarf.compileunit import CompileUnit
from elftools.dwarf.die import DIE

def main():
    filename = sys.argv[1]

    with open(filename, 'rb') as stream:
        elf = ELFFile(stream)
        dwarf_info = elf.get_dwarf_info()

        for CU in dwarf_info.iter_CUs():
            for DIE in CU.iter_DIEs():
                if (DIE.tag == 'DW_TAG_structure_type' or DIE.tag == 'DW_TAG_member'):
                    print(DIE)

if __name__ == '__main__':
    main()
    
