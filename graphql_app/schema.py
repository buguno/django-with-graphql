import graphene
from graphene_django import DjangoObjectType

from contacts.models import Contact


class ContactType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    class Meta:
        model = Contact
        field = ("id", "name", "phone_number")


class Query(graphene.ObjectType):
    # Query ContactType to get list of contacts
    list_contact = graphene.List(ContactType)
    read_contact = graphene.Field(ContactType, id=graphene.Int())

    @staticmethod
    def resolve_list_contact(root, info):
        # We can easily optimize query count in the resolve method
        return Contact.objects.all()

    @staticmethod
    def resolve_read_contact(root, info, id):
        # get data where id in the database = id queried from the frontend
        return Contact.objects.get(id=id)


class ContactMutation(graphene.Mutation):
    class Arguments:
        # Add fields you would like to create. This will corelate with the ContactType fields above.
        id = graphene.ID()
        name = graphene.String()
        phone_number = graphene.String()

    # Define the class we are getting the fields from
    contact = graphene.Field(ContactType)

    @classmethod
    def mutate(cls, root, info, id, name, phone_number):
        # Function that will save the data
        contact = Contact(name=name, phone_number=phone_number)  # Accepts all fields
        contact.save()

        get_contact = Contact.objects.get(id=id)
        get_contact.name = name
        get_contact.phone_number = phone_number
        get_contact.save()
        return ContactMutation(contact=get_contact)


class Mutation(graphene.ObjectType):
    # Keywords that will be used to do the mutation in the frontend
    create_contact = ContactMutation.Field()
    update_contact = ContactMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
