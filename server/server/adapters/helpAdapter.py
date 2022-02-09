from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
import re


class HelpAdapter(LogicAdapter):
    helpResponse = "Per sapere le ore che hai registrato puoi mandarmi un messaggio del tipo: \"Quante ore ho " \
                   "consuntivato nel progetto ***?\" Se ti interessa un particolare arco temporale puoi aggiungerlo " \
                   "alla richiesta indicando \"dal gg/mm/aaaa al gg/mm/aaaa\""

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.adapter = None

    def can_process(self, statement):
        if self.adapter is not None:
            return True

        words = ['aiuto', 'farmacista', 'help', 'come si fa', 'come funziona']

        sanitizedWords = re.sub("[^a-zA-Z0-9 \n./]", ' ', statement.text.lower()).split()

        if not any(x in sanitizedWords for x in words):
            return False

        return True

    def process(self, input_statement, additional_response_selection_parameters):
        response_statement = Statement(self.helpResponse)
        response_statement.confidence = 1

        return response_statement
