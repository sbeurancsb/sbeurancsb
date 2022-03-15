import requests as r
import pandas as p
import re
import json
import subprocess


filename = "cadi_users.xlsx"
collName = 'emails'
xlsx = p.read_excel(filename)
arr = xlsx[collName].tolist()
print(arr)
idls = []
salesOrg = {
  "DK": "A001",
  "UK": "B001",
  "NO": "C001",
  "SE": "D001",
  "FI": "E001",
  "FR": "F001",
  "DE": "L001"
}
roles = {
  "regular_ont": "APP_ONT_USER",
  "regular_oft": "APP_OFT_USER",
  "super_user_ont": "APP_ONT_SUP_USER",
  "super_user_oft": "APP_OFT_SUP_USER",
  "ordering": "APP_ORDER_USER"
}
action = {
  "add": "ENABLE",
  "remove": "DISABLE"
}

actionInput = input("Please choose if you want to add or remove a role \n add \n remove \n")
if actionInput in action:
   actionChosen = (action[actionInput])
else:
   print("Dont exist")

rolesInput =  input("Please choose the role to assign: \n regular_ont \n regular_oft \n super_user_ont \n super_user_oft \n ordering \n")
if rolesInput in roles:
   roleChosen = (roles[rolesInput])
else:
   print("Dont exist")

salesOrgInput =  input("Please choose the Sales Org: \n DK \n UK \n NO \n SE \n FI \n FR \n DE \n")
if salesOrgInput in salesOrg:
   salesOrgChosen = (salesOrg[salesOrgInput])
else:
   print("Dont exist")

for i in range(len(arr)):
    response = r.get("http://localhost:8081/services/users?type=INTERNAL&email={user}".format(user = arr[i]))
    data = response.json()
    idls.append(data.get("users")[0].get("eid"))
    
print(idls)

for i in range(len(idls)):
     url = ("http://localhost:8081/services/users/{id}/roles?rolePlacement=salesOrg&grantor=28f65d25-3828-4c17-85f7-4a718648e3d4&operation={actionChosen}").format(id = idls[i], actionChosen = (action[actionInput]))
     data = {"role": {"applicationCode": "CADI","roleName": roleChosen},"salesOrgCode": salesOrgChosen}
     addRole = r.post(url, json=data)
     print(addRole.status_code)
     print(addRole.json)
     
     
     

    
 