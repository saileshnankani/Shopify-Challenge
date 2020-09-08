import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from repository.models import Image
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class ImageType(DjangoObjectType):
    class Meta:
        model = Image
  
class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    image = graphene.Field(ImageType, id=graphene.Int())
    users = graphene.List(UserType)
    images= graphene.List(ImageType)
    me = graphene.Field(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return get_user_model().objects.get(pk=id)

        return None

    def resolve_image(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Image.objects.get(pk=id)

        return None

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_images(self, info, **kwargs):
        return Image.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    username = graphene.String()
    password = graphene.String()

class ImageInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    image_name = graphene.String()
    user = UserInput

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, username, password):
        ok = True
        user_instance = get_user_model()(
            username=username,
        )
        user_instance.set_password(password)
        user_instance.save()
        return CreateUser(ok=ok, user=user_instance)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = get_user_model().objects.get(pk=id)
        if user_instance:
            ok = True
            user_instance.name = input.name
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class CreateImage(graphene.Mutation):
    class Arguments:
        input = ImageInput(required=True)

    ok = graphene.Boolean()
    image = graphene.Field(ImageType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user = get_user_model().objects.get(pk=input.user.id)
        if user is None:
            return CreateImage(ok=False, image=None)
        image_instance = Image(
            name=input.name,
            image_name=input.image_name,
            user=input.user
        )
        image_instance.save()
        image_instance.user.set(user)
        return CreateImage(ok=ok, image=image_instance)


class UpdateImage(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ImageInput(required=True)

    ok = graphene.Boolean()
    image = graphene.Field(ImageType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        image_instance = Image.objects.get(pk=id)
        if image_instance:
            ok = True
            user = get_user_model().objects.get(pk=image_instance.user.id)
            image_instance.name=input.name
            image_instance.year=input.year
            image_instance.user=input.user
            image_instance.save()
            if user:
                image_instance.user.set(user)
            return UpdateImage(ok=ok, image=image_instance)
        return UpdateImage(ok=ok, image=None)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_image = CreateImage.Field()
    update_image = UpdateImage.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
