#!/bin/bash
# chmod u+x run_db_backup.sh

# Local .env
if [ -f .env ]; then
  # Load Environment Variables
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
  echo -e "\e[1;31mError: File .env not found \e[0m\n"
  exit 1
fi

DOCKER_DB_BACKUP_FULLPATH="$(echo $DOCKER_DB_BACKUP_DIRECTORY | tr -d '"')/$(date '+%Y-%m-%d_%H-%M')"

echo -e "\n\e[1mBacking up db (container $(echo $DOCKER_DB_CONTAINER_NAME | tr -d '"')) in '\e[4m$(echo $DOCKER_DB_BACKUP_FULLPATH | tr -d '"')\e[0m\e[1m'... \e[0m\n"

docker exec -it \
  --user "$(id -u):$(id -g)" \
  $(echo $DOCKER_DB_CONTAINER_NAME | tr -d '"') \
  influxd backup -database $(echo $INFLUXDB_DB | tr -d '"') \
  $(echo $DOCKER_DB_BACKUP_FULLPATH | tr -d '"') || exit 1

# echo -e "\n\e[1mCopying backup from container to local machine... \e[0m\n"
# docker cp $docker_db_container_name:$backup_path $HOME || exit 1

echo -e "\n\e[1;32m -> Ok! \e[0m\n"
