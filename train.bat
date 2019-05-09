@ECHO OFF
ECHO Setting environment
mlagents-learn settings.yaml --run-id=%1 --env=%2 --train