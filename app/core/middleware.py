from time import sleep 

class LaggyMiddleware(object):
    def process_request(self, request):
        if '/api/' in request.path:
            sleep(1.5)
