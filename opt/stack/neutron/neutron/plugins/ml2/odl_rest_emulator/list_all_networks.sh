# after this curl command, ODL log will not be appended because they are not the same service. One is curl, one is neutron request
# we need to emulaste neutron request, not the curl

curl --user admin:admin -H "Accept: application/json" "http://localhost:8181/controller/nb/v2/neutron/networks" | python -m json.tool
