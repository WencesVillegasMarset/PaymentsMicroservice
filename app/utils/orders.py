import http.client
import socket

import memoize

import app.utils.config as config
import app.utils.errors as errors
import app.utils.json_serializer as json

def getOrder(orderId, authKey):
    """
    Obtiene el order desde el servicio orders
    orderId: string id de order enviado por el cliente
    authKey: string El header Authorization enviado por el cliente
    return dict<property, value> Order
    """
    headers = {"Authorization".encode("utf-8"): authKey.encode("utf-8")}
    conn = http.client.HTTPConnection(
        socket.gethostbyname(config.get_orders_server_url()),
        config.get_orders_server_port(),
    )

    conn.request("GET", "/v1/orders/"+orderId,{}, headers)
    response = conn.getresponse()
    if (response.status != 200):
        raise errors.InvalidAuth()

    result = json.body_to_dic(response.read().decode('utf-8'))
    if result == None:
        raise errors.InvalidArgument('orderId', 'No order with that id')
    # for res in result:
        # if orderId == res['id']:
    return result

if __name__ == "__main__":
    pass
    res = getOrder('5dae41e40d86e227740bc318', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNWRhZGIyZmU5ZWQ3NWYzZmNjNjQwZGQzIiwidG9rZW5faWQiOiI1ZGFlNWQ1MjE0Nzg0MDM5Y2MzOGQ5YzciLCJpYXQiOjE1NzE3MDgyNDJ9.7qQOOiVICurfQgMCGJkmZP3FHdvwFHWdEphcfR1Hzmk')
    print(res)