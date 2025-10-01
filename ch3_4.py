def say_hello():
    print("Hello World!")

def do_twice(f):
    f()
    f()

do_twice(say_hello)

#depenancy injection
#   Als je een databestand naar 2 plekken stuurt (bv: database.sql en postgres) kan je de volgende "comentaar" code gebruiken:
#       def save_to_everywhere(f)
#           f()
#           f()