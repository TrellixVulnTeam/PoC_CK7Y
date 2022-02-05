from server.requestInterface import RequestInterface


class WorkingHoursRequest(RequestInterface):
    def __init__(self):
        self.project = None
        self.fromdate = None
        self.todate = None

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
        if prev_statement is None:
            if input_statement.find("progetto", 0, len(input_statement)) > -1:
                words = input_statement.split()
                self.project = words[words.index("progetto") + 1]
                """Handle case where project isn't there"""
            else:
                return "A quale progetto ti stai riferendo?"

    def isReady(self):
        if self.project is not None:
            return True

        return False

    def parseResult(self):
        1
