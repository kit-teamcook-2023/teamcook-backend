변경점

	1. 게시글 저장을 firebase에서 mysql로 변경
		firebase로 저장 시 어떻게 게시글을 가져와야 할 지 모르겠음.
		검색해도 자료가 부족함.
		sql은 LIMIT를 이용해서 바로 가져올 수 있음
	2. 닉네임을 mysql에 저장하도록 함.
		2차 발표 이후 uid를 이용해서 닉네임 설정하려고 하였음.
		하지만 사용자에게 닉네임을 설정하자! 라고 결정

	3. 크롤링 서버 aws lambda로 이동
		=> 크롤링하는데 3초가 넘어감... aws lambda 최대가 3초라 더 늘릴 수 없음

	4. frontend와 카카오 로그인 기능 구현 중 cors 오류 발생 및 redirect uri 이슈
		=> cors hosts를 ["*"]로 설정. 이전에는 localhost:8000으로 설정하여 외부에서 접근 불가.
		=> 카카오 redirect uri는 로그인 완료 후 로딩되는 page uri를 입력해야 함.
			서버 uri를 입력해서 카카오 로그인이 제대로 되지 않았던 현상 발생.
	
진행상황

	구현 완료

		1. 가스요금, 전기요금 계산식 완성 및 반환 라우팅 완료

		2. 유저 닉네임 중복 체크

		3. 카카오 로그인 기능 추가
			cors, redirect uri 이슈 해결
			redirect uri : 카카오 로그인 후 되돌아가는 페이지의 uri.
				서버에서 return해주는 라우팅이 없는 이상, 서버 uri로 아무리 시도해도 되지 않았음

		4. 게시글, 댓글 추가 및 제거 sql 쿼리문 작성

		5. jwt 토큰을 이용한 사용자 인증
			글 작성, 수정 등에 사용될 예정
			fastapi dependencies를 통한 토큰 검증기능 추가

		6. 글 작성 시 이미지 첨부
			aws s3버킷을 이용하여 이미지 업로드, s3버킷의 이미지 경로를 통해 이미지를 보여줌
		
	구현 중

		1. 게시글, 댓글 수정 sql 쿼리문 작성
			수정은 현재로선 고려상황이 아님

		2. 각 api 작성 후 docs 추가

		3. firebase로 구글 로그인 테스트

		4. 
		
	구현 해야 할 것

		1. 회원가입 시 기기와 통신 - 라즈베리파이 필요
			lora 통신 기능 수행할 수 있어야함.
			local로 wifi 공유기 dns 쓰면 되긴 한데...
			실 사용에서는 lora 필요함

		

	수정

		1. cors 오류
			cors가 aws 서버의 localhost만 접근 가능하도록 되어있어 문제가 됐었음.
			["*"] 로 하여 모든 ip에서 접근 가능하도록 수정


1. 기존 개발 목표 및 일정표

2. 현재 개발 진행 상황 (기존 개발 일정표와 비교)

3. 기존 계획 대비 수정 사항

4. 데모

 - 프로젝트 일부분을 직접 시연 

 - 강의실에서 직접 시연이 어려운 부분은 동영상으로 시연 가능

5. 향후 개발 일정

	5-1
		채팅 기능 추가
			websocket을 이용하여 채팅 서비스 구현 예정
	
	5-2
		요금 예측 기능 추가
			단순히 " 현재값 / 오늘까지의_일수 * 이번달_총_일수 "로 계산할 예정

6. 주요 애로사항 (해결하지 못한)

	6-1
		LoRa와 LoRa Wan을 사용하려고 하였으나, ttn console이 docker에서 돌아가지 않아 해당 기술을 사용하지 못함.
		해당 기술은 이전에 해본 선배에게 자문을 구할 예쩡

	6-2
		

7. 해결한 애로사항 (선택사항)

    - 이슈: 어떤 이슈가 발생?
    - 문제: 무엇이 문제였는가?
    - 어떻게 문제를 해결했는가?
    - 문제를 해결하면서 배운점

	7-1
		카카오 로그인 시 
		redirect uri의 작동 방식을 이해하지 못함
		redirect uri를 서버 주소 대신 localhost로 변경. 이 이후, 웹사이트의 페이지로 잘 redirect 됨
		공식 문서를 참고하는것이 중요하다는 것을 깨달음. 공식 문서의 각 요소가 무엇을 의미하는지 정확히 파악해야한다는 것을 깨달음
		
	7-2
		fastapi를 kill 명령어로 종료하였을 때 해당 port 및 ip를 사용중이라고 뜸
		kill 명령어를 하더라도 uvicorn 자체에서 port를 사용중이었음.
		https://stackoverflow.com/questions/64588486/address-already-in-use-fastapi
		kill 명령어를 쓰더라도 port를 반환하지 않는 경우가 생길 수 있다는 것을 배웠음

	7-3
		다른 ip에서 REST API를 이용하여 데이터를 요구할 때 cors 오류가 떴음. 
		cors 설정을 localhost만 접근 가능하도록 하여 문제 발생
		모든 ip에서 REST API를 이용할 수 있도록 cors 정책 변경
		참고 자료에서는 cors-allow_origin을 localhost로만 하였던 것을 그대로 사용하였던 것이 문제. 공식 문서를 참고하는것이 중요하다는 것을 깨달음

8. 기타 발표가 필요하다고 판단되는 내용 (선택사항)

