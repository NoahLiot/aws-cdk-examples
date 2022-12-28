import redis
import os
import boto3


def handler(event, context):
    """
    This function connect Elasticache for Redis, tries to read the incremental value to increment, 
    and creates it if it does not exists. Finally it returns the incremented value back to the requester.
    """
        
    ssm = boto3.client('ssm', region_name="ap-south-1",)
    parameter = ssm.get_parameter(Name='redisendpoint', WithDecryption=True)
    print(parameter['Parameter']['Value'])

    # redis_handler =  redis.Redis(host='localhost',
    #                              port=55000,
    #                              socket_connect_timeout=10,
    #                              password='redispw')
    # 
    # redis_handler.incr('mycounter')
    # counter_state = redis_handler.get('mycounter')

    return "Fetched value from memcache: "

# redis_handler =  redis.Redis(host='localhost',
#                                 port=55000,
#                                 socket_connect_timeout=10,
#                                 password='redispw')
# 
# redis_handler.incr('mycounter')
# print(redis_handler.get('mycounter'))