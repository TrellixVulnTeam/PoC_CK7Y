class RequestInterface:
    def isReady(self):
        """Check if the object is ready for the request"""
        pass

    def parseUserInput(self, input_statement, prev_statement):
        """Parse user input to find out if new infos are available"""
        pass

    def parseResult(self):
        """Parse the JSON result of the HTTP Request"""
        pass
