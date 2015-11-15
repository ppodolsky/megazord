import megazord

hello = megazord \
    .Target(["test/cpp/hello.cpp"],
            output="test/cpp/lib/libhello.so") \
    .add_support("root")
main = megazord.Target('test/cpp/main.cpp',
                       output='test/cpp/bin/main.a')\
    .depends_on(hello)
main.assembly()
main.deploy_to('./', exclude=hello)

java_target = megazord \
    .Target(['test/java/Solver.java', 'test/java/Board.java'],
            output='test/java/bin/',
            entry_point='Board') \
    .add_library('test/java/algs4.jar')
java_target.assembly()
jt = megazord.JarTool()
jt.run(java_target, 'target.jar')
