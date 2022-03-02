from flask import Flask, Response
import logging
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler
import os


os.system("curl -v 127.0.0.1:8200")
os.environ['NO_PROXY'] = '127.0.0.1'
app = Flask(__name__)


from elasticapm.contrib.flask import ElasticAPM
app.config['ELASTIC_APM'] = {
# Set the required service name. Allowed characters:
# a-z, A-Z, 0-9, -, _, and space
'SERVICE_NAME': 'my-app',

# Use if APM Server requires a secret token
'SECRET_TOKEN': '',

# Set the custom APM Server URL (default: http://localhost:8200)
#'SERVER_URL': 'http://10.61.145.105:8200',
'SERVER_URL': 'http://127.0.0.1:8200',
# Set the service environment
'ENVIRONMENT': 'production',
'DEBUG': True
}
apm = ElasticAPM(app)
@app.route('/')
def bar():
    try:
        1 / 0
    except ZeroDivisionError:
        print("dmmm")
        app.logger.error('Math is hard',
            exc_info=True,
            extra={
                'good_at_math': False,
            }
        )
        return "dmm"
@app.route('/dev')
def dev():
    try:
        1 / 0
    except ZeroDivisionError:
        app.logger.error('Math is dev',
            exc_info=True,
            extra={
                'good_at_math': False,
            }
        )
        return Response(response="a >= 10", status=502)
@app.route('/count404')
def notFound():
    try:
        1 / 0
    except ZeroDivisionError:
        app.logger.error('Math is dev',
            exc_info=True,
            extra={
                'good_at_math': False,
            }
        )
        return Response(response="a >= 10", status=405)

if __name__ == '__main__':
    # Create a logging handler and attach it.
    handler = LoggingHandler(client=apm.client)
    handler.setLevel(logging.WARN)
    app.logger.addHandler(handler)
    app.run(host='127.0.0.1', port=8088)
