# Functions with variable number of args
# https://docs.python.org/3.5/tutorial/controlflow.html

def Confirm(prompt, retries=4, complaint='yes or no, please!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False

        # retries = retries - 1
        retries -= 1
        if retries < 0:
            raise OSError('uncooperative user')
        print(complaint)


ans = Confirm("Are you married? ", 2)

if ans:
    print("That's the way to go~")
else:
    print("What are you waiting for? huhu")
    