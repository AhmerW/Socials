@echo off
set location=Ahmer
cd c:/users/%location%

title ak-zookeeper
cd kafka 
.\bin\windows\kafka-server-start.bat .\config\server.properties

