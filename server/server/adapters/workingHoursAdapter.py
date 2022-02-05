from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter
from server.workingHoursRequest import WorkingHoursRequest


class WorkingHoursAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.prev_statement = None
        self.adapter = None
        self.request = None

    def can_process(self, statement):
        if self.adapter is not None:
            return True

        hoursWords = ['ore', 'numero di ore']
        workWords = ['consuntivato', 'registrato', 'fatto', 'consuntivate', 'fatte']
        # projectWords = ['progetto']

        if not any(x in statement.text.split() for x in hoursWords):
            return False

        if not any(x in statement.text.split() for x in workWords):
            return False

        # if not any(x in statement.text.split() for x in projectWords):
        #    return False

        return True

    def process(self, input_statement, additional_response_selection_parameters):
        if self.adapter is None:
            self.adapter = "WorkingHoursAdapter"
            self.request = WorkingHoursRequest()
            self.prev_statement = None

        response = self.request.parseUserInput(input_statement.text, self.prev_statement)

        if self.request.isReady():
            response_statement = Statement("OK")
            response_statement.confidence = 0
        else:
            response_statement = Statement(response)
            response_statement.confidence = 0

        return response_statement
