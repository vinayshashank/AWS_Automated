import boto3
from datetime import datetime


def lambda_handler(event, context):

    ec2_client = boto3.client('ec2')

    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in regions:

        # if region in ['us-east-1', 'us-west-2']:

        ec2 = boto3.resource('ec2', region_name=region)
        print(f'Region: {region}')

        instances = ec2.instances.filter(Filters=[{'Name': 'tag:backup', 'Values': ['true']}])

        for instance in instances:
            for volume in instance.volumes.all():
                snapshot = volume.create_snapshot(Description=f'Snapshot taken at {datetime.utcnow()}')
                print(f'Created snapshot for {volume.id} attached to {instance.id} : {snapshot.id}')
