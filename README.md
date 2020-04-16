# IAM Key Watchman

## Overview

This is intended as an exercise in building a lambda function that will regularly check for and delete/disable all IAM keys which have not be used in the last 90 days.

## Resources
The following resources are deployed and used by this solution:
* IAM Role (for execution of the Lambda)
* IAM Policy (for scoping of the IAM role to least privileges)
* CloudWatch Event Rule (this is the cron that executes the lambda)
* Lambda (where the magic happens)
* SNS Topic (for notification of actions performed by the Lambda)

## Assumptions
The following assumptions have been made for this solution:
* The execution speed of this is unimportant (i.e. stays single threaded)
* The IAM keys in scope are only within the AWS account the Lambda is executed at (no cross-account mgmt)
* Only using Python modules available within the default Python 3.8 env

## Configuration

Configuration of the solution is drive by variables defined in the `terraform.tvvars` file.
* AWS_REGION
  * Desc: The AWS region that all the AWS resources will be deployed
  * Valid Values:
    * An AWS region
  * Default Value: us-west-2
* EXPIRATION_IN_DAYS
  * Desc: The number of days since last usage when an IAM key is considered expired
  * Valid Values:
    * Integer
  * Default Value: 90
* FREQUENCY
  * Desc: The frequency at which the solution should be executed
  * Valid Values:
    * Any format (cron or rate) supported by CloudWatch
      * https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
  * Default Value: `rate(1 day)`
* IGNORE_DISABLED
  * Desc: If disabled IAM keys should be ignored for checking expiration
  * Valid Values:
    * True / False
  * Default Value: True
* LOG_LEVEL
  * Desc: The logging level of execution of the function
  * Valid Values: `[DEBUG|INFO|WARNING|ERROR|CRITICAL]`
  * Default Value: `INFO`
* REMEDIATION_ACTION
  * Desc: What to do when an expired key is identified
  * Valid Values:
    * `NOTIFY`: Only send a notification, but don't change anything
    * `DISABLE`: Disable the IAM key and send a notification
    * `DELETE`: Delete the IAM key and send a notification
  * Default Value: `NOTIFY`

## Deployment to AWS

The deployment of the lambda and associated code is driven by Terraform:

```bash
terraform init

```

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests.

```bash
AWS$ pip install pytest pytest-mock --user
AWS$ python -m pytest tests/ -v
```

## Cleanup

To delete the solution, use the power of Terraform

```bash
terraform destroy
```

## Improvements

Before using this in a real-world environment, I would highly suggest improvements such as:
* There's significant opportunity for more granular error checking, but I'm assuming that if you can do one thing, you can do them all...
* Push the TF state somewhere external (S3, Terraform Enterprise, etc...)
* You should probably subscribe something to the SNS topic
* This has no input validation.  There can always be better input validation
* Speed up by using multi-proc


## General Comments/Rants
* A cheat way to do this much more simply would have been to generate a credential report, which dumps of a CSV of all this data.  Loop over and process
* This isn't auditing the root user's keys, because:
  1. We can't perform any actions against it
  2. If you have any IAM keys for your root user, you need to be banished from AWS, never to use the cloud again...
* In general, I try to follow the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html), but I've also never been judged on my adherence to it.  I'm sure I'm way off the mark, but until someone corrects me I can stay blissfully ignorant...
* There are some aspects of pylint that we don't like (We hates it, my precioussss!  We hates it!), but thats what modern IDEs (my poison of choice is PyCharm) to reform on the fly.  That's not to say there still can't be vestigates of this in the code...
  * 4 space indent (two fat for me; I prefer 2 space)
  * 80 char line limit (I haven't used a Hercules monochrome monitor in 20 years.  I'm pretty sure there's more space in my 4k monitor...)
  

