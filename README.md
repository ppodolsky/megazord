Simple Code Management System
-----------------------------

**Megazord** allows you to compile programs on different languages from Python program. Library provides you a
unified interface to manage all you code.

Currently supported features:
- Compilation C++, Java and D programs

Currently developing features:
- Deployment - create, name, move, run and delete your binaries
- Versioning control - simple interface to git repository gives you an opportunity to switch code versions by few commands.

## Conceptions

**mz.Target** is a compilation unit with all its dependencies. Configure it and then tell **assembly()**.

### Starting Example

#### 
```
import megazord as mz

hello = mz \
    .Target(["test/cpp/hello.cpp"],
            output="test/cpp/lib/libhello.so") \
    .add_support("root")
main = mz.Target('test/cpp/main.cpp',
                       output='test/cpp/bin/main.a')\
    .depends_on(hello)
main.assembly()

java_target = mz \
    .Target(['test/java/Solver.java', 'test/java/Board.java'],
            output='test/java/bin/',
            entry_point='Board') \
    .add_library('test/java/algs4.jar')
java_target.assembly()
jt = mz.JarTool()
jt.run(java_target, 'target.jar')
```