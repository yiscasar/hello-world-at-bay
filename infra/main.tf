#################################
### Hello world app - main ###
#################################

# general tf provider
terraform {
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = "4.55.0"
        }
    }
}

# set aws provider vaues
provider "aws" {
    region     = var.region
    access_key = var.access_key
    secret_key = var.secret_key
}


# create web-app bucket
resource "aws_s3_bucket" "web_app_bucket" {
    bucket = "${var.web_app_bucket_name}"

    website {
        index_document = "index.html"
        error_document = "index.html"
    }

    versioning {
        enabled = true
    }

    tags = merge (
        var.tags,
        { Name = "${var.web_app_bucket_name}" },
    )
}

data "aws_iam_policy_document" "s3_website_policy" {
    statement {
        actions   = ["s3:GetObject"]
        resources = ["${aws_s3_bucket.web_app_bucket.arn}/*"]
        principals {
            type        = "*"
            identifiers = ["*"]
        }
    }
}

resource "aws_s3_bucket_policy" "static_website_policy" {
    bucket = aws_s3_bucket.web_app_bucket.id
    policy = data.aws_iam_policy_document.s3_website_policy.json

    depends_on = [aws_s3_bucket.web_app_bucket]
}

# cloud front access to web-app bucket
resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
    comment = "Allow CloudFront to reach S3 web-app bucket"
}

# cloudFront destrbution
resource "aws_cloudfront_distribution" "hello_world_web_app_distribution" {
    depends_on = [aws_s3_bucket.web_app_bucket]
    origin {
        domain_name = aws_s3_bucket.web_app_bucket.bucket_regional_domain_name
        origin_id   = var.web_app_bucket_name

        s3_origin_config {
            origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
        }
    }

    enabled             = true
    is_ipv6_enabled     = true
    comment             = "hello world web_app distribution"
    default_root_object = "index.html"

    
    default_cache_behavior {
        allowed_methods         = var.allowed_methods
        cached_methods          = var.cached_methods
        target_origin_id        = aws_s3_bucket.web_app_bucket.id

        viewer_protocol_policy = "${var.app_protocol}"

        forwarded_values {
            query_string = false

            cookies {
                forward = "none"
            }
        }

        min_ttl     = var.min_ttl
        default_ttl = var.default_ttl
        max_ttl     = var.max_ttl
    }

    tags = var.tags
}