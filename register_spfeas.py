from gbdxtools import Interface

gbdx = Interface(
    username = '',
    password = '',
    client_id= '',
    client_secret = ''
)

gbdx.task_registry.register(json_filename = 'hello-gbdx-definition.json')