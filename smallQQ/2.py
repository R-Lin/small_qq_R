def test(**args):
    print args
    for item in args:
        print item

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
test(asd='123')
test(color="red", bold=False)
