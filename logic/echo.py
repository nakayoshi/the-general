class EchoImpl:

    @classmethod
    def echo(cls, text: str):
        return text

    @classmethod
    def echo_reversed(cls, text: str):
        return text[::-1]
