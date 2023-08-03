import os
import re
from glob import glob
import textwrap
import dataclasses
from typing import Generator, List, Tuple
from contextlib import contextmanager


@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


@dataclasses.dataclass
class CPPVar:
    type: str = 'void'
    name: str = None
    content: str = None
    def to_string(self, subelem=False):
        if subelem:
            return f"  {self.type} {self.name}"
        else:
            return f"  cdef {self.type} {self.name}"


@dataclasses.dataclass
class CPPElement:
    type: str = 'void'
    name: str = None
    content: List[str] = dataclasses.field(default_factory=list)
    def to_string(self, subelem=False):
        wrapper = textwrap.TextWrapper(width=80, initial_indent='  ', subsequent_indent='    ', break_long_words=False)
        # string = textwrap.fill(, initial_indent='  ', subsequent_indent='    ')
        hacky = [s.replace(" ", "$") for s in self.content]

        if subelem:
            string = '\n'.join(wrapper.wrap(text=f"{self.type} {self.name}({', '.join(hacky)})".strip()))
            if self.type == '':
                string = string + " except +"
        else:
            string = '\n'.join(wrapper.wrap(text=f"cdef {self.type} {self.name}({', '.join(hacky)})".strip()))
        return string.replace("$", " ")



@dataclasses.dataclass
class CPPClass:
    type: str = 'class'
    name: str = None
    content: List[CPPElement] = dataclasses.field(default_factory=list)
    def to_string(self):
        head = f'  cdef cppclass {self.name}:'
        string = ''
        if self.content:
            for el in self.content:
                # if type(el) is CPPElement:
                string = string + '\n' + el.to_string(subelem=True)
        else:
            string = string + '\n  pass'
        return head + string.replace('\n', '\n  ')

def print_header(hand:str) -> str:
    return f'''\
# File: {hand}.pxd
# distutils: language = c++
# cython: language_level=3


""" ----------------------------------------------------------------------------
C++ Source Files
---------------------------------------------------------------------------- """

'''
def print_end_src():
    return '''\

""" ----------------------------------------------------------------------------
End of Source Files
---------------------------------------------------------------------------- """

'''

def print_headers_guard():
    return '''\

# ------------------------------------------------------------------------------
# C++ Header files + exported definitions
# ------------------------------------------------------------------------------

'''

def print_cppsrc(src:str):
    return f'''\
cdef extern from "{src}":
  pass
'''


