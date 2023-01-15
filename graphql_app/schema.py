from graphene import List, ObjectType, Schema
from graphene_django import DjangoObjectType

from contacts.models import Contact


class ContactType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")


class Query(ObjectType):
    # Query ContactType to get list of contacts
    list_contact = List(ContactType)

    def resolve_list_contact(root, info):
        # We can easily optimize query count in the resolve method
        return Contact.objects.all()


schema = Schema(query=Query)
