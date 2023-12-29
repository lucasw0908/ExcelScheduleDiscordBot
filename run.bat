@echo off

:insq
SET /P install="Do you want to install pip packages?(y/n): "

IF "%install%" EQU "y" GOTO ins
IF "%install%" EQU "n" GOTO setq
ECHO Plaese enter y or n.
GOTO insq

:ins
pip install -r requirements.txt

:setq
SET /P set_token="Do you want to set token?(y/n): "
IF "%set_token%" EQU "y" GOTO reset
IF "%set_token%" EQU "n" GOTO runpy
ECHO Plaese enter y or n.
GOTO setq

:reset
SET /P token="Enter your bot token: "
IF [%token%]==[] ECHO This is not a bot token.& GOTO reset
ECHO %token%>x& FOR %%? IN (x) DO SET /A tokenlength=%%~z? - 2& DEL x
ECHO %tokenlength%
IF %tokenlength% NEQ 72 ECHO This is not a bot token.& GOTO reset
ECHO TOKEN=%token% > bot/.env
ECHO Bot token is setted.

:runpy
python main.py

PAUSE