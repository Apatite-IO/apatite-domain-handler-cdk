from aws_cdk import (
    CfnOutput,
    Duration,
    Fn,
    Stack,
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
)
from constructs import Construct
from config.env_config import StackEnvConfig


class cdk_apatiteDomainHandler(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: StackEnvConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.template_options.description = f"{config.project_name} - {config.environment} stack"

        domain = config.domain_name

        # ── Hosted zone ──────────────────────────────────────────────────────
        zone = route53.PublicHostedZone(self, "HostedZone",
            zone_name=domain,
        )

        # ── Nameserver output ─────────────────────────────────────────────────
        for i in range(4):
            CfnOutput(self, f"NameServer{i + 1}",
                value=Fn.select(i, zone.hosted_zone_name_servers),
                description=f"Route53 nameserver {i + 1} — must be set in the registered domain",
            )

        # ── Gmail MX records ─────────────────────────────────────────────────
        route53.MxRecord(self, "GmailMx",
            zone=zone,
            values=[
                route53.MxRecordValue(host_name="aspmx.l.google.com.",      priority=1),
                route53.MxRecordValue(host_name="alt1.aspmx.l.google.com.", priority=5),
                route53.MxRecordValue(host_name="alt2.aspmx.l.google.com.", priority=5),
                route53.MxRecordValue(host_name="alt3.aspmx.l.google.com.", priority=10),
                route53.MxRecordValue(host_name="alt4.aspmx.l.google.com.", priority=10),
            ],
        )

        # ── Gmail SPF record ─────────────────────────────────────────────────
        route53.TxtRecord(self, "GmailSpf",
            zone=zone,
            values=["v=spf1 include:_spf.google.com ~all"],
        )

        # ── ACM certificate validation CNAMEs ────────────────────────────────
        for i, (name, value) in enumerate(config.acm_validation_cnames):
            route53.CnameRecord(self, f"AcmValidationCname{i + 1}",
                zone=zone,
                ttl=Duration.seconds(60),
                record_name=name,
                domain_name=value,
            )

        # ── ACM certificate (manually created in us-east-1) ───────────────────
        certificate = acm.Certificate.from_certificate_arn(
            self, "Certificate", config.acm_certificate_arn
        )

        # ── CloudFront distributions ──────────────────────────────────────────
        # Each site gets its own distribution pointing to a separate S3 bucket.
        # S3 website endpoints only support HTTP on the origin side.
        sites = [
            ("Production",  domain,                         config.s3_website_production_bucket_name),
            ("WebsiteDev",  f"website-dev.{domain}",        config.s3_website_dev_bucket_name),
            ("WebsiteTest", f"website-test.{domain}",       config.s3_website_test_bucket_name),
        ]

        for name, site_domain, bucket_name in sites:
            s3_endpoint = f"{bucket_name}.s3-website-{config.s3_website_region}.amazonaws.com"

            distribution = cloudfront.Distribution(self, f"{name}Distribution",
                default_behavior=cloudfront.BehaviorOptions(
                    origin=origins.HttpOrigin(
                        s3_endpoint,
                        protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                    ),
                    viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                    cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                ),
                domain_names=[site_domain],
                certificate=certificate,
                default_root_object="index.html",
            )

            route53.ARecord(self, f"{name}Alias",
                zone=zone,
                record_name=site_domain,
                target=route53.RecordTarget.from_alias(
                    route53_targets.CloudFrontTarget(distribution)
                ),
            )
