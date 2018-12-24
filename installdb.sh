sudo -u postgres dropdb crucita_fashion >> /dev/null
sudo -u postgres dropuser crucita_fashion >> /dev/null
sudo -u postgres createuser crucita_fashion
sudo -u postgres createdb crucita_fashion
sudo -u postgres psql << EOF
alter user crucita_fashion with encrypted password 'crucitafashion';
alter role crucita_fashion set client_encoding to 'utf8';
alter role crucita_fashion set default_transaction_isolation to 'read committed';
alter role crucita_fashion set timezone to 'utc';
alter role crucita_fashion createdb;
grant all privileges on database crucita_fashion to crucita_fashion ;\q
EOF