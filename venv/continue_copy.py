import shutil

def continue_copy(source, dest):
    try:
        shutil.copy(source, dest)
    except FileNotFoundError as fe:
        print(fe)
        must_continue = input("Stop?")
        if must_continue.lower() == 'y':
            raise
    except shutil.SameFileError as se:
        pass