def main(file:str = "src/cpp/constitutive/hog_double_2D.hpp", show_content:bool = True):
    # file = "src/cpp/hmodels/objective_template.hpp"
    # file = "src/cpp/constitutive/neohookean.hpp"
    # file = "src/cpp/constitutive/hog_2D.hpp"
    file = "/".join(file.split(os.sep))
    cpphome = 'cpp'
    cythonhome = 'cython/headers'
    folder, name = os.path.split(file)
    handle, _ = os.path.splitext(name)
    folder = folder.replace(cpphome, cythonhome)
    hpp = file
    cpp = hpp.replace(".hpp", ".cpp")
    cython = os.path.join(folder, handle+".pxd")

    # if os.path.isfile(cython):
    #     hpptime = os.path.getmtime(hpp)
    #     cythontime = os.path.getmtime(cython)
    #     if (cythontime > hpptime):
    #         return
    # handle = hpp.with_suffix("")
    # cpp = hpp.with_suffix(".cpp")
    # cython = hpp.with_suffix(".pxd")
    print(hpp)
    print(cpp)
    print(cython)
    includes = list()
    code = list()
    namespace = None
    content = list()
    with open(hpp, 'r') as fin:
        raw = fin.read().split("\n")

    raw = [s for s in raw if not(s.startswith('#define'))]
    raw = [s.strip() for sd in raw for s in re.split(r'(?=//)', sd) if s != '']
    # print(data, '\n')
    raw = [s for s in raw if not(s.startswith("//"))]

    if raw[0].startswith("#pragma"):
        raw = raw[1:]
    while raw != []:
        if raw[0].startswith("#include"):
            line = raw[0].split()
            if line[1].startswith('"') and line[1].endswith('"'):
                string = os.path.join(folder, line[1].replace('"',''))
                string, _ = os.path.splitext(os.path.normpath(string))
                includes.append(".".join(string.split(os.sep)))
            raw = raw[1:]
        elif raw[0].startswith("namespace"):
            line = raw[0].split()
            namespace = line[1]
            if line[-1] != "{":
                if raw[1].startswith("{"):
                    raw = raw[1:]
                else:
                    raise ValueError("Start of Namespace scope not found!")
            if raw[-1] != "}":
                raise ValueError("Namespace scope did not end!")
            raw = raw[1:-1]
        else:
            code.append(raw[0])
            raw = raw[1:]
    data = " ".join(code).strip()

    if os.path.isfile(cpp):
        with open(cpp, 'r') as fin:
            cppa = fin.read().split("\n")
        cppa = [s for s in cppa if not(s.startswith('#define'))]
        cppa = [s.strip() for sd in cppa for s in re.split(r'(?=//)', sd) if s != '']
        cppa = [s for s in cppa if not(s.startswith("//"))]
        while cppa != []:
            if cppa[0].startswith("#include"):
                line = cppa[0].split()
                if line[1].startswith('"') and line[1].endswith('"'):
                    _, string = os.path.split(line[1].replace('"','').strip())
                    string, _ = os.path.splitext(string)
                    if string != handle:
                        string = os.path.join(folder, line[1].replace('"',''))
                        string, _ = os.path.splitext(os.path.normpath(string))
                        includes.append(".".join(string.split(os.sep)))
            cppa = cppa[1:]
    includes = list(set(includes))
    for s in includes:
        print(s)
    # print(namespace)

    not_end = not(data.strip() == "")
    while not_end:
        # print(data)
        not_end, elem, data = get_content(data)
        if elem is not None:
            content.extend(elem)
    os.makedirs(os.path.dirname(cython), exist_ok=True)
    with open(cython, 'w') as fout:
        fout.write(print_header(handle))
        for s in includes:
            fout.write(f'cimport {s}\n')
        fout.write('\n')
        if os.path.isfile(cpp):
            fout.write(print_cppsrc(cpp))
        fout.write(print_end_src())
        fout.write(print_headers_guard())
        if namespace is None:
            fout.write(f'cdef extern from "{hpp}":')
        else:
            fout.write(f'cdef extern from "{hpp}" namespace "{namespace}":\n')
        if show_content and (content != []):
            for c in content:
                fout.write(c.to_string())
                fout.write('\n\n')
        else:
            fout.write("\n  pass")

def get_content(input:str) -> Tuple[bool, CPPElement, str]:
    data = input
    # print(data, '\n')
    if data.startswith('double'):
        id, elem = construct_function(data, 'double')
    elif data.startswith('int'):
        id, elem = construct_function(data, 'int')
    elif data.startswith('void'):
        id, elem = construct_function(data, 'void')
    elif data.startswith('class'):
        id, elem = construct_class(data)
    elif data.startswith('template'):
        id   = data.find('>')
        res  = data[id+1:].strip()
        if res.startswith('int'):
            id   = data.find(';')
            elem = None
        elif res.startswith('double'):
            id   = data.find(';')
            elem = None
        elif res.startswith('void'):
            id   = data.find(';')
            elem = None
        elif res.startswith('class'):
            idx  = data.find('{')
            id   = find_context_end(data, idx)
            elem = None
        else:
            raise ValueError('Attempting to resolve template failed')
    elif data.startswith('typedef'):
        id   = data.find(';')
        elem = None
    elif data.startswith('extern const'):
        id   = data.find(';')
        elem = None
    else:
        raise ValueError(f"Type {data[:30]} not recognized")
    return not(id+1>=len(input.strip())), elem, input[id+1:].strip()


def find_context_end(data:str, istart:int):
    count = 1
    iend = istart + 1
    for _ in range(istart + 1, len(data)):
        if count == 0:
            break
        elif data[iend] == '{':
            count = count + 1
        elif data[iend] == '}':
            count = count - 1
        iend = iend + 1
    return iend


def construct_class(input:str, type:str='class') -> Tuple[int, CPPClass]:
    cls = CPPClass(type)
    sp_start = input[5:].strip().find(' ')
    cl_start = input[5:].strip().find(':')
    content = list()
    if cl_start == -1:
        cls.name = input[5:].strip()[:sp_start].strip()
    elif sp_start < cl_start:
        cls.name = input[5:].strip()[:sp_start].strip()
    elif sp_start > cl_start:
        cls.name = input[5:].strip()[:cl_start].strip()
    else:
        raise ValueError('class name not found')
    istart = input.find('{')
    iend = find_context_end(input, istart)
    data = input[istart + 1:iend-1]
    has_public = data.find('public:')
    has_private = data.find('private:')
    match [has_private, has_public]:
        case [-1, -1]:
            pass
        case [-1, _]:
            data = data[has_public+7:].strip()
        case [_, -1]:
            return iend, None
        case [x,y] if y > x:
            data = data[has_public+7:].strip()
        case [x,y] if x > y:
            data = data[has_public+7:has_private].strip()
    not_end = True
    while not_end:
        not_end, elem, data = get_class_member(data, cls.name)
        if elem is not None:
            cls.content.extend(elem)
    return iend, [cls]

