### Configure constants
IP="<domain>"
SUBSCRIBER_CERTS_DIR="<subscriber certs destination directory path>"
COUNTRY="<county code>"
CITY="<your city>"

### do not touch
SUBJECT_CA="/C=$COUNTRY/ST=$CITY/L=$CITY/O=IoT/OU=CA/CN=$IP"
SUBJECT_SERVER="/C=$COUNTRY/ST=$CITY/L=$CITY/O=IoT/OU=Server/CN=$IP"
SUBJECT_CLIENT="/C=$COUNTRY/ST=$CITY/L=$CITY/O=IoT/OU=Client/CN=$IP"

function generate_CA () {
   echo "$SUBJECT_CA"
   openssl req -x509 -nodes -sha256 -newkey rsa:2048 -subj "$SUBJECT_CA"  -days 36500 -keyout ca.key -out ca.crt
}

function generate_server () {
   echo "$SUBJECT_SERVER"
   openssl req -nodes -sha256 -new -subj "$SUBJECT_SERVER" -keyout server.key -out server.csr
   openssl x509 -req -sha256 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 36500
}

function generate_client () {
   echo "$SUBJECT_CLIENT"
   openssl req -new -nodes -sha256 -subj "$SUBJECT_CLIENT" -out client.csr -keyout client.key
   openssl x509 -req -sha256 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 36500
}

function copy_keys_to_broker () {
   sudo cp ca.crt /etc/mosquitto/certs/
   sudo cp server.crt /etc/mosquitto/certs/
   sudo cp server.key /etc/mosquitto/certs/
}

function copy_keys_to_subscriber () {
   sudo cp ca.crt $SUBSCRIBER_CERTS_DIR
   sudo cp client.crt $SUBSCRIBER_CERTS_DIR
   sudo cp client.key $SUBSCRIBER_CERTS_DIR
}

generate_CA
generate_server
generate_client
copy_keys_to_broker

read -r -p "Copy client certs to: $SUBSCRIBER_CERTS_DIR? [y/N]" response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    copy_keys_to_subscriber
fi


