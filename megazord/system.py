import platform
import os, errno
import subprocess
import tempfile
import shutil
import re

from .meta import *

def vectorizer(func):
    def vec_func(args):
        if isinstance(args, list):
            return list(map(func, args))
        else:
            return func(args)
    return vec_func

getwd = os.getcwd
exists = os.path.exists
abs_path = vectorizer(os.path.abspath)
move = os.rename
rename = os.rename
setwd = os.chdir
uname = os.uname().sysname.lower()

def call(cmd, *args):
    t = [cmd]
    t.extend(args)
    print("Run: {}".format(' '.join(t)))
    return subprocess.check_output(t)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def move(src, dst):
    if not isinstance(src, list): src = [src]
    if os.path.isdir(dst):
        if not dst.endswith('/'): dst += '/'
        for f in src:
            os.rename(f, dst + os.path.basename(f))
    elif len(src) == 1:
        os.rename(src[0], dst)
    else:
        raise ValueError("Don't know what to do")

def copy(src, dst):
    if not isinstance(src, list): src = [src]
    if os.path.isdir(dst):
        if not dst.endswith('/'): dst += '/'
        for f in src:
            shutil.copyfile(f, dst + os.path.basename(f))
    elif len(src) == 1:
        shutil.copy(src[0], dst)
    else:
        raise ValueError("Don't know what to do")


def rm(path):
    info('removing {} ...'.format(path), 2)
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def which(name):
    try:
        return subprocess.check_output(["which", name])[:-1].decode("utf-8")
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return None


def search(name, paths):
    for path in paths:
        compiler_path = path + name
        if os.path.isfile(compiler_path):
            return compiler_path
    return None


def mkdtemp(dir="."):
    r = tempfile.mkdtemp(dir=dir)
    info('creation temp directory {} ...'.format(r), 2)
    return r


def mkstemp(dir="."):
    r = tempfile.mkstemp(dir=dir)
    os.close(r[0])
    info('creation temp file {} ...'.format(r[1]), 2)
    return r[1]


def warning(text, *args):
    print("Warning: {}".format(text.format(args)))


def info(text, verbose=1, *args):
    if megazord.verbose >= verbose:
        print("Info: {}".format(text.format(args)))


def create_symlink(file, symlink):
    call("ln", "-sf", file, symlink)

