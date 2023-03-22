from httpx import AsyncClient

#creating question
async def test_create_question_not_auth(ac: AsyncClient):
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/5/', json=payload)
    assert response.status_code == 403


async def test_create_question_not_admin_or_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/5/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not owner or admin"
    

async def test_create_question_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/3/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"
    
    

async def test_create_question_not_quiz(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/300/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz does not exist"
    


async def test_create_question_not_full_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1"
    ]
}
    response = await ac.post('/question/quiz/3/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "At least two answer variants are required for a question."
    
    
async def test_create_question_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/3/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('message') == "success"
    

async def test_create_question_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
    "question": "which var?",
    "correct_answer": 1,
    "answer_variants": [
        "var1","var2","var3","var4"
    ]
}
    response = await ac.post('/question/quiz/5/', headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json().get('message') == "success"


#update question
async def test_bad_update_question_unauthorized(ac: AsyncClient):
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/9/quiz/3/", json=payload)
    assert response.status_code == 403


async def test_bad_update_question_not_found_quiz(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/9/quiz/100/", json=payload, headers=headers)
    assert response.status_code == 404
    

async def test_bad_update_question_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/900/quiz/3/", json=payload, headers=headers)
    assert response.status_code == 404


async def test_bad_update_question_not_your_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/9/quiz/3/", json=payload, headers=headers)
    assert response.status_code == 404



async def test_bad_update_question_not_owner_or_admin(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/10/quiz/5/", json=payload, headers=headers)
    assert response.status_code == 403
    
    
async def test_bad_update_question_not_full_answer(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/9/quiz/3/", json=payload, headers=headers)
    assert response.status_code == 400


async def test_update_question_success_one(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "question": "capital France?",
    "answer_variants": [
        "Madrid","Rome","Paris","London"
    ],
    "correct_answer": 2
    }
    response = await ac.put("/question/9/quiz/3/", json=payload, headers=headers)
    assert response.status_code == 200



async def test_get_question_by_id_one_updated(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/question/9/quiz/3/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("id") == 9
    assert response.json().get("result").get("question") == "capital France?"
    assert response.json().get("result").get("quiz_id") == 3
    assert response.json().get("result").get("correct_answer") == 2
    assert len(response.json().get("result").get("answer_variants")) == 4
    
    
async def test_update_question_success_two(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
    "quiz_id": 5,
    "question": "2*2=?",
    "answer_variants": [
        "1","10","0","4"
    ],
    "correct_answer": 3
    }
    response = await ac.put("/question/10/quiz/5/", json=payload, headers=headers)
    assert response.status_code == 200


async def test_get_question_by_id_two_updated(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/question/10/quiz/5/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("id") == 10
    assert response.json().get("result").get("question") == "2*2=?"
    assert response.json().get("result").get("quiz_id") == 5
    assert response.json().get("result").get("correct_answer") == 3
    assert len(response.json().get("result").get("answer_variants")) == 4    


#delete question
async def test_question_delete_not_auth(ac: AsyncClient):
    response = await ac.delete('/question/10/quiz/5/')
    assert response.status_code == 403


async def test_question_delete_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/question/100/quiz/5/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Question does not exist'


async def test_question_delete_quiz_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/question/10/quiz/500/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "Quiz does not exist"


async def test_question_delete_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.delete('/question/9/quiz/3/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"


async def test_question_delete_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/question/10/quiz/5/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not owner or admin"


async def test_question_delete_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/question/10/quiz/5/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('message') == "success"


async def test_get_question_deleted(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/question/10/quiz/5/", headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Question does not exist'
    
    
# get question

async def test_bad_get_question_unauthorized(ac: AsyncClient):
    response = await ac.put("/question/9/quiz/3/")
    assert response.status_code == 403


async def test_bad_get_question_by_id_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/question/900/quiz/3/", headers=headers)
    assert response.status_code == 404


async def test_bad_get_question_quiz_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/question/9/quiz/300/", headers=headers)
    assert response.status_code == 404


async def test_bad_get_question_not_member(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    response = await ac.get("/question/9/quiz/3/", headers=headers)
    assert response.status_code == 404    
    
    
async def test_bad_get_question_not_owner_admin(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/question/8/quiz/5/", headers=headers)
    assert response.status_code == 403
    



