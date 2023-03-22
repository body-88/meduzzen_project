from httpx import AsyncClient

#creating quiz
async def test_create_quiz_not_auth(ac: AsyncClient):
    payload = {
    "company_id": 1,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', json=payload)
    assert response.status_code == 403


async def test_create_quiz_not_admin_or_owner(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "company_id": 2,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not owner or admin"
    

async def test_create_quiz_not_member(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
    "company_id": 1,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"
    
    

async def test_create_quiz_not_company(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "company_id": 100,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"
    


async def test_create_quiz_not_full_question(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "company_id": 1,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "At least two questions are required for a quiz."
    
    
async def test_create_quiz_not_full_answer(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "company_id": 1,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 400
    assert response.json().get('detail') == "At least two answer variants are required for a question."
    
    
async def test_create_quiz_one_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
    "company_id": 1,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json().get('message') == "success"
    

async def test_create_quiz_two_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
    "company_id": 2,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json().get('message') == "success"
    

async def test_create_quiz_three_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test3@test.com']}",
    }
    payload = {
    "company_id": 2,
    "name": "string",
    "description": "string",
    "frequency": "string",
    "questions": [
        {
        "question": "string",
        "correct_answer": 2,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        },
        {
        "question": "string",
        "correct_answer": 1,
        "answer_variants": [
            "var1","var2","var3","var4"
        ]
        }
    ]
}
    response = await ac.post('/quiz/', headers=headers, json=payload)
    assert response.status_code == 201
    assert response.json().get('message') == "success"
    
    

#quizzes list

async def test_quizzes_list_not_auth(ac: AsyncClient):
    response = await ac.get('/company/1/quizzes')
    assert response.status_code == 403


async def test_quizzes_list_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/100/quizzes', headers=headers)
    assert response.status_code == 404


async def test_quizzes_list_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get('/company/2/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 2
    
    
#update quiz
async def test_bad_update_quiz_unauthorized(ac: AsyncClient):
    payload = {
        "name": "quiz_NEW",
        "frequency": "30"
    }
    response = await ac.put("/quiz/1/company/1/", json=payload)
    assert response.status_code == 403


async def test_bad_update_quiz_not_found_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "quiz_NEW",
        "frequency": "30"
    }
    response = await ac.put("/quiz/1/company/100/", json=payload, headers=headers)
    assert response.status_code == 404
    

async def test_bad_update_quiz_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "quiz_NEW",
        "frequency": "30"
    }
    response = await ac.put("/quiz/100/company/1/", json=payload, headers=headers)
    assert response.status_code == 404


async def test_bad_update_quiz_not_your_company(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test4@test.com']}",
    }
    payload = {
        "name": "quiz_NEW",
        "frequency": "30"
    }
    response = await ac.put("/quiz/2/company/1/", json=payload, headers=headers)
    assert response.status_code == 404



async def test_bad_update_quiz_not_owner_or_admin(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    payload = {
        "name": "quiz_NEW",
        "frequency": "30"
    }
    response = await ac.put("/quiz/2/company/2/", json=payload, headers=headers)
    assert response.status_code == 403


async def test_update_quiz(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    payload = {
        "name": "quiz_NEW",
        "description": "new_description",
        "frequency": "30"
    }
    response = await ac.put("/quiz/4/company/2/", json=payload, headers=headers)
    assert response.status_code == 200



async def test_get_quiz_by_id_one_updated(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/quiz/4/company/2/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("id") == 4
    assert response.json().get("result").get("name") == "quiz_NEW"
    assert response.json().get("result").get("frequency") == "30"
    assert response.json().get("result").get("company_id") == 2



#delete quiz
async def test_quiz_delete_not_auth(ac: AsyncClient):
    response = await ac.delete('/quiz/5/company/2/')
    assert response.status_code == 403


async def test_quiz_delete_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/quiz/100/company/2/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quiz does not exist'


async def test_quiz_delete_company_not_found(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.delete('/quiz/4/company/200/', headers=headers)
    assert response.status_code == 404
    assert response.json().get('detail') == "You're not member of the company or company doesn't exist"


async def test_quiz_delete_not_owner_or_admin(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.delete('/quiz/4/company/2/', headers=headers)
    assert response.status_code == 403
    assert response.json().get('detail') == "You are not owner or admin"


async def test_quiz_delete_success(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }

    response = await ac.delete('/quiz/4/company/2/', headers=headers)
    assert response.status_code == 200
    assert response.json().get('message') == "success"


async def test_quiz_list_success_after_remove(ac: AsyncClient, users_tokens):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get('/company/2/quizzes', headers=headers)
    assert response.status_code == 200
    assert len(response.json().get('result').get('quizzes')) == 1

# get quiz

async def test_bad_get_quiz_unauthorized(ac: AsyncClient):
    response = await ac.put("/quiz/1/company/1/")
    assert response.status_code == 403


async def test_bad_get_quiz_by_id_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/quiz/100/company/1/", headers=headers)
    assert response.status_code == 404


async def test_bad_get_quiz_company_not_found(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/quiz/5/company/100/", headers=headers)
    assert response.status_code == 404


async def test_bad_get_quiz_not_member(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/quiz/3/company/1/", headers=headers)
    assert response.status_code == 404    
    
    
async def test_bad_get_quiz_not_owner_admin(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test1@test.com']}",
    }
    response = await ac.get("/quiz/5/company/2/", headers=headers)
    assert response.status_code == 403
    

async def test_get_quiz_success(users_tokens, ac: AsyncClient):
    headers = {
        "Authorization": f"Bearer {users_tokens['test2@test.com']}",
    }
    response = await ac.get("/quiz/5/company/2/", headers=headers)
    assert response.status_code == 200
    assert response.json().get("result").get("id") == 5
    assert response.json().get("result").get("name") == "string"
    assert response.json().get("result").get("frequency") == "string"
    assert response.json().get("result").get("company_id") == 2
    assert len(response.json().get("result").get("questions")) == 2



