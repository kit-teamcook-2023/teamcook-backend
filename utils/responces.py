class Responces():
    def delete(self, method:str) -> dict[int, dict]:
        return {
                200: {
                    "description": "삭제 성공",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": f"Remove {method} successed"
                            }
                        }
                    }
                },
                400: {
                    "description": "삭제 실패",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": f"Remove {method} failed"
                            }
                        }
                    }
                },
                401: {
                    "description": "승인되지 않은 유저",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": f"Not allowed"
                            }
                        }
                    }
                }
            }

    def post_comment(self) -> dict:
        return {
                200: {
                    "description": "댓글 작성 성공",
                    "content": {
                        "application/json": {
                            "example": {
                                "comment_id": "<int>",
                                "post_id": "<int>",
                                "status": "Post comment successed"
                            }
                        }
                    }
                },
                400: {
                    "description": "댓글 작성 실패",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "Post comment failed"
                            }
                        }
                    }
                }
            }

    def post_post(self):
        return {
            200: {
                "description": "글 작성 성공",
                "content": {
                    "application/json": {
                        "example": {
                            "id": "<int>",
                            "status": "Post post successed"
                        }
                    }
                }
            },
            400: {
                "description": "글 작성 실패",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "Post post failed"
                        }
                    }
                }
            }
        }

    def get_post(self):
        return {
                200: {
                    "description": "글 및 댓글 조회 성공",
                    "content": {
                        "application/json": {
                            "example": {
                                "writing": {
                                    "title": "test",
                                    "content": "test 내용입니다",
                                    "author": "작성자입니다",
                                    "date": "23-04-12 10:25:41"
                                },
                                "comments": [
                                    {
                                        "content": "댓글 내용입니다",
                                        "author": "작성자입니다",
                                        "date": "23-04-20 17:24:56",
                                        "id": 17
                                    },
                                    {
                                        "content": "댓글 내용입니다",
                                        "author": "작성자입니다",
                                        "date": "23-04-20 17:24:56",
                                        "id": 24
                                    }
                                ],
                                "writing_id": "13"
                            }
                        }
                    }
                },
                400: {
                    "description": "해당 id 가진 글 없음",
                    "content": {
                        "application/json": {
                            "example": {
                                "status": "Not exist post id"
                            }
                        }
                    }
                }
            }

    def get_all_posts(self):
        return {
            200: {
                "description": "조회 성공",
                "content": {
                    "application/json": {
                        "example": {
                            "counts": 34,
                            "posts": [
                                {
                                    'id': 20,
                                    'title': 'eg_title',
                                    'author': 'tester',
                                    'date': "23-04-10 10:32:41"
                                },
                                {
                                    'id': 31,
                                    'title': 'eg_title1',
                                    'author': 'tester1',
                                    'date': "23-04-10 10:35:41"
                                }
                            ]
                        }
                    }
                }
            }
        }

    def search_posts(self):
        return {
            200: {
                "description": "조회 성공",
                "content": {
                    "application/json": {
                        "example": {
                            "counts": 14,
                            "posts": [
                                {
                                    'id': 20,
                                    'title': 'eg_title',
                                    'author': 'tester',
                                    'date': "23-04-10 10:32:41"
                                },
                                {
                                    'id': 31,
                                    'title': 'eg_title1',
                                    'author': 'tester1',
                                    'date': "23-04-10 10:35:41"
                                }
                            ]
                        }
                    }
                }
            }
        }

    def kakao_callback(self):
        return {
            200: {
                "description": "회원가입용 토큰 발급",
                "content": {
                    "application/json": {
                        "example": {
                            'access_token': 'xxx.payload.yyy'
                        }
                    }
                }
            },
            226: {
                "description": "기 가입자의 토큰 발급",
                "content": {
                    "application/json": {
                        "example": {
                            'access_token': 'xxx.payload.yyy'
                        }
                    }
                }
            }
        }

    def check_nickname_usage(self):
        return {
            200: {
                "description": "닉네임 사용 가능",
            },
            226: {
                "description": "닉네임 사용중",
            }
        }

    def get_user_fee(self):
        return {
            200: {
                "description": "사용자 가스, 전기 사용 요금 반환",
                "content": {
                    "application/json": {
                        "example": {
                            'last_month': {
                                'gas': '<int>',
                                'elec': '<int>'
                            },
                            'cur_month' : {
                                'gas': '<int>',
                                'elec': '<int>'
                            }
                        }
                    }
                }
            }
        }

    def check_valid_token(self):
        return {
            200: {
                "description": "유효한 토큰",
                "content": {
                    "application/json": {
                        "example": {
                            'status': 'valid'
                        }
                    }
                }
            },
            401: {
                "description": "유효하지 않은 토큰. ",
                "content": {
                    "application/json": {
                        "example": {
                            'status': 'Invalid token or expired token.'
                        }
                    }
                }
            }
        }

    def sign_up(self):
        return {
            200: {
                "description": "회원가입 성공, 토큰 발급",
                "content": {
                    "application/json": {
                        "example": {
                            'access_token': 'xxx.payload.yyy'
                        }
                    }
                }
            },
            226: {
                "description": "회원가입 request를 보냈을때도 한번 더 닉네임 검사. 중복 닉네임 있을 경우 발생.",
                "content": {
                    "application/json": {
                        "example": {
                            "signup": "ignored"
                        }
                    }
                }
            }
        }

    def delete_user(self):
        return {
            200: {
                "description": "탈퇴 성공",
                "content": {
                    "application/json": {
                        "example": {
                            'status': 'delete successed'
                        }
                    }
                }
            },
            400: {
                "description": "이미 탈퇴된 회원",
                "content": {
                    "application/json": {
                        "example": {
                            'status': 'already deleted'
                        }
                    }
                }
            }
        }

    def get_previous_chat(self):
        return {
            200: {
                "description": "이전  조회 성공",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                'sender': 'test1',
                                'message': 'testing',
                                'date': "23-04-10T10:32:41"
                            },
                            {
                                'sender': 'test2',
                                'message': 'testing_',
                                'date': "23-04-10T10:32:43"
                            },
                        ]
                    }
                }
            }
        }

    def modify_like(self):
        return {
            200: {
                "description": "좋아요 추가/제거 성공",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "status": "Like successed"
                            }
                        ]
                    }
                }
            }, 
            400: {
                "description": "좋아요 추가/제거 실패",
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "status": "Like failed"
                            }
                        ]
                    }
                }
            }
        }