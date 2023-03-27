from httpx import AsyncClient
import asyncio

#creating question
async def test_pass_quiz_not_auth(ac: AsyncClient):
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 20
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('/company/1/quiz/3/submit', json=payload)
    assert response.status_code == 403


async def test_create_question_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 20
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('company/1/quiz/3/submit', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"
    

async def test_pass_quiz_not_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 20
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('company/1/quiz/300/submit', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz does not exist"
    
    
async def test_pass_quiz_not_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 20
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('company/100/quiz/3/submit', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Company does not exist"


async def test_pass_quiz_one_success_two_correct(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 22
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('company/1/quiz/3/submit', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result') > 6.6         # 2/3*10
    assert response.json().get('result') < 6.7
    assert response.json().get('message') == "success"


async def test_pass_quiz_two_success_three_correct(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 3,
        "correct_answer": 2
        },
    {
        "id": 4,
        "correct_answer": 1
        },
    {
        "id": 9,
        "correct_answer": 2
        }
    ]
    }
    response = await ac.post('company/1/quiz/3/submit', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result') > 8.3  # 5/6*10
    assert response.json().get('result') < 8.4
    assert response.json().get('message') == "success"   



async def test_company_rating_one(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/1/rating", headers=headers)
    assert response.status_code == 200
    assert response.status_code == 200
    assert response.json().get('result') > 8.3         # 5/6*10
    assert response.json().get('result') < 8.4
    assert response.json().get('message') == "success"


async def test_pass_quiz_three_success_half_correct(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "answers": [
        {
        "id": 7,
        "correct_answer": 2
        },
    {
        "id": 8,
        "correct_answer": 11
        }
    ]
    }
    response = await ac.post('company/2/quiz/5/submit', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('result') == 5.0
    assert response.json().get('message') == "success"
    
    
async def test_company_rating_three(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/company/2/rating", headers=headers)
    assert response.status_code == 200
    assert response.status_code == 200
    assert response.json().get('result') == 5.0
    assert response.json().get('message') == "success"


async def test_user_system_rating(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/user/system_rating", headers=headers)
    assert response.status_code == 200
    assert response.json().get('result') == 7.5  #6/8*10