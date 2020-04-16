from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import boto3
import traceback
import sys
from botocore.exceptions import ClientError

# Constants, Global Vars, Environment Vars
#######################################################################################################################
_PRINT_STACKTRACE_ON_ERROR = True
_LOG_LEVEL = os.environ['LOG_LEVEL']
_REMEDIATION_ACTION = os.environ['REMEDIATION_ACTION']
_EXPIRATION_IN_DAYS = os.environ['EXPIRATION_IN_DAYS']
_logger = logging.getLogger(__name__)
_logger.setLevel(_LOG_LEVEL)
logging.basicConfig(format='%(asctime)s - %(message)s', level=_LOG_LEVEL)


# Functions
#######################################################################################################################
def _get_iam_keys():
  """Get all the IAM keys within the AWS Account

  Args:
    None

  Returns:
    A list of dictionaries containing all access keys, their associated user's name, key status, and the last time they were used.
    [{
      'UserName': string,
      'AccessKeyId': string,
      'Status': string,
      'LastUsed': Datetime
    }]

  Raises:
    ClientError: Unable to access or perform action against an AWS resource
  """
  try:
    _logger.debug('Get IAM Keys')
    _iam_client = boto3.client(service_name='iam')
    _client_args = {'MaxItems': 100}
    _iam_keys = []
    while True:
      _users_response = _iam_client.list_users(**_client_args)
      for _user in _users_response['Users']:
        _logger.debug('User: {0} - Get Keys'.format(_user['UserName']))
        try:
          _keys_response = _iam_client.list_access_keys(UserName=_user['UserName'])
          for _key in _keys_response['AccessKeyMetadata']:
            try:
              _logger.debug('User: {0} Key: {1} - Get Last Used'.format(_user['UserName'], _key['AccessKeyId']))
              _key_last_used_response = _iam_client.get_access_key_list_used(AccessKeyId=_key['AccessKeyId'])
              _iam_keys.append({
                'UserName': _user['UserName'],
                'AccessKeyId': _key['AccessKeyId'],
                'Status': _key['Status'],
                'LastUsed': _key_last_used_response['AccessKeyLastUsed']['LastUsedDate']
              })
            except:
              _logger.error('Error in Key: {0}'.format(_key['AccessKeyId']))
              raise
        except:
          _logger.error('Error in User: {0}'.format(_user['UserName']))
          raise
  except:
    _logger.error('Something failed getting User IAM keys')
    raise
  return _iam_keys


def _determine_key_actions(all_iam_keys):
  """Given a list of keys, determine if any actions should be done to each key

  Args:
    A list of dictionaries containing all access keys, their associated user's name, key status, and the last time they were used.

  Returns:
    A list of dictionaries containing all access keys, their associated user's name, and a list of actions that need to occur for the key (Notify, Disable, Delete)

  Raises:
    AccessError: Unable to access or perform action against an AWS resource
  """
  return


def _execute_actions(key_actions):
  """Perform defined actions against a list of keys

  Args:
    A list of dictionaries containing all access keys, their associated user's name, and a list of actions that need to occur for the key (Notify, Disable, Delete)

  Returns:
    None

  Raises:
    AccessError: Unable to access or perform action against an AWS resource
  """

  return


# Main function
#######################################################################################################################
def lambda_handler(event, context):
  _logger.info('event:{}'.format(event))
  # {'version': '0', 'id': 'f04bcde6-2961-8b24-8015-07c936b8f183', 'detail-type': 'Scheduled Event', 'source': 'aws.events', 'account': '187960249655', 'time': '2020-04-15T00:42:31Z', 'region': 'ca-central-1', 'resources': ['arn:aws:events:ca-central-1:187960249655:rule/myTrigger1'], 'detail': {}}
  _logger.info('context:{}'.format(context))

  try:
    _all_iam_keys = _get_iam_keys()
    _key_actions = _determine_key_actions(_all_iam_keys)
    _execute_actions(_key_actions)
  except Exception as _err:
    _logger.critical('Unexpected error in lambda handler: {0}'.format(_err))
  if _PRINT_STACKTRACE_ON_ERROR:
    traceback.print_exc(file=sys.stderr)
  return
