import boto3

def scan_s3_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        print(f"Scanning S3 bucket {bucket_name}")
        # Check if the bucket is publicly accessible
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                print(f"Bucket {bucket_name} is publicly accessible.")
                break
        # Check if the bucket has weak ACLs
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        for statement in policy['Statement']:
            if statement['Effect'] == 'Allow' and statement['Principal'] == '*':
                print(f"Bucket {bucket_name} has a policy that allows access from any user or account.")
                break

if __name__ == '__main__':
    scan_s3_buckets()