def get_class_member(input:str, cls:str) -> Tuple[bool, List[CPPElement|CPPVar]|None, str]:
    data = input.strip()
    if data.startswith(cls):
        id, elem = construct_function(data, '')
    elif data.startswith('~'+cls):
        id, _ = construct_function(data, '')
        elem = None
    elif data.startswith('double'):
        id, elem = construct_function(data, 'double')
    elif data.startswith('int'):
        id, elem = construct_function(data, 'int')
    elif data.startswith('void'):
        id, elem = construct_function(data, 'void')
    elif data.startswith('template'):
        id   = data.find(';')
        elem = None
    elif data.startswith('typedef'):
        id   = data.find(';')
        elem = None
    elif data.startswith('const'):
        id   = data.find(';')
        elem = None
    else:
        id   = data.find(';')
        elem = None
        print(f"Warn: Type {data[:10]} not recognized")
    return not(id + 1>=len(input)), elem, data[id+1:].strip()
    # return False, None, input


def construct_function(input:str, type:str='double') -> Tuple[bool, List[CPPElement|CPPVar]|None]:
    function_seperator = re.compile(r";|{};|{}")
    matched_obj = function_seperator.search(input)
    # id   = input.find(';')
    id = matched_obj.end() - 1
    if matched_obj.group(0) == r";":
        data = input[len(type):id].strip()
    elif matched_obj.group(0) == r"{}":
        data = input[len(type):id-1].strip()
    elif matched_obj.group(0) == r"{};":
        data = input[len(type):id-2].strip()
    if data.endswith(')') or data.endswith('{}'):
        name, content, *_ = re.split(r"[()]", data)
        elem = CPPElement(type)
        elem.name = name.strip()
        content_check = False
        if content != '':
            content = content.split(", ")
            for c in content:
                if c.startswith('const'):
                    _, t, v = c.split()
                # elif c.startswith('extern const'):
                #     _, _, t, v = c.split()
                # elif c.startswith('extern'):
                #     _, t, v = c.split()
                else:
                    t, v = c.split()
                if t in ['int', 'double']:
                    if v.endswith("]"):
                        v = re.split(r"[\[\]]",v)[0]
                        t = t+"[]"
                    elem.content.append(t + " " + v)
                else:
                    content_check = True
        if content_check:
            elem = None
        else:
            elem = [elem]
    else:
        # if data.endswith(']'):
        #     istart = data.find('[')
        #     elem = CPPVar(type+data[istart:])
        #     elem.name = data[:istart]
        # else:
        content = data.split(", ")
        elem = [CPPVar(type, val) for val in content]
    return id + 1, elem


def get_include(data:Generator[str, None, None]) -> CPPElement:
    elem = CPPElement("include")
    item = data.__next__()
    name = os.path.basename(item)
    name, _ = os.path.splitext(name)
    elem.name = name
    elem.content.append(item)
    return elem


if __name__=="__main__":
    # main(show_content=True)

    with cwd(os.path.dirname(__file__)):
        # files = glob('src/cpp/constitutive/*.hpp')
        # for fin in files:
        #     print(f"Working on {fin}")
        #     main(fin)
        # files = glob('src/cpp/hmodels/*.hpp')
        # for fin in files:
        #     print(f"Working on {fin}")
        #     main(fin)
        # files = glob('src/cpp/ensemble_model/*.hpp')
        # for fin in files:
        #     print(f"Working on {fin}")
        #     main(fin)
        # files = glob('src/cpp/kinematics/*.hpp')
        # for fin in files:
        #     print(f"Working on {fin}")
        #     main(fin)
        files = glob('cpp/*/*.hpp')
        for fin in files:
            print(f"Working on {fin}")
            main(fin)
        files = glob('cpp/*.hpp')
        for fin in files:
            print(f"Working on {fin}")
            main(fin)
    # files = glob('src/cpp/kernel_density_estimation/*.hpp')
    # for fin in files:
    #     print(f"Working on {fin}")
    #     main(fin)