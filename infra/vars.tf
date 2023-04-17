#################################
### Hello world app - tf vars ###
#################################
# aws creds
variable "access_key" {}
variable "secret_key" {}

# aws region
variable "region" {
    default = "eu-west-1"
}

# default tags - for all resources
variable tags {
    default = {
        owner   = "yisca"
        project = "hello-world-web-app"
        env     = "prod"
    }
}


# web app bucket name
variable "web_app_bucket_name" {
    type        = string
    description = "the name of the s3 bucket which will host the webapp and will hode its files"
    default     = "hello-word-web-app"
}

# cloudFront vars
variable "min_ttl" {
    type        = number
    description = "min time for caching content"
    default     = 0
}

variable "default_ttl" {
    type        = number
    description = "default time for caching content"
    default     = 3600
}

variable "max_ttl" {
    type        = number
    description = "default time for caching content"
    default     = 86400
}


variable "app_protocol" {
    type        = string
    description = "set in which protocol (http, https or both) user can access th app"
    default     = "http-only"
}


variable "allowed_methods" {
  type        = list(string)
  description = "set the HTTP methods that CloudFront processes and forwards to to the web app"
  default     = ["GET", "HEAD"]
}


variable "cached_methods" {
  type        = list(string)
  description = "set the HTTP methods for which CloudFront caches responses"
  default     = ["GET", "HEAD"]
}