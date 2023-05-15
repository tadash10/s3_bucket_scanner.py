import boto3

def list_s3_buckets():
    """
    Returns a list of all S3 bucket names in the current AWS account.
    """
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def is_bucket_public(bucket_name):
    """
    Returns True if the specified S3 bucket is publicly accessible, False otherwise.
    """
    s3 = boto3.client('s3')
    acl = s3.get_bucket_acl(Bucket=bucket_name)
    for grant in acl['Grants']:
        if 'URI' in grant['Grantee'] and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
            return True
    return False

def has_weak_acl(bucket_name):
    """
    Returns True if the specified S3 bucket has weak Access Control Lists (ACLs), False otherwise.
    """
    s3 = boto3.client('s3')
    policy = s3.get_bucket_policy(Bucket=bucket_name)
    for statement in policy['Statement']:
        if statement['Effect'] == 'Allow' and statement['Principal'] == '*':
            return True
    return False

def generate_bucket_report(bucket_name):
    """
    Generates a report of security issues for the specified S3 bucket.
    """
    report = []
    if is_bucket_public(bucket_name):
        report.append("Bucket is publicly accessible.")
    if has_weak_acl(bucket_name):
        report.append("Bucket has a policy that allows access from any user or account.")
    return report

def scan_s3_buckets():
    """
    Scans all S3 buckets in the current AWS account and generates a report of security issues.
    """
    bucket_names = list_s3_buckets()
    for bucket_name in bucket_names:
        print(f"Scanning S3 bucket {bucket_name}")
        report = generate_bucket_report(bucket_name)
        if report:
            print(f"Security issues found for bucket {bucket_name}:")
            for issue in report:
                print(f"  - {issue}")

if __name__ == '__main__':
    scan_s3_buckets()
