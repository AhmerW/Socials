@echo off
set location=Ahmer
cd c:/users/%location%

title ak-zookeeper
cd kafka 
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties