import pytest


@pytest.fixture(autouse=True)
def create_users(django_user_model):
    user1 = "user1"
    pass1 = "pass1"
    django_user_model.objects.create_user(username=user1, password=pass1)
    user2 = "user2"
    pass2 = "pass2"
    django_user_model.objects.create_user(username=user2, password=pass2)


def test_get_not_authorized(client):
    response = client.get("/careers/")
    assert response.status_code == 403


def test_get_logged_in(client, django_user_model):
    client.login(username="user1", password="pass1")
    response = client.get("/careers/")
    assert response.status_code == 200


def test_post_not_authorized(client):
    response = client.post("/careers/", {"title": "Titulo", "content": "Conteúdo"})
    assert response.status_code == 403


def test_post_logged_in(client, django_user_model):
    client.login(username="user1", password="pass1")
    response = client.post("/careers/", {"title": "Titulo", "content": "Conteúdo"})
    assert response.status_code == 201


def test_should_get_logged_user_posts_only(client, django_user_model):
    client.login(username="user1", password="pass1")
    response = client.post(
        "/careers/", {"title": "Titulo Usuário 1", "content": "Conteúdo Usuário 1"}
    )
    assert response.status_code == 201
    client.login(username="user2", password="pass2")
    response = client.post(
        "/careers/", {"title": "Titulo Usuário 2", "content": "Conteúdo Usuário 2"}
    )
    response = client.get("/careers/")
    assert len(response.data) == 1


def test_should_get_logged_user_posts_only(client, django_user_model):
    client.login(username="user1", password="pass1")
    response = client.post(
        "/careers/", {"title": "Titulo Usuário 1", "content": "Conteúdo Usuário 1"}
    )
    assert response.status_code == 201
    post_id_other_user = response.data.get("id")
    client.login(username="user2", password="pass2")
    response = client.post(
        "/careers/", {"title": "Titulo Usuário 2", "content": "Conteúdo Usuário 2"}
    )
    response = client.get("/careers/{}/".format(post_id_other_user))
    assert response.status_code == 403


def test_should_edit_logged_user_posts_only(client, django_user_model):
    client.login(username="user1", password="pass1")
    response = client.post(
        "/careers/", {"title": "Titulo Usuário 1", "content": "Conteúdo Usuário 1"}
    )
    assert response.status_code == 201
    post_id_other_user = response.data.get("id")
    client.login(username="user2", password="pass2")
    response = client.put(
        "/careers/{}/".format(post_id_other_user),
        data={
            "title": "Titulo alterado pelo usuário 2",
            "content": "Conteúdo alterado pelo usuário 2",
        },
        content_type="application/json",
    )
    assert response.status_code == 403
