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
    def calculer_temps_trajetV2(ctx, vitesse_moyenne, lat1, lon1, lat2, lon2, autonomie, temps_recharge_min):
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

    @rpc(Decimal, Decimal, Decimal, Decimal, _returns=Decimal)
    def calculer_temps_trajet(ctx, distance_km, vitesse_km_h, autonomie_km, temps_recharge_h):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = ctx.descriptor.service_class.origin
        temps_trajet = distance_km / vitesse_km_h  # Temps de trajet sans recharge
        # Nombre de recharges nécessaires
        nb_recharges = int(math.ceil(distance_km / autonomie_km)) - 1
        temps_recharge_total = nb_recharges * \
            temps_recharge_h  # Temps total de recharge
        # Temps total de trajet avec recharges
        temps_trajet_total = temps_trajet + temps_recharge_total
        return temps_trajet_total




def dist(lat1, lon1, lat2, lon2):
    return distance.distance((lat1, lon1), (lat2, lon2)).km

application = Application([TrajetService], 'mon_app_serveur.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
app = wsgi_application