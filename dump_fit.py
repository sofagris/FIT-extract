import libfdt
import sys

USE_COLORS = sys.stdout.isatty()

# ANSI escape codes for colors
if USE_COLORS:
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'invert': '\033[7m',
        'hidden': '\033[8m'
    }
else:
    COLORS = {key: '' for key in ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'reset']} # noqa E501

STARTBRACKET = '{'
ENDBRACKET = '}'


def format_prop_value(prop):
    try:
        # Try to interpret as a string list
        value = prop.as_stringlist()
        return ', '.join(value)
    except (libfdt.FdtException, ValueError):
        pass
    try:
        # Try to interpret as a list of uint32 values
        value = prop.as_uint32_list()
        return ', '.join(hex(v) for v in value)
    except (libfdt.FdtException, ValueError):
        pass
    try:
        # Return the data as a hexadecimal string
        return prop.data.hex()
    except (libfdt.FdtException, ValueError, AttributeError):
        pass
    # If everything else fails, return the length of the data
    try:
        data_length = len(prop.data)
        return f"<{data_length} bytes>"
    except AttributeError:
        return "<unknown size>"


def print_node(fdt, offset, indent=''):
    node_name = fdt.get_name(offset)
    # Colorize node name
    print(f"{indent}{COLORS['blue']}{node_name}{COLORS['reset']} {COLORS['white']}{STARTBRACKET}{COLORS['reset']}") # noqa E501

    # Print properties
    try:
        prop_offset = fdt.first_property_offset(offset)
    except libfdt.FdtException as e: # noqa F841
        prop_offset = -1

    while prop_offset >= 0:
        prop = fdt.get_property_by_offset(prop_offset)
        prop_name = prop.name

        if prop_name == 'data':
            try:
                data_length = len(prop.data)
            except AttributeError:
                data_length = '<unknown size>'
            prop_value = f"<{data_length} bytes>"
        else:
            prop_value = format_prop_value(prop)

        # Colorize property names and values
        print(f"{indent}  {COLORS['green']}{prop_name}{COLORS['reset']} = {COLORS['yellow']}{repr(prop_value)}{COLORS['reset']};") # noqa E501

        try:
            prop_offset = fdt.next_property_offset(prop_offset)
        except libfdt.FdtException as e: # noqa F841
            break  # Exit loop on error

    # Recurse into subnodes
    try:
        subnode_offset = fdt.first_subnode(offset)
    except libfdt.FdtException as e: # noqa F841
        subnode_offset = -1

    while subnode_offset >= 0:
        print_node(fdt, subnode_offset, indent + '  ')
        try:
            subnode_offset = fdt.next_subnode(subnode_offset)
        except libfdt.FdtException as e: # noqa F841
            break  # Exit loop on error

    # Colorize closing bracket
    print(f"{indent}{COLORS['white']}{ENDBRACKET}{COLORS['reset']}")


def dump_fit(fit_file_path):
    with open(fit_file_path, 'rb') as f:
        fit_data = f.read()

    # Create an FDT object
    fdt = libfdt.Fdt(fit_data)

    # Start from the root node
    root_offset = fdt.path_offset('/')
    print_node(fdt, root_offset)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dump_fit.py <fit_fil>")
        sys.exit(1)

    fit_file = sys.argv[1]
    dump_fit(fit_file)
