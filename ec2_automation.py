import boto3
import time

AMI_ID = "ami-0c02fb55956c7d316" 
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "trial-ami" 
SECURITY_GROUP_ID = "sg-060096e65b968392b"  
REGION = "us-east-1"

ec2 = boto3.resource('ec2', region_name=REGION)

def launch_instance():import boto3
import time

AMI_ID = "ami-0c02fb55956c7d316" 
INSTANCE_TYPE = "t2.micro"
KEY_NAME = "trial-ami" 
SECURITY_GROUP_ID = "sg-060096e65b968392b"  
REGION = "us-east-1"

ec2 = boto3.resource('ec2', region_name=REGION)

def launch_instance():
    instance = ec2.create_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        SubnetId='subnet-00f87e05c8a3570ca',
        IamInstanceProfile={'Name': 'MyEC2SSMInstanceProfile'},
    )[0]

    instance.wait_until_running()
    instance.reload()
    print(f"Instance {instance.id} is running at {instance.public_dns_name}")
    time.sleep(10)
    return instance.id, instance.public_dns_name

def get_output(instance_id):
    ssm = boto3.client('ssm', region_name=REGION)
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [
            'echo "Starting script..."',
            'sleep 10',
            'echo "Finished after sleep"'
        ]}
    )
    command_id = response["Command"]["CommandId"]

    while True:
        time.sleep(2)
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
        if output['Status'] in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
            break

    return {
        "stdout": output.get("StandardOutputContent", ""),
        "stderr": output.get("StandardErrorContent", ""),
        "status": output["Status"]
    }


def terminate_instance(instance_id):
    instance = ec2.Instance(instance_id)
    instance.terminate()
    instance.wait_until_terminated()
    print(f"Instance {instance_id} terminated.")
