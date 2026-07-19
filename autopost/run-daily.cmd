@echo off
REM 오늘살림 자동발행 — Windows 작업 스케줄러에 이 파일을 매일 원하는 시각으로 등록
cd /d "%~dp0"
node poster.cjs --due >> run.log 2>&1
