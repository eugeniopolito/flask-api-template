if [ "$(ls -A 'migrations')" ]; then
  echo "Migration directory exists."
else
  echo "Initializing DB"
  flask db init
fi

echo "Migrating DB"
flask db migrate

echo "Upgrading DB"
flask db upgrade

echo "Starting Flask..."
flask run
