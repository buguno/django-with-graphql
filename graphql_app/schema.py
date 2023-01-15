from graphene import Field, Int, List, Mutation, ObjectType, Schema, String
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
    read_contact = Field(ContactType, id=Int())

    @staticmethod
    def resolve_list_contact(root, info):
        # We can easily optimize query count in the resolve method
        return Contact.objects.all()

    @staticmethod
    def resolve_read_contact(root, info, id):
        # get data where id in the database = id queried from the frontend
        return Contact.objects.get(id=id)


class ContactMutation(Mutation):
    class Arguments:
        # Add fields you would like to create. This will corelate with the ContactType fields above.
        name = String()
        phone_number = String()

    contact = Field(ContactType)  # Define the class we are getting the fields from

    @classmethod
    def mutate(cls, root, info, name, phone_number):
        # Function that will save the data
        contact = Contact(name=name, phone_number=phone_number)  # Accepts all fields
        contact.save()
        return ContactMutation(contact=contact)


class Mutation(ObjectType):
    # Keywords that will be used to do the mutation in the frontend
    create_contact = ContactMutation.Field()


schema = Schema(query=Query, mutation=Mutation)
