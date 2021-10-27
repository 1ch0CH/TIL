# Docker
## Docker 사용 시 sudo 없이 사용하기

> sudo usermod -aG docker [현재 사용자]
- usermod : 사용자 속성을 변경하는 명령어
- G(== --groups) : 새로운 그룹을 말한다
- a(== --append) : 다른 그룹에서 삭제없이 G 옵션에 따른 그룹에 사용자를 추가한다.

