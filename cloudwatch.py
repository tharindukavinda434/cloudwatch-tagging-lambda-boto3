import json
import boto3
from  pprint import pprint

def lambda_handler(event, context):
  
  regions = ["eu-west-1","eu-west-2","us-east-1","us-east-2"]
  #remove ,"us-east-2" when in LE accounts
  
  tagged_now = 0
  cant_tag   = 0
  alrdy_tagged =0
  all_cloudwatch_count = 0
  
  for region in regions:
    
    cloud_w_client = boto3.client('logs',region_name=region)
    paginator = cloud_w_client.get_paginator('describe_log_groups')
    response_iterator = paginator.paginate()
    
    for page in response_iterator:
      for i in page['logGroups']:
        all_cloudwatch_count += 1
        cloud_watch_arn = i['arn']
        cloud_watch_name = i['logGroupName']
        print(i)
        #print(cloud_watch_arn)
        #client = boto3.client('logs')
        response = cloud_w_client.list_tags_log_group(logGroupName=cloud_watch_name)
        
        flag = 0 
        for tagkey in response['tags']:
          if ( tagkey == 'map-migrated'  ):
            flag = 1
            alrdy_tagged += 1
            
        if ( flag == 0  ):
          
          try:
            response = cloud_w_client.tag_log_group(logGroupName=cloud_watch_name,tags={'map-migrated': 'd-server-00hnvedb9bgt7t'})
            tagged_now += 1
            
          except Exception as e:
            print (e)
            cant_tag +=1
            
  print('all cloud watch  count',all_cloudwatch_count)
  print('already tagged count' ,alrdy_tagged )
  print('tagged from this attempt',tagged_now)
  print('refused to tag',cant_tag )
