from flask import Blueprint, jsonify, request
from flask_cors import CORS

from src.database import add_blog, get_blogs, get_blog_by_id, delete_blog, update_blog, upload_image_to_s3

blog_api = Blueprint("blog_api", "blog_api", url_prefix="/api/blog")

CORS(blog_api, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

@blog_api.route('/', methods=['GET'])
def api_get_blogs():
    blogs = get_blogs()

    return jsonify(blogs), 200


@blog_api.route('/', methods=["POST"])
def api_add_blog():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "content is required"}), 400

    post_id = add_blog(data)

    return jsonify({"message": "Blog created", "id": str(post_id)}), 201


@blog_api.route('/<string:id>', methods=["GET"])
def api_get_blog(id):
    blog = get_blog_by_id(id)

    if blog:
        return jsonify(blog), 200

    return jsonify({"error": "Blog not found"}), 404


@blog_api.route('/<string:id>', methods=["PUT"])
def api_update_blog(id):
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "content is required"}), 400
    result = update_blog(id, data)
    return jsonify(result), 200


@blog_api.route('/<string:id>', methods=["DELETE"])
def api_delete_blog(id):
    result = delete_blog(id)
    return jsonify(result), 200

@blog_api.route('/image/upload', methods=["OPTIONS", "POST"])
def api_upload_image_to_s3():
    if "image" not in request.files:
        return jsonify({"error": "No file present"}), 400
    result = upload_image_to_s3(request.files)
    return jsonify(result)

