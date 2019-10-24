
def init(app):

    """
    Inicializa las rutas para Gateways de Pagos
    app: Flask
    """

    @app.route('/v1/gateways/ipn', methods=['POST'])
    def addPayment():
        pass

    

    
