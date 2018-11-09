#!/usr/bin/env bash

declare -A projects=(
    [test_chatsrv-frontend]="172.20.20.3"
    [test_chatsrv-core]="172.20.20.5"
    [test_chatsrv-storage]="172.20.20.5"
    [test_chatsrv-push]="172.20.20.5"
)

token="xxxxxxxxx"

for project in ${!projects[@]}; do
    client="${projects[${project}]}"
    curl -w '\n' 'http://deploy.ixiaochuan.cn/deploy' -H "Cookie: remember_token=${token};" --data "operation=update&project=${project}&client=${client}" --compressed --silent
done
