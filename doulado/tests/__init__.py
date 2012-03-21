from mock import patch
import unittest
import functools
import stuf


def no_mock(method):
    @functools.wraps(method)
    def inner(*args):
        return method(args[0])
    return inner
    

@patch('doulado.devinst.devinstall')
class TestDevinstConfigAndInit(unittest.TestCase):

    def test_devinst_hookedup(self, di):
        self.di = di
        from doulado import script
        di.return_value = True
        self.true_or_wat(script.main, argv=['devinst'])

    def test_devinst_gets_default_deps(self, di):
        from doulado import script
        di.return_value = True
        self.true_or_wat(script.main, argv=['devinst'])
        assert len(di.mock_calls) == 1, 'devinst called %s time' %len(di.mock_calls)
        deps = di.call_args[0][0]
        assert 'bambino' in deps 
        assert deps['bambino'].startswith('git@'), deps['bambino']

    def true_or_wat(self, call, *args, **kwargs):
        out = call(*args, **kwargs)
        assert out is True, "%s, expected True"

    @no_mock
    def test_devinst_gets_readonly_deps(self):
        from doulado import script
        di = script.devinstall
        di.configure_mock(return_value=True)
        args = stuf.fixedstuf(config='egg:doulado#doulado/devinst.yml',
                              read_only=True)
        self.true_or_wat(script.devinst, args)
        deps = stuf.fixedstuf(di.call_args[0][0])
        assert 'bambino' in deps 
        assert deps['bambino'].startswith('git://'), deps.bambino


def test_deploy():
    from doulado import script
    args = stuf.stuf()
    assert script.deploy(args)

def test_create():
    from doulado import script
    args = stuf.stuf()
    assert script.create(args)
        
