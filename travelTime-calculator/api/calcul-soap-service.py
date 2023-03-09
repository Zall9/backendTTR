from datetime import datetime, timedelta
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Decimal
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import decimal
from wsgiref.simple_server import make_server
import math
from geopy import distance


class TrajetService(ServiceBase):
    origin = '*'

    @rpc(float, float, float, float, float, float, float, _returns=float)
    def calculer_temps_trajet(ctx, vitesse_moyenne, lat1, lon1, lat2, lon2, autonomie, temps_recharge_min):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'

        # Utiliser GeoPy pour calculer la distance entre les coordonnées GPS
        distance_km = distance.distance((lat1, lon1), (lat2, lon2)).km
        # Calculer la distance maximale que la voiture peut parcourir avec l'autonomie donnée
        distance_max_km = autonomie

        # Calculer le temps de trajet sans tenir compte du temps de recharge
        temps_trajet = distance_km / vitesse_moyenne
        # Calculer le nombre de recharges nécessaires
        nb_recharges = distance_km // distance_max_km
        # Calculer le temps de recharge total
        temps_recharge_total = 1 + nb_recharges * temps_recharge_min
        # Ajouter le temps de recharge total au temps de trajet
        temps_trajet += temps_recharge_total
        # Retourner le temps de trajet
        return (temps_trajet / 10) * 2

application = Application([TrajetService], 'mon_app_serveur.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
app = wsgi_application