# Simulação da API do DETRAN - Na prática, você precisaria integrar com a API real
def consultar_detran(plate):
    # Esta é uma simulação - uma implementação real precisaria de credenciais e acesso à API oficial
    plate = plate.upper().replace(' ', '')
    
    # Simulação de dados baseados na placa
    if plate.startswith('ABC'):
        return {
            'modelo': 'Fiat Uno',
            'ano': 2018,
            'cor': 'Vermelho',
            'marca': 'Fiat',
            'situacao': 'Regular',
            'multas': [
                {'data': '15/03/2022', 'valor': 130.16, 'infracao': 'Excesso de velocidade'},
                {'data': '02/01/2023', 'valor': 88.38, 'infracao': 'Farol queimado'}
            ],
            'ipva': 'Pago',
            'licenciamento': 'Regular'
        }
    elif plate.startswith('XYZ'):
        return {
            'modelo': 'Volkswagen Gol',
            'ano': 2020,
            'cor': 'Prata',
            'marca': 'Volkswagen',
            'situacao': 'Regular',
            'multas': [],
            'ipva': 'Pago',
            'licenciamento': 'Regular'
        }
    else:
        return {
            'modelo': 'Desconhecido',
            'ano': 'Não identificado',
            'cor': 'Não identificada',
            'marca': 'Não identificada',
            'situacao': 'Não consta no sistema',
            'multas': [],
            'ipva': 'Não informado',
            'licenciamento': 'Não informado'
        }