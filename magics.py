from IPython.core.magic import register_line_cell_magic,register_cell_magic,register_line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

from IPython.core.getipython import get_ipython
shell = get_ipython()

def substitute_globals(content):
    from string import Template
    from collections import defaultdict
    return Template(content).substitute(defaultdict(str, **globals()))


@magic_arguments()
@argument('file', 
          type=str, 
          help='Input template file.')
@argument(
    "--output",
    "-o",
    default=None,
    help=("Output file where the rendered template will be written. Writes to console if not provided. "),
)
@argument(
    "--skip-preview",
    "-s",
    action='store_true',
    help=("Preview the rendered document before writing."),
)
@register_line_magic
def template(line):
    args = parse_argstring(template, line)
    with open(args.file, 'r') as f:        
        contents = substitute_globals(f.read())
        if args.output is None:
            print(contents)
            return
        
        if not args.skip_preview:
            payload = dict(
                source='set_next_input',
                text=(f'#%%writefile "{args.output}"\n' if args.output is not None else '')+contents,
                replace=False,
            )
            shell.payload_manager.write_payload(payload, single=True)
            return
        
        with open(args.output, 'w') as f:
            f.write(contents)
            print(f'Template rendered to {args.output}') 
