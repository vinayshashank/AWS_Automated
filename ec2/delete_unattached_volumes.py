import boto3


def lambda_handler(event, context):

    ec2_client = boto3.client('ec2')

    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in regions:
        # if region in ['us-east-1', 'us-west-2']:

        ec2 = boto3.resource('ec2', region_name=region)
        print(f'Region: {region}')

        volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])

        for volume in volumes:
            volume.delete()
            print(f'{volume.id} deleted')
