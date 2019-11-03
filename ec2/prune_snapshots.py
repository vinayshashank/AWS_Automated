import boto3


def lambda_handler(event, context):

    account_id = boto3.client('sts').get_caller_identity()['Account']
    ec2_client = boto3.client('ec2')

    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    for region in regions:

        # if region in ['us-east-1', 'us-west-2']:

        print(f'Region: {region}')

        ec2_client = boto3.client('ec2', region_name=region)
        snapshots = ec2_client.describe_snapshots(OwnerIds=[account_id])['Snapshots']

        snapshots.sort(key=lambda x: x['StartTime'])

        snapshots = snapshots[:-5]

        for snapshot in snapshots:
            try:
                snap_id = snapshot['SnapshotId']
                ec2_client.delete_snapshot(SnapshotId=snap_id)
                print(f'Snapshot {snap_id} is deleted')
            except Exception:
                print(f'Snapshot {snap_id} is in use')



