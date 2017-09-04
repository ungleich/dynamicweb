from hosting.models import UserHostingKey


def get_all_public_keys(customer):
    """
    Returns all the public keys of the user
    :param customer: The customer whose public keys are needed
    :return: A list of public keys
    """
    return UserHostingKey.objects.filter(user_id=customer.id).values_list(
        "public_key", flat=True)
