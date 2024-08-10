import json
from wsgiref.simple_server import make_server
import datetime

def load_settings():
    with open("settings.json", 'r') as file:
        return json.load(file)
    
def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def logging(*args):
    print(get_datetime(), "[info] ", *args)

def get_request_body(environ):
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size) if request_body_size > 0 else b''
        return request_body.decode("utf-8")

def make_App(settings):
    def App(environ, start_response):
        path = environ["PATH_INFO"]
        request_method = environ["REQUEST_METHOD"]
        query_params = environ["QUERY_STRING"]
        output_filepath = settings["response_files"][path][request_method]

        logging(request_method, path)
        logging("query params:", query_params)
        logging("request body:", get_request_body(environ))

        status = "200 OK"
        headers = [("Content-type", "Application/json; charset=utf-8")]
        start_response(status, headers)
        with open(output_filepath) as rf:
            d = json.load(rf)
            body = [json.dumps(d).encode("utf-8")]
            logging("response body: ", d)
        return body
    return App

if __name__ == "__main__":
    settings = load_settings()
    port = settings["port"]

    httpd = make_server('', port, make_App(settings))
    print("Serving on port {}...".format(port))
    httpd.serve_forever()
