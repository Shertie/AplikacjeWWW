import graphene
from graphene_django import DjangoObjectType
from .models import Kraj, LiniaLotnicza, Lot, Hotel, Wycieczka

class KrajType(DjangoObjectType):
    class Meta:
        model = Kraj
        fields = "__all__"

class LiniaLotniczaType(DjangoObjectType):
    class Meta:
        model = LiniaLotnicza
        fields = "__all__"

class LotType(DjangoObjectType):
    class Meta:
        model = Lot
        fields = "__all__"

class HotelType(DjangoObjectType):
    class Meta:
        model = Hotel
        fields = "__all__"

class WycieczkaType(DjangoObjectType):
    class Meta:
        model = Wycieczka
        fields = "__all__"

class Query(graphene.ObjectType):
    all_kraje = graphene.List(KrajType)
    all_wycieczki = graphene.List(WycieczkaType)
    wycieczka_by_id = graphene.Field(WycieczkaType, id=graphene.Int(required=True))
    kraj_by_nazwa = graphene.Field(KrajType, nazwa=graphene.String(required=True))

    def resolve_all_kraje(root, info):
        return Kraj.objects.all()

    def resolve_all_wycieczki(root, info):
        return Wycieczka.objects.select_related('kraj_docelowy', 'hotel', 'lot_tam', 'lot_powrot').all()

    def resolve_wycieczka_by_id(root, info, id):
        try:
            return Wycieczka.objects.get(pk=id)
        except Wycieczka.DoesNotExist:
            return None
    
    def resolve_kraj_by_nazwa(root, info, nazwa):
        try:
            return Kraj.objects.get(nazwa=nazwa)
        except Kraj.DoesNotExist:
            return None

class CreateKraj(graphene.Mutation):
    class Arguments:
        nazwa = graphene.String(required=True)
        kod = graphene.String(required=True)
        kontynent = graphene.String(required=True)
        opis = graphene.String()

    kraj = graphene.Field(KrajType)

    @classmethod
    def mutate(cls, root, info, nazwa, kod, kontynent, opis=""):
        kraj = Kraj(nazwa=nazwa, kod=kod, kontynent=kontynent, opis=opis)
        kraj.save()
        return CreateKraj(kraj=kraj)

class Mutation(graphene.ObjectType):
    create_kraj = CreateKraj.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
