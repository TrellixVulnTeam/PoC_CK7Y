import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from server.utils.ChatterBotApiKey import ChatterBotApiKey
from chatterbot.ext.django_chatterbot import settings


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    chatterbot = ChatterBotApiKey(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'Non è stato specificato nessun testo!'
                ]
            }, status=400)

        if request.headers["Authorization"] is not None:
            apiKey = request.headers["Authorization"]
        else:
            apiKey = None

        response = self.chatterbot.get_response(apiKey, input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """

        return JsonResponse({
            'name': self.chatterbot.name,
            'text': "Ciao! Io sono Alfredo, il tuo assistente. Se hai bisogno di aiuto scrivimi \"farmacista\" :)",
        }, status=200)
