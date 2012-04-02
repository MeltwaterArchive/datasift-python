username = 'my_username'
api_key = 'my_api_key'

definition = 'interaction.content contains "datasift"'
definition_hash = '947b690ec9dca525fb8724645e088d79'

unicode_definition = u'interaction.content contains "datasift"'

invalid_definition = 'interactin.content contains "datasift"'

stream_id = 10121
stream_name = 'DataSift API Test'
stream_description = 'This stream is used by the official DataSift API tests.'

stream_versions = {
    1: {
        'message': '',
        'definition': 'interaction.content contains "datasift"',
        'definition_hash': '947b690ec9dca525fb8724645e088d79',
        'created_at': 1305817598,
    },
    2: {
        'message': 'Added Klout score condition.',
        'definition': 'interaction.content contains "datasift" and klout.score > 50',
        'definition_hash': '2554e156165157ff7a55879615756f49',
        'created_at': 1305927524,
    },
    3: {
        'message': 'Removed the Klout score condition.',
        'definition': 'interaction.content contains "datasift"',
        'definition_hash': '947b690ec9dca525fb8724645e088d79',
        'created_at': 1305927551,
    },
}
