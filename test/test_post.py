from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    post = posts_list[0].Post
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
    # assert post.id == test_posts[0].id

# if the route is restricted will return 401
def test_unaothorized_user_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

def test_get_one_not_exist(client):
    res = client.get(f"/posts/9")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published, rating",[("marked title", "marked content", True, 0)])

def test_create_post(authorized_client, test_user, test_posts,title, content, published, rating):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published, "rating": rating})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content

def test_unaothorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "title", "content": "content", "published": False, "rating": 0})
    assert res.status_code == 401

def test_unaothorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_unahtorized_user_delete_other_user_post(authorized_client, test_user2, test_posts):
    
    res = authorized_client.delete(
        f"/posts/{test_posts[1].id}")
    assert res.status_code == 401


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "id": test_posts[0].id,
        "title": "updated title",
        "content": "updatd content",
        "published": True,
        "rating": 10
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostCreate(**res.json())
    assert res.status_code == 204
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "published": False,
        "rating": 0,
        "id": test_posts[1].id

    }
    res = authorized_client.put(f"/posts/{test_posts[1].id}", json=data)

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id
    }
    
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404