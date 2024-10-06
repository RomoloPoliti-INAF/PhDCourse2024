from newState import fPath, checkFile


def test_fPath():
    assert fPath('test.py') == './test.py'
    
def test_checkFile():
    assert checkFile(fPath('commandsTable.csv')) == True