import os
import re
import subprocess

import megazord

# This is a generic class for any tools.
# It consists of several functions and ArgBuilder class
class GenericTool:
    def __init__(self, path):
        if megazord.system.which(path) is not None:
            self.path = path
        else:
            raise FileNotFoundError("{} was not found".format(path))

class GenericCompiler(GenericTool):
    # The main aim of ArgBuilder is hiding details of flags appending to the calling of
    # the tool
    class ArgBuilder:
        def __str__(self):
            return ' '.join(self.flags)

        def __repr__(self):
            return ' '.join(self.flags)

        def __init__(self):
            self.flags = []

        def append(self, *flags):
            if isinstance(flags, list) or isinstance(flags, tuple):
                self.flags.extend(flags)
            else:
                self.flags.append(flags)
            return self

        def build(self):
            return self.flags

    def __init__(self, path):
        super(GenericCompiler, self).__init__(path)

    def prepare_args(self, target):
        args = GenericCompiler.ArgBuilder()
        return args

    def compile(self, target):
        args = self.prepare_args(target)
        megazord.system.call(self.path, *args.build())


class CCompiler(GenericCompiler):
    class CArgBuilder(GenericCompiler.ArgBuilder):
        def add_include_path(self, path):
            self.append('-I{}'.format(path))
            return self

        def add_include(self, name):
            self.append('-i{}'.format(name))
            return self

        def add_library_path(self, path):
            self.append('-L{}'.format(path))
            return self

        def add_library(self, name):
            self.append('-l{}'.format(name))
            return self

        def set_output_name(self, name):
            self.append('-o{}'.format(name))
            return self

        def set_std(self, std='c++11'):
            self.append('-std={}'.format(std))
            return self

        def set_target(self, sources, output_format):
            if output_format == '.o':
                self.append('-c')
            elif output_format in ['.so', '.dylib']:
                self.append('-shared')
            self.append(*sources)
            return self

        def build(self):
            return self.flags

    def prepare_args(self, target):
        args = self.CArgBuilder()
        args.set_std()
        args.set_target(target.get_sources(), target.output_format)
        compiled_lib_paths = []
        for dependency in target.dependencies:
            if dependency.output_format == '.o':
                args.append(dependency.output)
            elif dependency.output_format in ['.so', '.dylib']:
                compiled_lib_paths.append(dependency.output_dir)
                if dependency.output_name.startswith('lib'):
                    args.add_library(dependency.output_name[3:])
                else:
                    args.add_library(dependency.output_name)
            else:
                raise ValueError("{} cannot be processed as dependency for {}. "
                                 "Did you forget to set output format for dependency to '.o'?".format(
                    dependency.sources))

        for compiled_lib_path in set(compiled_lib_paths):
            args.add_library_path(compiled_lib_path)

        args.set_output_name(target.output_dir + target.output)
        if target.output_format in ['.so', '.dylib'] and not target.output.startswith('lib'):
            megazord.system.create_symlink(target.output_dir + target.output, target.output_dir + 'lib' + target.output)

        args.append('-O{}'.format(target.optimization_level))
        for library_path in target.library_paths:
            args.add_library_path(library_path)
        for include_path in target.include_paths:
            args.add_include_path(include_path)
        for library in target.libraries:
            args.add_library(library)
        for include in target.includies:
            args.add_include(include)
        return args

class DmdCompiler(GenericCompiler):
    def __init__(self, path='dmd'):
        super(DmdCompiler, self).__init__(path)


class GccCompiler(CCompiler):
    def __init__(self, path='gcc'):
        super(GccCompiler, self).__init__(path)


class GppCompiler(CCompiler):
    def __init__(self, path='g++'):
        super(GppCompiler, self).__init__(path)


class ClangCompiler(CCompiler):
    def __init__(self, path='clang'):
        super(ClangCompiler, self).__init__(path)


class ClangppCompiler(CCompiler):
    def __init__(self, path='clang++'):
        super(ClangppCompiler, self).__init__(path)


class JarTool(GenericTool):
    class JarArgBuilder(GenericCompiler.ArgBuilder):
        def set_output_name(self, name):
            self.append('{}'.format(name))
            return self

        def set_target(self, sources):
            self.append(*sources)
            return self

    def __init__(self, path='jar'):
        super(JarTool, self).__init__(path)

    def prepare_args(self, output_name, sources, entry_point=None):
        args = self.JarArgBuilder()
        if entry_point is None:
            args.append('cvf')
        else:
            args.append('cfe')
        args.set_output_name(output_name)
        if entry_point is not None:
            args.append(entry_point)
        args.set_target(sources)
        return args

    def collect_classes(self, target):
        all_class_files = [f for f in os.listdir(target.output_dir) if
                           os.path.isfile(os.path.join(target.output_dir, f))]
        related_class_files = []
        sources_names = set()
        for sources_name in target.sources_names:
            sources_names.add(os.path.basename(sources_name))
        for cf in all_class_files:
            if not cf.endswith('.class'):
                continue
            cf_crop = re.match("(\w+)[\$\.$]", cf).group(1)
            if cf_crop in sources_names:
                related_class_files.append(cf)
        return related_class_files

    def run(self, target, name):
        tmp_file = megazord.system.mkstemp(target.output_dir)
        print(tmp_file)
        if not target.compiled:
            target.assembly()
        classes = self.collect_classes(target)
        args = self.prepare_args(tmp_file, classes, target.entry_point)
        old_wd = megazord.system.getwd()
        megazord.system.setwd(target.output_dir)
        megazord.system.call(self.path, *args.build())
        megazord.system.setwd(old_wd)
        megazord.system.move(tmp_file, name)

class JavaCompiler(GenericCompiler):
    class JavaArgBuilder(GenericCompiler.ArgBuilder):
        def add_classpath(self, classpath):
            self.append('-cp', classpath)
            return self

        def set_output_dir(self, dir):
            self.append('-d', dir)
            return self

        def set_std(self):
            return self

        def set_target(self, sources):
            self.append(*sources)
            return self

    def __init__(self, path="javac"):
        super(JavaCompiler, self).__init__(path)

    def prepare_args(self, target):
        args = self.JavaArgBuilder()
        args.set_target(target.get_sources())
        args.set_output_dir(target.output_dir)
        dependencies = target.libraries
        for dependency in target.dependencies:
            if dependency.output_format != '.jar':
                raise ValueError("The only resolvable dependencies is .jar ones")
            dependencies.append(dependency.output_dir + dependency.output)
        if len(dependencies) > 0:
            args.add_classpath(':'.join(dependencies))
        return args
