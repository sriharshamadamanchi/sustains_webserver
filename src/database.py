import json
import os
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
    blog = {"content": json.dumps(data["content"])}
    from src.factory import mongo
    post_id = mongo.db.blogs.insert_one(blog).inserted_id
    return post_id


def get_blogs():
    blogs = []
    from src.factory import mongo
    for blog in mongo.db.blogs.find():
        blogs.append({"id": str(blog["_id"]), "content": json.loads(blog["content"])})
    return blogs


def get_blog_by_id(blog_id):
    from src.factory import mongo
    try:
        object_id = ObjectId(blog_id)
    except:
        return None
    post = mongo.db.blogs.find_one({"_id": object_id})
    if post:
        return {"id": str(post["_id"]), "content": json.loads(post["content"])}

    return None


def update_blog(blog_id, data):
    from src.factory import mongo
    try:
        object_id = ObjectId(blog_id)
    except:
        return {"message": "Blog not found"}
    updated_blog = mongo.db.blogs.find_one_and_update(
        {"_id": object_id},
        {"$set": {"content": json.dumps(data["content"])}}
    )

    if updated_blog:
        return {"message": "Blog updated", "id": blog_id}
    return {"error": "Blog not found"}


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

    return {"url": file_url}
