#!/usr/bin/env python3
import os
import json
import aws_cdk as cdk

from lambda_elasticache.lambda_elasticache_stack import LambdaElasticacheStack


app = cdk.App()

with open("secrets.json") as config_file:
    config = json.load(config_file)

app = cdk.App()
env_ = cdk.Environment(account=config['account'], region=config['region'])

LambdaElasticacheStack(app, "LambdaElasticacheStack", env=env_)

app.synth()
