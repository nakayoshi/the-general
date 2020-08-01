from logic.echo import EchoImpl

sample_word = "WORD"

def test_echo():
    result = EchoImpl.echo(sample_word)
    assert result == sample_word


def test_echo_reversed():
    result = EchoImpl.echo_reversed(sample_word)
    assert result == sample_word[::-1]
