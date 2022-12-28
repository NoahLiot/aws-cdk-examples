<!--BEGIN STABILITY BANNER-->
---

![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

> **This is a stable example. It should successfully build out of the box**
>
> This example is built on Construct Libraries marked "Stable" and does not have any infrastructure prerequisites to build.
---
<!--END STABILITY BANNER-->

# Overview

This CDK examples build an [Amazon ElastiCache for Redis](https://aws.amazon.com/elasticache/redis/) cluster and uses it to create a very simple data centric orchestration for [AWS Lambda](https://aws.amazon.com/lambda/) functions. We are using Redis as it gots Atomic writes, which ensure that a workflow cannot end up in an invalid state while providing thousands of write per second scalability and sub-millisecond latency.

# Build/Deploy

## Building the Docker image of the service independently

The following guidance is for any of the Lambda service.
If you run `runlocally.sh` you will build a Lambda container image and run it locally on port `9000`.
You can then use `calllocally.sh` to call that Lambda function. In order for the function to run, you will need to run Redis locally (I recommend using the [official Docker image](https://hub.docker.com/_/redis)).

[TODO] Add what a call and response would look like.

## Deploying the construct using CDK

To run the stack you will need to add a `secrets.json` file in the root of the `eventbridge-lambda-construct`. This file should contains the following information:

    {
        "account": "YOUR-ACCOUNT-NUMBER",
        "region": "YOUR-REGION"
    }

Once done, to build the stack simply run `cdk deploy`

## Test the services

[TODO] Complete that Section

# Next Steps

Using this construct, you can now add logic in you services to route the response payloads to another service using the `source` field in the messages, and hence build service choregraphy without having to manage endpoints and scalability in the service logic.

# Cleanup

To remove the Stack, simply run `cdk destroy`.
