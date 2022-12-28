from aws_cdk import (
    # Duration,
    Stack,
    aws_elasticache as elasticache,
    aws_lambda as _lambda,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_ssm as ssm,
    CfnOutput, Duration,
)
import json
import time

from constructs import Construct

class LambdaElasticacheStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #======================================================
        # Infrastructure Wide Deployment
        #======================================================
        
        # Get current time, used to force generation of new services versions on infrastructure update.
        timestamp_str = str(int(time.time()))
        
        # VPC        
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=1,
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC,cidr_mask=24),
                ec2.SubnetConfiguration(name="private",subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,cidr_mask=24)
            ]
        ) 
        
        # Security Groups
        redis_sec_group = ec2.SecurityGroup(
            self, "redis-sec-group",security_group_name="redis-sec-group", vpc=vpc, allow_all_outbound=True,
        )   

        private_subnets_ids = [ps.subnet_id for ps in vpc.private_subnets]

        redis_subnet_group = elasticache.CfnSubnetGroup(
            scope=self,
            id="redis_subnet_group",
            subnet_ids=private_subnets_ids,  # todo: add list of subnet ids here
            description="subnet group for redis"
        )

        #lambda_redis_role = iam.Role.from_role_name()
        
        # Elasticache for Redis cluster
        redis_cluster = elasticache.CfnCacheCluster(
            scope=self,
            id="redis_cluster",
            engine="redis",
            cache_node_type="cache.t3.small",
            num_cache_nodes=1,
            cache_subnet_group_name=redis_subnet_group.ref,
            vpc_security_group_ids=[redis_sec_group.security_group_id],
            port=55000,  
        )
        
        redis_endpoint = redis_cluster.attr_redis_endpoint_address
        redis_port = redis_cluster.attr_redis_endpoint_port
        
        ssm.CfnParameter(
            scope=self, 
            id="redis_endpoint",
            type="String",
            name="redisendpoint",
            value=redis_endpoint,
        )
        
        ssm.CfnParameter(
            scope=self, 
            id="redis_port",
            type="String",
            name="redisport",
            value=redis_port,
        )
        
        #======================================================
        # Functions
        #======================================================

        # Create the lambda function
        service_lambda = _lambda.Function(self,
            #Name of the function 
            id="_lambda",
            #This is critical to force generation of a new version of the function
            description=timestamp_str,
            #Choose the runtime
            runtime=_lambda.Runtime.FROM_IMAGE,
            #File and function of the handler
            handler=_lambda.Handler.FROM_IMAGE,
            #Code location
            code=_lambda.Code.from_asset_image("lambda/increment"),
            #Increase the timeout from default 5s
            timeout=Duration.seconds(30),
            #Enable x-ray tracing
            tracing=_lambda.Tracing.ACTIVE,
            #Increase memory from default 128MB
            memory_size=512,
        )
        
        version = service_lambda.current_version

     # service_lambda_alias = _lambda.Alias(self,
     #     id="_lambda_alias",
     #     alias_name="service_at_" + timestamp_str,
     #     version=version,
     #     description="Lastest version of " + id,
     #     on_success=on_success,
     #     on_failure=dlq_sqs_destination,
     #     provisioned_concurrent_executions=3,
     # )
        
        #======================================================
        # Console Outputs
        #======================================================
        
        CfnOutput(self, "Stack region", value=self.region)
        CfnOutput(self, "Redis Cluster Endpoint", value=redis_endpoint)
        
        
