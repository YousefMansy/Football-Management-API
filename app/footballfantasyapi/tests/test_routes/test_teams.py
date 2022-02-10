def test_fetch_team(authorized_client, authorized_user):
    team_id = 1
    response = authorized_client.get(f'/teams/team/{team_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == team_id
    assert response_json['user_id'] == authorized_user['id']
