import graphene
from graphene_django import DjangoObjectType
from posts.models import Category, Topic, Post
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "posts")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = "__all__"

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

class Query(graphene.ObjectType):
    # Basic queries
    all_categories = graphene.List(CategoryType)
    all_topics = graphene.List(TopicType)
    all_posts = graphene.List(PostType)
    
    category_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))

    # Task 2: Additional resolvers
    # 1. Filter posts by title fragment
    posts_by_title_fragment = graphene.List(PostType, substr=graphene.String(required=True))
    
    # 2. Count posts for a user
    post_count_by_user = graphene.Int(user_id=graphene.Int(required=True))
    
    # 3. Topics by category name fragment
    topics_by_category_name_fragment = graphene.List(TopicType, substr=graphene.String(required=True))

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_topics(root, info):
        return Topic.objects.all()

    def resolve_all_posts(root, info):
        return Post.objects.select_related('topic', 'created_by').all()

    def resolve_category_by_id(root, info, id):
        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return None

    def resolve_post_by_id(root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_posts_by_title_fragment(root, info, substr):
        return Post.objects.filter(title__icontains=substr)

    def resolve_post_count_by_user(root, info, user_id):
        return Post.objects.filter(created_by_id=user_id).count()

    def resolve_topics_by_category_name_fragment(root, info, substr):
        return Topic.objects.filter(category__name__icontains=substr)

# Task 3: Mutations for Post

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        text = graphene.String(required=True)
        slug = graphene.String(required=True)
        topic_id = graphene.Int(required=True)
        created_by_id = graphene.Int(required=True)

    post = graphene.Field(PostType)

    def mutate(root, info, title, text, slug, topic_id, created_by_id):
        try:
            topic = Topic.objects.get(pk=topic_id)
            user = User.objects.get(pk=created_by_id)
            post = Post(title=title, text=text, slug=slug, topic=topic, created_by=user)
            post.save()
            return CreatePost(post=post)
        except (Topic.DoesNotExist, User.DoesNotExist):
            raise Exception("Topic or User not found")

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        text = graphene.String()
        slug = graphene.String()

    post = graphene.Field(PostType)

    def mutate(root, info, id, title=None, text=None, slug=None):
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            raise Exception("Post not found")

        if title:
            post.title = title
        if text:
            post.text = text
        if slug:
            post.slug = slug
        
        post.save()
        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return DeletePost(success=True)
        except Post.DoesNotExist:
            return DeletePost(success=False)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
