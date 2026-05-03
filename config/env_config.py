import os
from config.validators import validate_env_vars

class StackEnvConfig:
    def __init__(self, project_name, environment, aws_account):
        validate_env_vars(
            "PROJECT_NAME",
            "PROJECT_OWNER",
            "AWS_APATITE_PROD_ACCOUNT_ID",
            "AWS_REGION",
            "DOMAIN_NAME",
            "S3_WEBSITE_REGION",
            "ACM_CERTIFICATE_ARN",
            "S3_WEBSITE_PRODUCTION_BUCKET_NAME",
            "S3_WEBSITE_DEV_BUCKET_NAME",
            "S3_WEBSITE_TEST_BUCKET_NAME",
            "ACM_VALIDATION_APATITE_IO_NAME",
            "ACM_VALIDATION_APATITE_IO_VALUE",
            "ACM_VALIDATION_WEBSITE_DEV_NAME",
            "ACM_VALIDATION_WEBSITE_DEV_VALUE",
            "ACM_VALIDATION_WEBSITE_TEST_NAME",
            "ACM_VALIDATION_WEBSITE_TEST_VALUE",
        )
        self.project_owner = os.getenv("PROJECT_OWNER")
        self.aws_account = aws_account
        self.region = os.getenv("AWS_REGION")
        self.project_name = project_name
        self.stack_name = project_name
        self.environment = environment
        self.application_id_tag = os.getenv("PROJECT_NAME")
        self.domain_name = os.getenv("DOMAIN_NAME")
        self.s3_website_region = os.getenv("S3_WEBSITE_REGION")
        self.acm_certificate_arn = os.getenv("ACM_CERTIFICATE_ARN")
        
        self.s3_website_production_bucket_name = os.getenv("S3_WEBSITE_PRODUCTION_BUCKET_NAME")
        self.s3_website_dev_bucket_name = os.getenv("S3_WEBSITE_DEV_BUCKET_NAME")
        self.s3_website_test_bucket_name = os.getenv("S3_WEBSITE_TEST_BUCKET_NAME")

        self.acm_validation_cnames = [
            (os.getenv("ACM_VALIDATION_APATITE_IO_NAME"),   os.getenv("ACM_VALIDATION_APATITE_IO_VALUE")),
            (os.getenv("ACM_VALIDATION_WEBSITE_DEV_NAME"),  os.getenv("ACM_VALIDATION_WEBSITE_DEV_VALUE")),
            (os.getenv("ACM_VALIDATION_WEBSITE_TEST_NAME"), os.getenv("ACM_VALIDATION_WEBSITE_TEST_VALUE")),
        ]


class stackConfig:
    def __init__(self, project_name):
        self.prod = StackEnvConfig(
            project_name=project_name,
            environment="production",
            aws_account=os.getenv("AWS_APATITE_PROD_ACCOUNT_ID"),
        )


stack_config = {
    os.getenv("PROJECT_NAME"): stackConfig(project_name=os.getenv("PROJECT_NAME")),
}
