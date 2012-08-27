username = 'my_username'
api_key = 'my_api_key'

definition = 'interaction.content contains "datasift"'
definition_hash = '947b690ec9dca525fb8724645e088d79'

unicode_definition = u'interaction.content contains "datasift"'

invalid_definition = 'interactin.content contains "datasift"'

historic_start_date = 1335869526
historic_end_date   = 1335870126
historic_sources    = ['twitter', 'facebook']
historic_sample     = 1.56
historic_id         = '4ef7c852a96d6352764f'
historic_dpus       = 2334.6916666667
historic_name       = 'myhistoric'

push_id = 'b665761917bbcb7afd3102b4a645b41e'
push_created_at = 1335869526
push_hash_stream_type = 'stream'
push_hash_historic_type = 'historic'
push_hash = definition_hash
push_name = 'mypush'
push_status = 'active'
push_output_type = 'http'
push_output_params = {
        'delivery_frequency': 10,
        'url':                'http://www.example.com/push_endpoint',
        'auth.type':          'basic',
        'auth.username':      'frood',
        'auth.password':      'towel42'
    }
