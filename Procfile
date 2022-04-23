release: chmod u+x dokku_commands.sh && chmod u+x geoip/GeoLite2-Country.mmdb && ./dokku_commands.sh
web: gunicorn config.wsgi:application --worker-class gevent
