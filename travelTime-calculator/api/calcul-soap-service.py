from spyne import Application, rpc, ServiceBase, Integer,Float, Unicode , Decimal
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from geopy.distance import distance

class CalculService(ServiceBase):
    @rpc(Float, Float, Float, Float, Float, Float, Float, _returns=Float)
    def calculer_temps_trajet(ctx,vitesse_moyenne, lat1, lon1, lat2, lon2, autonomie, temps_recharge_min):
        ctx.transport.resp_headers['Access-Control-Allow-Origin'] = '*'

        # Utiliser GeoPy pour calculer la distance entre les coordonnées GPS
        distance_km = distance((lat1, lon1), (lat2, lon2)).km
        # Calculer la distance maximale que la voiture peut parcourir avec l'autonomie donnée
        distance_max_km = autonomie

        # Calculer le temps de trajet sans tenir compte du temps de recharge
        temps_trajet = distance_km / vitesse_moyenne
        # Calculer le nombre de recharges nécessaires
        nb_recharges = distance_km // distance_max_km
        # Calculer le temps de recharge total
        temps_recharge_total = 1+ nb_recharges * temps_recharge_min
        # Ajouter le temps de recharge total au temps de trajet
        temps_trajet += temps_recharge_total
        # Retourner le temps de trajet
        return (temps_trajet /10 )* 2


application = Application([CalculService], 'info.802.calcul.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)
app = wsgi_application

# if __name__ == '__main__':
#     server = make_server('127.0.0.1', 8000, wsgi_application)
#     server.serve_forever()
