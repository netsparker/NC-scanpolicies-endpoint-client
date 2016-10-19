import requests

API_ROOT = "https://www.netsparkercloud.com/api/1.0/%s"
USER_ID = "NETSPARKER CLOUD API USER ID GOES HERE"
API_TOKEN = "NETSPARKER CLOUD API TOKEN GOES HERE"
AUTH = (USER_ID, API_TOKEN)

def list_policies():
    endpoint_url = API_ROOT % "scanpolicies/list"
    response = requests.get(endpoint_url, auth=AUTH)
    json_response = response.json()

    print "\nExisting Policies:"
    for policy in json_response["List"]:
        print "%s: %s - %s" % (policy["Id"], policy["Name"], policy["Description"])
    print ""


def get_policy_by_name(name):
    endpoint_url = API_ROOT % "scanpolicies/get"
    response = requests.get(endpoint_url, params={'name':name}, auth=AUTH)
    json_response = response.json()
    return json_response


def get_policy_by_id(id):
    endpoint_url = API_ROOT % ("scanpolicies/get/%s" % id)
    response = requests.get(endpoint_url, auth=AUTH)
    json_response = response.json()
    return json_response


# This one actually clones Default Security Checks
def new_policy(name, description):
    default_policy_json = get_policy_by_name("Default Security Checks")
    default_policy_json["Name"] = name
    default_policy_json["Description"] = description
    default_policy_json["IsShared"] = False

    endpoint_url = API_ROOT % "scanpolicies/new"
    response = requests.post(endpoint_url, json=default_policy_json, auth=AUTH)
    return response.json()


# Implemented as update policy example
def rename_policy(name, new_name):
    policy_json = get_policy_by_name(name)
    policy_json["Name"] = new_name

    endpoint_url = API_ROOT % "scanpolicies/update"
    response = requests.post(endpoint_url, json=policy_json, auth=AUTH)
    return response.json()


def delete_policy(name):
    endpoint_url = API_ROOT % "scanpolicies/delete"
    response = requests.post(endpoint_url, headers={'Content-Type':'application/json'}, data=`name`, auth=AUTH)
    return response.json()

def main():
    list_policies()

    # Get default policy by name
    print "Getting Default Security Checks by name"
    print get_policy_by_name("Default Security Checks")

    # Get default policy by id
    print "\nGetting Default Security Checks by id"
    print get_policy_by_id("b2018666-2a01-e411-976c-0a45dbb897e8")

    # Create (clone) a new policy based on default policy
    print "\nCloning Default Security Checks: ",
    new_policy("Test Policy", "Test description")
    print "Ok"

    list_policies()

    print "\nRenaming newly created policy: ",
    rename_policy("Test Policy", "Test Policy 1")
    print "Ok"

    list_policies()

    print "\nRemoving newly created policy: ",
    print delete_policy("Test Policy 1")

    list_policies()


if __name__ == '__main__':
    main()