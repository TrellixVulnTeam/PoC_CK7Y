from requests import Response
from server.requestInterface import RequestInterface
from datetime import datetime


class WorkingHoursRequest(RequestInterface):
    responseProjectMissing = "A quale progetto ti stai riferendo?"

    def __init__(self):
        self.project = None
        self.fromdate = None
        self.todate = None

    def parseUserInput(self, input_statement: str, prev_statement: str) -> str:
        if prev_statement is None:
            if input_statement.find("progetto", 0, len(input_statement)) > -1:
                words = input_statement.split()
                self.project = words[words.index("progetto") + 1]
                # handle case where project isn't there

                if set(input_statement.split()).intersection(set("dal")):
                    words = input_statement.split()
                    self.fromdate = datetime.strptime(words[words.index("dal") + 1], '%d/%m/%Y').strftime('%Y-%m-%d')

                    if set(input_statement.split()).intersection(set("al")):
                        words = input_statement.split()
                        self.todate = datetime.strptime(words[words.index("al") + 1], '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                return self.responseProjectMissing
        else:
            if prev_statement == self.responseProjectMissing:
                self.project = input_statement
                return "Eseguo azione!"

    def isReady(self) -> bool:
        if self.project is not None:
            return True

        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 200:
            strReturn = ""
            for record in response.json():
                date = datetime.strptime(record.get('date'), '%Y-%m-%d').date()
                strReturn += date.strftime('%d/%m/%Y') + '\n'
                strReturn += "\tLocalità: " + record.get('location', "non segnalata") + '\n'
                strReturn += "\tOre fatturate: " + str(record.get('billableHours', "non registrate")) + '\n'
                strReturn += "\tNote: " + record.get('note', "none") + '\n'
                strReturn += '\n\n'

            return strReturn
        elif response.status_code == 401:
            return "Non sei autorizzato ad accedere a questa risorsa. Per favore effettua il login al link ..."
        else:
            return "Il progetto che hai cercato non esiste"

