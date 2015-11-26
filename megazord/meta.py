import megazord
import re


def include_paths(name):
    database = {'python': ('python', 'includes', r"-I(.*?)(?=\s-I|$)"),
                'python3': ('python3', 'includes', r"-I(.*?)(?=\s-I|$)"),
                'root': ('root', 'incdir', None)}
    if name in database.keys():
        config = database[name]
        return get_config(*config)
    else:
        raise ValueError("{}-config is not supported by megazord. Invoke neccesary information manually.".format(name))


def get_tool_by_language(language):
    tool_by_language = {'c': ['clang', 'gcc'],
                            'c++': ['clang++', 'g++'],
                            'd': ['dmd'],
                            'object': ['clang++', 'g++', 'clang', 'gcc'],
                            'java': ['javac']}

    if language in tool_by_language:
        for tool_name in tool_by_language[language]:
            try:
                tool = get_tool_by_name(tool_name)
                if tool is not None:
                    return tool
            except:
                continue
    return None


def get_tool_by_name(name):
    tools_by_name = {'clang': megazord.ClangCompiler,
                         'clang++': megazord.ClangppCompiler,
                         'gcc': megazord.GccCompiler,
                         'g++': megazord.GppCompiler,
                         'dmd': megazord.DmdCompiler,
                         'javac': megazord.JavaCompiler,
                         'jar': megazord.JarTool}
    if name in tools_by_name.keys():
        return tools_by_name[name]()
    return None


def get_config(name, arg, r=None):
    result = megazord.system.call("{}-config".format(name), "--{}".format(arg))[:-1].decode("utf-8")
    if r is not None:
        result = re.findall(r, result)
    else:
        result = [result]
    return result


def get_default_includies(format):
    default_includies = {
        'clang++': ['/usr/local/include'],
        'clang': ['/usr/local/include'],
        'g++': ['/usr/local/include'],
        'gcc': ['/usr/local/include'],
    }
    if format in default_includies:
        return default_includies[format]
    return []


def get_default_libraries(format):
    default_libraries = {
    }
    if format in default_libraries:
        return default_libraries[format]
    return []


def get_default_output_format_for_language(language):
    default_formats = {
        'c++': '.a',
        'c': '.a',
        'd': '.a',
        'java': '.class',
        'object': '.a'
    }
    if language in default_formats:
        return default_formats[language]
    return ''


def get_language_by(extensions):
    languages_by_extension = {'.c': 'c',
                              '.cpp': 'c++',
                              '.java': 'java',
                              '.d': 'd',
                              '.o': 'object'}
    used_languages = set(
        map(lambda x: languages_by_extension[x] if x in languages_by_extension else 'unknown', extensions))
    if 'c' in used_languages and 'c++' in used_languages:
        used_languages.remove('c')
    return list(used_languages)


def library(name):
    database = {'python': ('python', 'libs', r"-l(.*?)(?=\s-|$)"),
                'python3': ('python3', 'libs', r"-l(.*?)(?=\s-|$)"),
                'root': ('root', 'libs', r"-l(.*?)(?=\s-|$)")}
    if name in database.keys():
        config = database[name]
        return get_config(*config)
    else:
        raise ValueError("{}-config is not supported by megazord. Invoke neccesary information manually.".format(name))


def library_paths(name):
    database = {'python': ('python', 'ldflags', r"-L(.*?)(?=\s-l|$)"),
                'python3': ('python3', 'ldflags', r"-L(.*?)(?=\s-l|$)"),
                'root': ('root', 'libdir', None)}
    if name in database.keys():
        config = database[name]
        return get_config(*config)
    else:
        raise ValueError("{}-config is not supported by megazord. Invoke neccesary information manually.".format(name))