import fileinput, sys, os, re

def io():
    files = [k for k in sys.argv[1:] if os.path.exists(k)]
    for iline in  fileinput.input(files, openhook=fileinput.hook_compressed):
        yield iline.decode('utf8')

re_i = re.compile(r'^[\d]+i$')
re_f = re.compile(r'^[\d]+\.[\d]+f$')
re_b = re.compile(r'^(True|False)$')

def convert(v):
    v = v.strip()

    try:
        if re_i.match(v):
            return int(v[:-1])
        elif re_f.match(v):
            return float(v[:-1])
        elif re_b.match(v):
            return bool(v)
        elif v == "None":
            return None
    except:
        pass

    return v

def now(func=None):
    re_arg = re.compile(r'\-\-([\w]+)=(.+)')

    func = func or sys.argv[1]
    func = getattr(sys.modules['__main__'], func)

    args = (re_arg.findall(k)[0] for k in sys.argv[1:] if re_arg.match(k))
    args = {k:convert(v) for k, v in args}
    return func(**args)
