import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from posts.models import Post, Category, Topic

def setup():
    print("Setting up Lab 7 data...")

    # 1. Create Group "Lab7_Group"
    group_lab7, created = Group.objects.get_or_create(name='Lab7_Group')
    print(f"Group 'Lab7_Group' created: {created}")

    # 2. Add 'view_category' permission to "Lab7_Group"
    content_type = ContentType.objects.get_for_model(Category)
    permission = Permission.objects.get(
        codename='view_category',
        content_type=content_type,
    )
    group_lab7.permissions.add(permission)
    print(f"Added 'view_category' to 'Lab7_Group'")

    # 3. Create user "lab7user"
    user_lab7, created = User.objects.get_or_create(username='lab7user')
    if created:
        user_lab7.set_password('testpass123')
        user_lab7.is_staff = True # "w zespole"
        user_lab7.save()
    print(f"User 'lab7user' created: {created}")

    # 4. Add "lab7user" to "Lab7_Group"
    user_lab7.groups.add(group_lab7)
    print(f"Added 'lab7user' to 'Lab7_Group'")

    # 5. Create Group "moderator forum"
    group_mod, created = Group.objects.get_or_create(name='moderator forum')
    print(f"Group 'moderator forum' created: {created}")

    # 6. Add 'can_edit_others_posts' to "moderator forum"
    content_type_post = ContentType.objects.get_for_model(Post)
    perm_edit_others = Permission.objects.get(
        codename='can_edit_others_posts',
        content_type=content_type_post,
    )
    group_mod.permissions.add(perm_edit_others)
    print(f"Added 'can_edit_others_posts' to 'moderator forum'")

    # 7. Create user "moderator"
    user_mod, created = User.objects.get_or_create(username='moderator')
    if created:
        user_mod.set_password('testpass123')
        user_mod.is_staff = True
        user_mod.save()
    print(f"User 'moderator' created: {created}")

    # 8. Add "moderator" to "moderator forum"
    user_mod.groups.add(group_mod)
    print(f"Added 'moderator' to 'moderator forum'")
    
    # Also give moderator 'change_post' permission so they can actually edit
    perm_change_post = Permission.objects.get(
        codename='change_post',
        content_type=content_type_post,
    )
    group_mod.permissions.add(perm_change_post)
    print(f"Added 'change_post' to 'moderator forum'")

    # Create a post by another user for testing
    other_user, _ = User.objects.get_or_create(username='testuser') # Existing from Lab 6
    if not other_user.password:
        other_user.set_password('testpass123')
        other_user.save()
    
    # Ensure we have a category and topic
    cat, _ = Category.objects.get_or_create(name='TestCat')
    topic, _ = Topic.objects.get_or_create(title='TestTopic', category=cat)

    post, created = Post.objects.get_or_create(
        title='Post by testuser',
        defaults={
            'text': 'Content',
            'slug': 'post-by-testuser',
            'topic': topic,
            'created_by': other_user
        }
    )
    if not created and post.created_by != other_user:
        post.created_by = other_user
        post.save()
    print(f"Post '{post.title}' created/ensured by {post.created_by.username} (ID: {post.id})")

if __name__ == '__main__':
    setup()
