# hanghae99-chapter1-9th
항해99-웹미니프로젝트-9조


# 동네 빵집

세상엔 맛잇는 빵집이 너무 많고 ~ 하늘아래 같은 빵맛은 없다 !

빵순이 빵돌이들을 위해 우리동네 빵 맛집을 추천해드립니다.


# 1. 제작기간 & 팀원 소개

- 2022년 3월 7일 ~ 2022년 3월 10일 (총4일)

- 4인 1조 팀 프로젝트

     황인호 : 각자 맡은 기능 작성

     김정태 : 각자 맡은 기능 작성
  
     이덕행 : 각자 맡은 기능 작성

     이미란 : 검색기능, 검색필터 기능




# 2. 사용 기술 


- Back-end

     python 3

     Flask (python frame work)

     MongoDB


- Front-end

     bootstrap

     bulma

     JQuery

     AJAX

     AWS EC2




# 3. 핵심기능

- 회원가입 및 로그인

     구현 방법 작성

- 서브페이지 기능

     구현 방법 작성


- 추천 빵집 포스팅 기능 (사진 파일 업로드 기능)

     구현 방법 작성


- 지도 기능

     구현 방법 작성


- 검색 필터 및 검색 기능

     클라이언트에서 입력 데이터를 전달하기 위해서 query parameter를 url에 덧붙여서 전달하였습니다.
     서버에서는 클라에서 보내준 키워드를 받아 빵집 전체 목록 중 빵집 이름과 일치하는 결과를 찾아내고,
     딕셔너리 형태로 만들어 전달하였습니다.



# 4. 실행 정보

 - 동영상 파일 등록




# 5. 프로젝트 과정 중 이슈 사항

Q. 검색 기능 구현 중 해당 검색어와 일치하는 데이터만 찾아서 불러와야 하는데 어떤 식으로 검색어 정보를 서버에 전달할 수 있을까?

A. 처음에는 서버에서 전체 목록을 불러와서 클라이언트에서 filter함수를 사용해 검색어와 일치하는 데이터를 includes 하고 있는 정보를 리스팅 하려고 시도했었는데, 콘솔에 찍는 것까진 성공했으나, 실제로 이걸 리스트로 보여주는 방법을 찾지 못하였습니다. 그래서 서버에서 전체 데이터를 불러오는 것은 비효율적이라는 기술매니저님의 조언을 듣고 Query String 방법으로 시도를했고, 해결하였습니다. 
 검색 필터 기능은 구글링 끝에 getElementById, getElementsByClassName라는 내장함수를 알게되어 구글에 계신 선생님들의 조언대로 구현해 보았습니다 검색 기능 구현시 indexOf라는 함수를 사용하는 것 같은데 이부분은 조금 더 사용법 숙지가 필요할 것 같습니다. 
