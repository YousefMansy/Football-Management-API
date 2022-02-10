def test_fetch_player(authorized_client, authorized_user):
    player_id = 1
    response = authorized_client.get(f'/players/player/{player_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == player_id
