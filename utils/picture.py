from client.models import Client


def get_client_picture(user):
    client = Client.objects.get(user=user)
    return client
