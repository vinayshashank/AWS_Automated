import boto3

ec2 = boto3.client('ec2')
response = ec2.run_instances(
            ImageId='ami-0b69ea66ff7391e80',
            InstanceType='t2.micro',
            KeyName='mykeypair',
            MinCount=1,
            MaxCount=1)

print(response)