import json
import os
import time

import boto3
from bson import ObjectId
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

# AWS S3 Configuration
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def add_blog(data):
    author = data.get("author", {})
    blog_type = data.get("blogType", "Other")

    timestamp = int(time.time() * 1000)
    blog = {"author": author,
            "blog_type": blog_type,
            "last_updated_at": timestamp,
            "content": json.dumps(data.get("content", {}))}
    from src.factory import mongo
    post_id = mongo.db.blogs.insert_one(blog).inserted_id
    return post_id


def get_blogs():
    blogs = []
    from src.factory import mongo
    for blog in mongo.db.blogs.find():
        blogs.append({
            "id": str(blog["_id"]),
            "author": blog.get("author", {}),
            "blog_type": blog.get("blog_type", "Other"),
            "last_updated_at": blog.get("last_updated_at"),
            "content": json.loads(blog.get("content", "{}"))
        })
    return blogs


def get_blog_by_id(blog_id):
    from src.factory import mongo
    try:
        object_id = ObjectId(blog_id)
    except:
        return None
    blog = mongo.db.blogs.find_one({"_id": object_id})
    if blog:
        return {
            "id": str(blog["_id"]),
            "author": blog.get("author", {}),
            "blog_type": blog.get("blog_type", "Other"),
            "last_updated_at": blog.get("last_updated_at"),
            "content": json.loads(blog.get("content", "{}"))
        }

    return None


def update_blog(blog_id, data):
    saved_blog = get_blog_by_id(blog_id)
    if not saved_blog:
        return {"error": "Blog not found"}

    from src.factory import mongo
    try:
        object_id = ObjectId(blog_id)
    except:
        return {"message": "Blog not found"}

    timestamp = int(time.time() * 1000)

    updated_data = {
        "author": data.get("author", saved_blog.get("author")),
        "blog_type": data.get("blog_type", saved_blog.get("blog_type")),
        "last_updated_at": timestamp,
        "content": json.dumps(data.get("content"))
    }

    mongo.db.blogs.find_one_and_update(
        {"_id": object_id},
        {"$set": updated_data}
    )

    return {"message": "Blog updated", "id": blog_id}


def delete_blog(blog_id):
    from src.factory import mongo
    try:
        object_id = ObjectId(blog_id)
    except:
        return {"message": "Blog not found"}
    result = mongo.db.blogs.delete_one({"_id": object_id})
    if result.deleted_count:
        return {"message": "Blog deleted"}
    return {"message": "Blog not found"}


def upload_image_to_s3(data):
    file = data["image"]
    filename = secure_filename(file.filename)
    s3.upload_fileobj(file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})

    file_url = f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{filename}"

    return {"success": 1, "file": {"url": file_url}}


def get_user_by_email(email):
    from src.factory import mongo
    return mongo.db.users.find_one({"email": email})


def get_user_by_id(id):
    from src.factory import mongo
    try:
        object_id = ObjectId(id)
    except:
        return None
    return mongo.db.users.find_one({"_id": object_id})


def add_user(user):
    from src.factory import mongo
    return mongo.db.users.insert_one(user)


def update_user(user, update):
    from src.factory import mongo
    mongo.db.users.update_one({"_id": user["_id"]}, {"$set": update})


def delete_user_by_id(id):
    from src.factory import mongo
    try:
        object_id = ObjectId(id)
    except:
        return None
    return mongo.db.users.delete_one({"_id": object_id})
